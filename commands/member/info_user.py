import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class UserInfo(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='userinfo', aliases=['infouser'])
    async def userinfo(self, ctx):
        if ctx.message.guild is not None:
            try:
                user = ctx.message.mentions[0]
                role = ",".join([r.name for r in user.roles if r.name != "@everyone"])
                userjoinedat = str(user.joined_at).split('.', 1)[0]
                usercreatedat = str(user.created_at).split('.', 1)[0]
                embed = discord.Embed(
                    title=":pushpin:Informações pessoais de:",
                    color=color,
                    description=user.name
                )
                embed.add_field(name=":door:Entrou no server em:", value=userjoinedat, inline=True)
                embed.add_field(name="📅Conta criada em:", value=usercreatedat, inline=True)
                embed.add_field(name="💻ID:", value=user.id, inline=True)
                embed.add_field(name=":label:Tag:", value=user.discriminator, inline=True)
                embed.add_field(name="Cargos:", value=role, inline=True)
                embed.set_footer(text="Pedido por {}#{}".format(ctx.author.name, ctx.author.discriminator))
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.channel.send(embed=embed)
            except IndexError:
                user2 = ctx.author
                role2 = ",".join([r.name for r in ctx.author.roles if r.name != "@everyone"])
                userjoinedat2 = str(user2.joined_at).split('.', 1)[0]
                usercreatedat2 = str(user2.created_at).split('.', 1)[0]
                embed2 = discord.Embed(
                    title=":pushpin:Informações pessoais de:",
                    color=color,
                    description=user2.name
                )
                embed2.add_field(name=":door:Entrou no server em:", value=userjoinedat2, inline=True)
                embed2.add_field(name="📅Conta criada em:", value=usercreatedat2, inline=True)
                embed2.add_field(name="💻ID:", value=user2.id, inline=True)
                embed2.add_field(name=":label:Tag:", value=user2.discriminator, inline=True)
                embed2.add_field(name="Cargos:", value=role2, inline=True)
                embed2.set_footer(text="Pedido por {}#{}".format(ctx.author, ctx.author.discriminator))
                embed2.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed2)
            finally:
                pass


def setup(bot):
    bot.add_cog(UserInfo(bot))
    print('\033[1;32mO comando \033[1;34mUSERINFO\033[1;32m foi carregado com sucesso!\33[m')
