import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

rpg = {
    "Name": None,
    "img": None,
    "vip": False,
    "lower_net": False,
    "Class": 'Default',
    "Level": 1,
    "XP": 0,
    "Status": {"con": 5, "prec": 5, "agi": 5, "atk": 5, "luk": 0, "pdh": 0},
    "artifacts": dict(),
    "relics": dict(),
    'items': list(),
    'equipped_items': list()
}


class RpgStart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='rpg', aliases=['start'])
    async def rpg(self, ctx):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        await self.bot.db.update_data(data, update, 'users')

        msg = ""
        embed = discord.Embed(
            color=self.bot.color,
            description=f'<:stream_status:519896814825242635>│``{msg}``')
        await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @rpg.command(name='class', aliases=["classe", "profissão", "profissao"])
    async def _class(self, ctx):
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(RpgStart(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mRPG_START_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
