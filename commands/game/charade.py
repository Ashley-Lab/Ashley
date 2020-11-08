import discord

from discord.ext import commands
from random import choice
from asyncio import TimeoutError
from resources.check import check_it
from resources.db import Database
from datetime import datetime


class CharadeClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color
        self.charade = self.bot.config['riddles']

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='whats', aliases=['charada'])
    async def whats(self, ctx):
        """Use ash whats ou ash charada e tente adivinhar a resposta certa. foco em tente"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        try:
            if data['inventory']['coins']:
                pass
        except KeyError:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE NÃO TEM FICHA!``')
            return await ctx.send(embed=embed)

        ct = 25
        if data['rpg']['active']:
            date_old = data['rpg']['activated_at']
            date_now = datetime.today()
            days = abs((date_old - date_now).days)
            if days <= 10:
                ct = 5

        if data['inventory']['coins'] > ct and not data['config']['playing']:
            update['config']['playing'] = True
            await self.bot.db.update_data(data, update, 'users')

            def check(m):
                return m.author == ctx.author

            charade_list = list(self.charade.keys())
            charade = choice(charade_list)

            embed = discord.Embed(
                title='A CHADARA É...',
                description=f'```{charade}```',
                color=self.color,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            if ctx.author.id == self.bot.owner_id:
                await ctx.send(f"``OLÁ MESTRE, SUA RESPOSTA É:`` "
                               f"**{self.charade[charade].lower().replace('resposta: ', '')}**")

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['playing'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` **COMANDO'
                                      ' CANCELADO**')

            update['inventory']['coins'] -= ct
            if answer.content.lower() == self.charade[charade].lower().replace('resposta: ', ''):
                await ctx.send(f'<:rank:519896825411665930>│``VOCÊ ACERTOU!`` 🎊 **PARABENS** 🎉 ``A resposta era `` '
                               f'**{self.charade[charade].lower().replace("resposta: ", "")}** ``e vc respondeu`` '
                               f'**{answer.content.lower()}** ``Ganhou 12 pontos!``')

                update['config']['points'] += 12

            elif len([name for name in answer.content.lower().split() if len(name) >= 2 and
                     name in self.charade[charade].lower().replace('resposta: ', '')]) > \
                    (len(self.charade[charade].lower().replace('resposta: ', '').split()) / 2):
                await ctx.send(f'<:rank:519896825411665930>│``VOCÊ QUASE ACERTOU!`` 🎊 **PARABENS** 🎉 ``A resposta '
                               f'era `` **{self.charade[charade].lower().replace("resposta: ", "")}** ``e vc '
                               f'respondeu`` **{answer.content.lower()}** ``Ganhou 4 pontos!``')

                update['config']['points'] += 4

            else:
                await ctx.send(f'<:negate:721581573396496464>│``A resposta era `` '
                               f'**{self.charade[charade].lower().replace("resposta: ", "")}** ``e vc '
                               f'respondeu`` **{answer.content.lower()}** '
                               f'``INFELIZMENTE VOCE PERDEU! LOGO PERDE 8 PONTOS``')

                if update['config']['points'] - 8 >= 0:
                    update['config']['points'] -= 8
                else:
                    update['config']['points'] = 0

            update['config']['playing'] = False
            await self.bot.db.update_data(data, update, 'users')

        else:
            if data['config']['playing']:
                await ctx.send('<:alert:739251822920728708>│``VOCÊ JÁ ESTÁ JOGANDO!``')
            else:
                await ctx.send(f'<:alert:739251822920728708>│``VOCÊ PRECISA DE + DE {ct} FICHAS PARA JOGAR``\n'
                               f'**OBS:** ``USE O COMANDO`` **ASH SHOP** ``PARA COMPRAR FICHAS!``')


def setup(bot):
    bot.add_cog(CharadeClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mCHARADECLASS\033[1;32m foi carregado com sucesso!\33[m')
