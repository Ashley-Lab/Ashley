from discord.ext import commands
from resources.ia_list import palin
from random import choice
from resources.check import check_it
from resources.db import Database


class Inverse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='palin', aliases=['palindromo'])
    async def palin(self, ctx):
        answer = choice(palin)
        await ctx.channel.send('''```Markdown\n [>]: {}```'''.format(answer.upper()))


def setup(bot):
    bot.add_cog(Inverse(bot))
    print('\033[1;32mO comando \033[1;34mPALINDROMO\033[1;32m foi carregado com sucesso!\33[m')
