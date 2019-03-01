import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class TotComandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command()
    async def total_de_comandos(self, ctx):
        embed = discord.Embed(color=color)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        for val in self.bot.commands_used.most_common(25):
            embed.add_field(name=val[0], value=val[1])
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TotComandos(bot))
    print('\033[1;32mO comando \033[1;34mTOTCOMANDOS\033[1;32m foi carregado com sucesso!\33[m')
