import json
import discord

from random import choice
from discord.ext import commands
from resources.db import Database
from resources.check import check_it

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class DanceClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='dance', aliases=['dança'])
    async def dance(self, ctx):
        try:
            dance_img = ['https://media.giphy.com/media/1woCaEQvSvKMODsyEA/giphy.gif',
                         'https://media.giphy.com/media/xWfS0QepPvL3iYViCY/giphy.gif',
                         'https://media.giphy.com/media/5kFckUFIHb5W07fpmJ/giphy.gif',
                         'https://media.giphy.com/media/1X8U0exkuqAMMKAQ3Y/giphy.gif',
                         'https://media.giphy.com/media/58FpXQi6fKXrQcZPba/giphy.gif']
            dance = choice(dance_img)
            dance_embed = discord.Embed(title='Dance <a:dyno:541775159460102167>',
                                        description='**{}** Ele(a) esta dançando com **{}**! Alguem tira foto! EU '
                                                    'SHIPPO! :heart_eyes: '.format(ctx.message.mentions[0].name,
                                                                                   ctx.author.name),
                                        color=color)
            dance_embed.set_image(url=dance)
            dance_embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=dance_embed)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'dançar!``')


def setup(bot):
    bot.add_cog(DanceClass(bot))
    print('\033[1;32mO comando \033[1;34mDANCE\033[1;32m foi carregado com sucesso!\33[m')
