import json
import discord

from discord.ext import commands
from asyncio import sleep
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def reload(self, ctx, cog):
        try:
            self.bot.unload_extension('{}'.format(cog))
            await sleep(1)
            self.bot.load_extension('{}'.format(cog))
            embed = discord.Embed(
                color=color,
                description=f'<:confirmado:519896822072999937>│Extenção **{cog}**, recarregada com sucesso!')
            await ctx.send(embed=embed)
        except ModuleNotFoundError as e:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'<:oc_status:519896814225457152>│Falha ao recarregar a extenção **{cog}**. \n```{e}```')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ReloadCog(bot))
    print('\033[1;32mO comando \033[1;34mRELOAD\033[1;32m foi carregado com sucesso!\33[m')
