from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class DoorClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='door', aliases=['porta'])
    async def door(self, ctx):
        """Esse nem eu sei..."""
        pass


def setup(bot):
    bot.add_cog(DoorClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDOOR_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
