import json
import discord

from discord.ext import commands
from resources.db import Database
from resources.check import check_it

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class SkinMine(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='skin', aliases=['mine'])
    async def skin(self, ctx, skin=None):
        if skin is not None:
            embed = discord.Embed(color=color, )
            embed.set_image(url=f"https://mc-heads.net/skin/{skin}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:oc_status:519896814225457152>│``Você precisa escolher uma skin!``")


def setup(bot):
    bot.add_cog(SkinMine(bot))
    print('\033[1;32mO comando \033[1;34mSKIN_MINE\033[1;32m foi carregado com sucesso!\33[m')
