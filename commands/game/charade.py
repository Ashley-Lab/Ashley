import json
import discord

from discord.ext import commands
from random import choice
from asyncio import TimeoutError
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class CharadeClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("resources/charadas.json", "r", encoding='utf-8') as f:
            self.charade = json.loads(f.read())

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='whats', aliases=['charada'])
    async def whats(self, ctx):

        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['inventory']['coins'] > 0 and not data['config']['playing']:
            update['config']['playing'] = True
            self.bot.db.update_data(data, update, 'users')

            def check(m):
                return m.author == ctx.author

            charade_list = list(self.charade.keys())
            charade = choice(charade_list)

            embed = discord.Embed(
                title='A CHADARA É...',
                description=f'```{charade}```',
                color=color,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            if ctx.author.id == self.bot.owner_id:
                await ctx.send(f"``OLÁ MESTRE, SUA RESPOSTA É:`` "
                               f"**{self.charade[charade].lower().replace('resposta: ', '')}**")

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=60.0)
            except TimeoutError:
                update['config']['playing'] = False
                self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                      ' CANCELADO**')

            update['inventory']['coins'] -= 1
            if answer.content.lower() == self.charade[charade].lower().replace('resposta: ', ''):
                await ctx.send(f'<:rank:519896825411665930>│``VOCÊ ACERTOU!`` 🎊 **PARABENS** 🎉 ``A resposta era `` '
                               f'**{self.charade[charade].lower().replace("resposta: ", "")}** ``e vc respondeu`` '
                               f'**{answer.content.lower()}** ``Ganhou 12 pontos!``')

                try:
                    update['config']['points'] += 12
                except KeyError:
                    update['config']['points'] = 12

            elif len([name for name in answer.content.lower().split() if len(name) >= 2 and
                     name in self.charade[charade].lower().replace('resposta: ', '')]) > \
                    (len(self.charade[charade].lower().replace('resposta: ', '').split()) / 2):
                await ctx.send(f'<:rank:519896825411665930>│``VOCÊ QUASE ACERTOU!`` 🎊 **PARABENS** 🎉 ``A resposta '
                               f'era `` **{self.charade[charade].lower().replace("resposta: ", "")}** ``e vc '
                               f'respondeu`` **{answer.content.lower()}** ``Ganhou 4 pontos!``')

                try:
                    update['config']['points'] += 4
                except KeyError:
                    update['config']['points'] = 4

            else:
                await ctx.send(f'<:negate:520418505993093130>│``A resposta era `` '
                               f'**{self.charade[charade].lower().replace("resposta: ", "")}** ``e vc '
                               f'respondeu`` **{answer.content.lower()}** '
                               f'``INFELIZMENTE VOCE PERDEU! LOGO PERDE 8 PONTOS``')

                try:
                    if update['config']['points'] - 8 >= 0:
                        update['config']['points'] -= 8
                    else:
                        update['config']['points'] = 0
                except KeyError:
                    update['config']['points'] = 0

            update['config']['playing'] = False
            self.bot.db.update_data(data, update, 'users')

        else:
            if data['config']['playing']:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ JÁ ESTÁ JOGANDO!``')
            else:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ PRECISA DE FICHAS PARA JOGAR``')


def setup(bot):
    bot.add_cog(CharadeClass(bot))
    print('\033[1;32mO comando \033[1;34mCHARADECLASS\033[1;32m foi carregado com sucesso!\33[m')
