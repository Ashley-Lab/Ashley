import json
import discord

import random
from discord.ext import commands
from resources.db import Database
from resources.check import check_it

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class KickClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='kick', aliases=['chute'])
    async def kick(self, ctx):
        try:
            kickimg = ['https://media.giphy.com/media/28dP8puMEC1iVGgUtY/giphy.gif',
                       'https://media.giphy.com/media/28DOzqSFj5RbODIeu8/giphy.gif',
                       'https://media.giphy.com/media/1eEDH9ib0DpJ48F1oF/giphy.gif',
                       'https://media.giphy.com/media/C9U5DgKIde7fjOWHf6/giphy.gif',
                       'https://media.giphy.com/media/mMCXkn2YIFUdGcthIa/giphy.gif',
                       'https://media.giphy.com/media/5kFQ3Dt7dEmlrUduSR/giphy.gif']
            kick = random.choice(kickimg)
            kickemb = discord.Embed(title='Chute :boot:',
                                    description='**{}** Ele(a) levou um chute de **{}**! {}'
                                                ':joy: '.format(ctx.message.mentions[0].name, ctx.author.name, 'Tomo!'
                                                                if random.randint(1, 2) == 1 else 'Achei merecido.'),
                                    color=color)
            kickemb.set_image(url=kick)
            kickemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=kickemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'abraçar!``')


def setup(bot):
    bot.add_cog(KickClass(bot))
    print('\033[1;32mO comando \033[1;34mKICKCLASS\033[1;32m foi carregado com sucesso!\33[m')
