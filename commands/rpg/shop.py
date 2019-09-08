from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class ShopClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='shop', aliases=['loja'])
    async def shop(self, ctx):
        return await ctx.send("em desenvolvimento...")


def setup(bot):
    bot.add_cog(ShopClass(bot))
    print('\033[1;32mO comando \033[1;34mSHOP\033[1;32m foi carregado com sucesso!\33[m')
