import json
import discord

from random import choice
from discord.ext import commands
from resources.db import Database
from resources.check import check_it

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class SlapClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='slap', aliases=['tapa'])
    async def slap(self, ctx):
        try:
            slapimg = ['https://media.giphy.com/media/2ni8mCQhDe6buYEzMG/giphy.gif',
                       'https://media.giphy.com/media/c75UADvToGNZTBFBtO/giphy.gif',
                       'https://media.giphy.com/media/7zMvSym6iPdlNvm8hd/giphy.gif',
                       'https://media.giphy.com/media/3d5NhNnsXQ7LB1XhH5/giphy.gif',
                       'https://media.giphy.com/media/U86rbsmKUVtQVODuoI/giphy.gif']
            slap = choice(slapimg)
            slapemb = discord.Embed(title='Tapa :wave:',
                                    description='**{}** Ele(a) levou um tapa de **{}**! Acho que doeu... '
                                                'SOLDADO FERIDO! :broken_heart: '.format(ctx.message.mentions[0].name,
                                                                                         ctx.author.name),
                                    color=color)
            slapemb.set_image(url=slap)
            slapemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=slapemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'dar um tapa!``')


def setup(bot):
    bot.add_cog(SlapClass(bot))
    print('\033[1;32mO comando \033[1;34mSLAPCLASS\033[1;32m foi carregado com sucesso!\33[m')
