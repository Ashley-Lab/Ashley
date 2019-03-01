import json
import discord

from random import choice
from discord.ext import commands
from resources.db import Database
from resources.check import check_it

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class PunchClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='punch', aliases=['soco'])
    async def punch(self, ctx):
        try:
            punchimg = ['https://media.giphy.com/media/loMkSw7gyB5FKOK7mR/giphy.gif',
                        'https://media.giphy.com/media/8JW411NAN3yAT5dYst/giphy.gif',
                        'https://media.giphy.com/media/1H84T9Cm1SF15uFca4/giphy.gif',
                        'https://media.giphy.com/media/bwPqXlNEDvT3URFBIa/giphy.gif',
                        'https://media.giphy.com/media/YVrv6Z9gdfqkHl4mHa/giphy.gif',
                        'https://media.giphy.com/media/nyjEMeiIK7n9APuzrv/giphy.gif']
            punch = choice(punchimg)
            punchemb = discord.Embed(title='Soco :boxing_glove: ',
                                     description='**{}** Ele(a) levou um soco de **{}**! GAME! '
                                                 ':regional_indicator_k: :regional_indicator_o:  '
                                     .format(ctx.message.mentions[0].name, ctx.author.name),
                                     color=color)
            punchemb.set_image(url=punch)
            punchemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=punchemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'abraçar!``')


def setup(bot):
    bot.add_cog(PunchClass(bot))
    print('\033[1;32mO comando \033[1;34mPUNCHCLASS\033[1;32m foi carregado com sucesso!\33[m')
