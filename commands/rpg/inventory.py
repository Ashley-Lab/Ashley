import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import paginator

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class InventoryClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.i = self.bot.items

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='inventory', aliases=['inventario', 'i'])
    async def inventory(self, ctx):
        if ctx.invoked_subcommand is None:
            data = self.bot.db.get_data("user_id", ctx.author.id, "users")
            if ctx.author.id == data["user_id"]:
                embed = ['Inventário:', color, 'Items: \n']
                await paginator(self.bot, self.i, data['inventory'], embed, ctx)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @inventory.command(name='quest', aliases=['missao'])
    async def _shop(self, ctx):
        return await ctx.send("<:negate:520418505993093130>│``O inventário de missões ainda não está disponível!``")


def setup(bot):
    bot.add_cog(InventoryClass(bot))
    print('\033[1;32mO comando \033[1;34mINVENTORYCLASS\033[1;32m foi carregado com sucesso!\33[m')
