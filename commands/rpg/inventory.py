import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class InventoryClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='inventory', aliases=['inventario', 'i'])
    async def inventory(self, ctx):
        if ctx.invoked_subcommand is None:
            data = self.bot.db.get_data("user_id", ctx.author.id, "users")
            if ctx.author.id == data["user_id"]:
                inventory = 'Itens: \n'
                for key in data['inventory'].keys():
                    inventory += f"{self.bot.items[key][0]} **{key.upper()}**: {data['inventory'][key]}\n"
                resposta = discord.Embed(
                    title='Inventário (BETA):',
                    color=color,
                    description=f"{inventory}"
                )
                resposta.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                resposta.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                resposta.set_footer(text="Ashley ® Todos os direitos reservados.")
                await ctx.channel.send(embed=resposta, delete_after=120.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @inventory.command(name='shop', aliases=['loja'])
    async def _shop(self, ctx):
        return


def setup(bot):
    bot.add_cog(InventoryClass(bot))
    print('\033[1;32mO comando \033[1;34mINVENTORYCLASS\033[1;32m foi carregado com sucesso!\33[m')
