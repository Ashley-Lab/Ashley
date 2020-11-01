import discord

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
    async def userinfo(self, ctx, member: discord.Member = None):
        """comando que da uma lista de informações sobre o usuario
        Use ash userinfo <@usuario em questão>"""
        if member is None:
            member = ctx.author

        data = await self.bot.db.get_data("user_id", member.id, "users")
        if data is not None:
            database = f"USUARIO CADASTRADO"
        else:
            database = "USUARIO NAO CADASTRADO"

        role = ",".join([r.name for r in member.roles if r.name != "@everyone"])
        userjoinedat = str(member.joined_at).split('.', 1)[0]
        usercreatedat = str(member.created_at).split('.', 1)[0]

        embed = discord.Embed(
            title=":pushpin:Informações pessoais de:",
            color=self.color,
            description=member.name
        )
        embed.add_field(name=":door:Entrou no server em:", value=userjoinedat, inline=True)
        embed.add_field(name="📅Conta criada em:", value=usercreatedat, inline=True)
        embed.add_field(name="💻ID:", value=str(member.id), inline=True)
        embed.add_field(name=":label:Tag:", value=str(member.discriminator), inline=True)
        embed.add_field(name="Cargos:", value=role, inline=True)
        embed.add_field(name="DataBase:", value=database)
        embed.set_footer(text="Pedido por {}#{}".format(ctx.author.name, ctx.author.discriminator))
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UserInfo(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUSERINFO\033[1;32m foi carregado com sucesso!\33[m')
