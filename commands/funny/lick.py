import discord

from random import choice
from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class LickClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='lick', aliases=['lambida'])
    async def lick(self, ctx):
        try:
            lickimg = ['https://media.giphy.com/media/2tKBNfl2rCnpeJXS4H/giphy.gif',
                       'https://media.giphy.com/media/3ZZ9tf6NpY0pxr9VYo/giphy.gif',
                       'https://media.giphy.com/media/40bEkgVmarjulQAo1M/giphy.gif',
                       'https://media.giphy.com/media/TIx5q55UTonDN0oxw2/giphy.gif',
                       'https://media.giphy.com/media/PNxrsO5Ql0RibjZCxo/giphy.gif']
            lick = choice(lickimg)
            lickemb = discord.Embed(title='Lambida :heart:',
                                    description='**{}** Ele(a) recebeu uma lambida de **{}**! Que casal fofo! '
                                                ':heart_eyes: '.format(ctx.message.mentions[0].name, ctx.author.name),
                                    color=self.color)
            lickemb.set_image(url=lick)
            lickemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=lickemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'lamber!``')


def setup(bot):
    bot.add_cog(LickClass(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mLICKCLASS\033[1;32m foi carregado com sucesso!\33[m')
