from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class PingMS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='ping', aliases=['latency'])
    async def ping(self, ctx):
        """comando pra verificar a latencia do bot
        Use ash ping"""
        if ctx.message.guild is not None:
            ping = round(self.bot.latency * 1000)
            await ctx.send("🏓 ``Pong:`` **{}ms**".format(ping))


def setup(bot):
    bot.add_cog(PingMS(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPINGMS\033[1;32m foi carregado com sucesso!\33[m')
