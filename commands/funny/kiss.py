import discord

from random import choice
from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class KissClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='kiss', aliases=['beijo'])
    async def kiss(self, ctx):
        try:
            kissimg = ['https://media.giphy.com/media/xTDsoOpxyc0mfD5kRL/giphy.gif',
                       'https://media.giphy.com/media/YFI5F1DGueggFIwjFQ/giphy.gif',
                       'https://media.giphy.com/media/NRensrTKS7couFakNT/giphy.gif',
                       'https://media.giphy.com/media/8cj4Ir95UFQGEiphsV/giphy.gif',
                       'https://media.giphy.com/media/yvBl6HeIYNjiiKTw3W/giphy.gif']
            kiss = choice(kissimg)
            kissemb = discord.Embed(title='Beijo :heart:',
                                    description='**{}** Ele(a) recebeu um beijo de **{}**! Que casal fofo! '
                                                ':heart_eyes: '.format(ctx.message.mentions[0].name, ctx.author.name),
                                    color=self.color)
            kissemb.set_image(url=kiss)
            kissemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=kissemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'beijar!``')


def setup(bot):
    bot.add_cog(KissClass(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mKISSCLASS\033[1;32m foi carregado com sucesso!\33[m')
