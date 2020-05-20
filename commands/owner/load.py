import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class LoadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def load(self, ctx, cog):
        """apenas desenvolvedores"""
        try:
            self.bot.load_extension('{}'.format(cog))
            embed = discord.Embed(
                color=self.color,
                description=f'<:confirmado:519896822072999937>│Extenção **{cog}**, carregada com sucesso!')
            await ctx.send(embed=embed)
        except ModuleNotFoundError as e:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'<:oc_status:519896814225457152>│Falha ao carregar a extenção **{cog}**. \n```{e}```')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LoadCog(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mLOAD\033[1;32m foi carregado com sucesso!\33[m')
