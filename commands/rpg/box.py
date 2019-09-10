import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import paginator

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class BoxClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='box', aliases=['caixa'])
    async def box(self, ctx):
        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        if ctx.author.id == data["user_id"]:
            try:
                if data['box']:
                    embed = discord.Embed(
                        title='Box:',
                        color=color,
                        description=f"```py\n{data['box']['status']}```")
                    embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                    embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                    await ctx.send(embed=embed)
            except KeyError:
                await ctx.send("<:negate:520418505993093130>│``Você nao tem box na sua conta ainda...``")


def setup(bot):
    bot.add_cog(BoxClass(bot))
    print('\033[1;32mO comando \033[1;34mBOXCLASS\033[1;32m foi carregado com sucesso!\33[m')