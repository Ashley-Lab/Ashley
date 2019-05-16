import json
import discord

from discord.ext import commands
from resources.utility import pokemon
from random import randint
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class PokemonClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='pokemon', aliases=['poke'])
    async def cards(self, ctx):

        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['inventory']['coins'] > 0 and not data['config']['playing']:
            update['config']['playing'] = True
            self.bot.db.update_data(data, update, 'users')

            def check(m):
                return m.author == ctx.author

            response = pokemon[randint(0, 399)]
            embed = discord.Embed(
                title='QUAL O NOME DESSE POKEMON?',
                color=color,
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_image(url=response['foto'])
            await ctx.send(embed=embed)

            if ctx.author.id == self.bot.owner_id:
                await ctx.send(f"``OLÁ MESTRE, SUA RESPOSTA É:`` **{response['nome'].upper()}**")

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=60.0)
            except TimeoutError:
                data = self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['playing'] = False
                self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                      ' CANCELADO**')

            update['inventory']['coins'] -= 1
            if answer.content.upper() == response['nome'].upper():
                await ctx.send(f'<:rank:519896825411665930>│``VOCÊ ACERTOU!`` 🎊 **PARABENS** 🎉 ``O pokemon era`` '
                               f'**{response["nome"]}** ``e vc respondeu`` **{answer.content}** ``Ganhou 12 pontos!``')
                try:
                    update['config']['points'] += 12
                except KeyError:
                    update['config']['points'] = 12
            else:
                await ctx.send(f'<:negate:520418505993093130>│``O pokemon era`` **{response["nome"]}** ``e vc '
                               f'respondeu`` **{answer.content}** ``INFELIZMENTE VOCE PERDEU! LOGO PERDE 8 PONTOS``')
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
    bot.add_cog(PokemonClass(bot))
    print('\033[1;32mO comando \033[1;34mPOKEMONCLASS\033[1;32m foi carregado com sucesso!\33[m')
