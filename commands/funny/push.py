import json
import discord

from random import choice
from discord.ext import commands
from resources.db import Database
from resources.check import check_it

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class PushClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='push', aliases=['empurrao'])
    async def push(self, ctx):
        try:
            pushimg = ['https://media.giphy.com/media/2eqvwrFmCPz4ngW0DC/giphy.gif',
                       'https://media.giphy.com/media/4Q1I8CEIjkQAvZnmPx/giphy.gif',
                       'https://media.giphy.com/media/dB1Ds51ye6smSv09lX/giphy.gif',
                       'https://media.giphy.com/media/vcAXxIghuHWaPainqe/giphy.gif',
                       'https://media.giphy.com/media/65zUCIaDvzhyQdYThW/giphy.gif']
            push = choice(pushimg)
            pushemb = discord.Embed(title='Empurrão :raised_hands:',
                                    description='**{}** Ele(a) recebeu um empurrão de **{}**! BRIGA! '
                                                ':laughing: '.format(ctx.message.mentions[0].name, ctx.author.name),
                                    color=color)
            pushemb.set_image(url=push)
            pushemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=pushemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'abraçar!``')


def setup(bot):
    bot.add_cog(PushClass(bot))
    print('\033[1;32mO comando \033[1;34mPUSHCLASS\033[1;32m foi carregado com sucesso!\33[m')
