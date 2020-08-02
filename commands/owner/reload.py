import discord

from discord.ext import commands
from asyncio import sleep
from resources.check import check_it
from resources.db import Database


class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='reload')
    async def reload(self, ctx, cog):
        """apenas desenvolvedores"""
        try:
            self.bot.unload_extension('{}'.format(cog))
            await sleep(1)
            self.bot.load_extension('{}'.format(cog))
            embed = discord.Embed(
                color=self.color,
                description=f'<:confirmed:721581574461587496>│Extenção **{cog}**, recarregada com sucesso!')
            await ctx.send(embed=embed)
        except ModuleNotFoundError as e:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'<:negate:721581573396496464>│Falha ao recarregar a extenção **{cog}**. \n```{e}```')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ReloadCog(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mRELOAD\033[1;32m foi carregado com sucesso!\33[m')
