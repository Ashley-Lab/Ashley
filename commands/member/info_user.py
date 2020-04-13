import discord
from datetime import datetime

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='userinfo', aliases=['infouser', 'ui', 'iu'])
    async def userinfo(self, ctx):
        if ctx.message.guild is not None:
            try:
                data = self.bot.db.get_data("user_id", ctx.author.id, "users")
                if data['config']['vip']:
                    data_ = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
                    if data_['vip']:
                        status = "<:vip_full:546020055478042644>"
                    else:
                        status = "<:vip_member:546020055478042647>"
                else:
                    status = "<:negate:520418505993093130>"
                user = ctx.message.mentions[0]
                role = ",".join([r.name for r in user.roles if r.name != "@everyone"])
                userjoinedat = str(user.joined_at).split('.', 1)[0]
                usercreatedat = str(user.created_at).split('.', 1)[0]
                embed = discord.Embed(
                    title=":pushpin:Informações pessoais de:",
                    color=self.color,
                    description=user.name
                )
                embed.add_field(name=":door:Entrou no server em:", value=userjoinedat, inline=True)
                embed.add_field(name="📅Conta criada em:", value=usercreatedat, inline=True)
                embed.add_field(name="💻ID:", value=user.id, inline=True)
                embed.add_field(name=":label:Tag:", value=user.discriminator, inline=True)
                embed.add_field(name="Cargos:", value=role, inline=True)
                embed.add_field(name="Vip: ", value=status)
                embed.set_footer(text="Pedido por {}#{}".format(ctx.author.name, ctx.author.discriminator))
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.channel.send(embed=embed)
            except IndexError:
                data = self.bot.db.get_data("user_id", ctx.author.id, "users")
                if data['config']['vip']:
                    data_ = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
                    if data_['vip']:
                        status = "<:vip_full:546020055478042644>"
                    else:
                        status = "<:vip_member:546020055478042647>"
                else:
                    status = "<:negate:520418505993093130>"
                user2 = ctx.author
                role2 = ",".join([r.name for r in ctx.author.roles if r.name != "@everyone"])
                userjoinedat2 = str(user2.joined_at).split('.', 1)[0]
                usercreatedat2 = str(user2.created_at).split('.', 1)[0]
                embed2 = discord.Embed(
                    title=":pushpin:Informações pessoais de:",
                    color=self.color,
                    description=user2.name
                )
                embed2.add_field(name=":door:Entrou no server em:", value=userjoinedat2, inline=True)
                embed2.add_field(name="📅Conta criada em:", value=usercreatedat2, inline=True)
                embed2.add_field(name="💻ID:", value=user2.id, inline=True)
                embed2.add_field(name=":label:Tag:", value=user2.discriminator, inline=True)
                embed2.add_field(name="Cargos:", value=role2, inline=True)
                embed2.add_field(name="Vip: ", value=status)
                embed2.set_footer(text="Pedido por {}#{}".format(ctx.author, ctx.author.discriminator))
                embed2.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed2)
            finally:
                pass


def setup(bot):
    bot.add_cog(UserInfo(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUSERINFO\033[1;32m foi carregado com sucesso!\33[m')
