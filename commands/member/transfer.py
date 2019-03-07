from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class TransferClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='transfer', aliases=['trans'])
    async def transfer(self, ctx):
        await ctx.send("<:confirmado:519896822072999937>│``COMANDO AINDA EM CRIAÇÃO!``")


def setup(bot):
    bot.add_cog(TransferClass(bot))
    print('\033[1;32mO comando \033[1;34mTRANSFER_CLASS\033[1;32m foi carregado com sucesso!\33[m')
