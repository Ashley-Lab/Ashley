import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class LogoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='logout')
    async def logout(self, ctx, *, reason: str = None):
        """apenas desenvolvedores"""
        if reason is None:
            return await ctx.send('<:alert:739251822920728708>│``DIGA UM MOTIVO PARA ME DESLIGAR!``')
        await self.bot.shutdown(reason)
        embed = discord.Embed(
            color=self.color,
            description=f'<:confirmed:721581574461587496>│**Logging out...**')
        await ctx.send(embed=embed)
        await self.bot.logout()


def setup(bot):
    bot.add_cog(LogoutCog(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mLOGOUT\033[1;32m foi carregado com sucesso!\33[m')
