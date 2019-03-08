import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class ActionsClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def add_vip(self, ctx, id_: int = None, target: str = "guild"):
        if target == "guild":
            guild = self.bot.get_guild(id_)
            if guild is None:
                return await ctx.send("<:oc_status:519896814225457152>│``GUILDA INVALIDA!``")
            self.bot.data.add_vip(target="guild", guild_id=id_, state=True)
        elif target == "user":
            user = self.bot.get_user(id_)
            if user is None:
                return await ctx.send("<:oc_status:519896814225457152>│``USUÁRIO INVALIDO!``")
            self.bot.data.add_vip(target="user", user_id=id_, state=True)
        else:
            return await ctx.send("<:oc_status:519896814225457152>│``OPÇÃO INVALIDA!``")
        embed = discord.Embed(
            color=color,
            description=f'<:confirmado:519896822072999937>│``Vip Adicionado com sucesso!``')
        await ctx.send(embed=embed)

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def remove_vip(self, ctx, id_: int = None, target: str = "guild"):
        if target == "guild":
            guild = self.bot.get_guild(id_)
            if guild is None:
                return await ctx.send("<:oc_status:519896814225457152>│``GUILDA INVALIDA!``")
            self.bot.data.add_vip(target="guilds", guild_id=id_, state=False)
        elif target == "user":
            user = self.bot.get_user(id_)
            if user is None:
                return await ctx.send("<:oc_status:519896814225457152>│``USUÁRIO INVALIDO!``")
            self.bot.data.add_vip(target="users", user_id=id_, state=False)
        else:
            return await ctx.send("<:oc_status:519896814225457152>│``OPÇÃO INVALIDA!``")
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'<:confirmado:519896822072999937>│``Vip retirado com sucesso!``')
        await ctx.send(embed=embed)

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def add_ban(self, ctx, id_: int = None, *, reason: str = "SEM REGISTRAR O MOTIVO!"):
        if id_ is None:
            return await ctx.send("<:oc_status:519896814225457152>│``O ID NÃO PODE SER VAZIO!``")
        guild = self.bot.get_guild(id_)
        if guild is None:
            user = self.bot.get_user(id_)
            if user is None:
                return await ctx.send("<:oc_status:519896814225457152>│``ID INVALIDO!``")
        self.bot.ban_(id_, reason)
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'<:confirmado:519896822072999937>│``Banimento adicionado com sucesso!``')
        await ctx.send(embed=embed)

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def remove_ban(self, ctx, id_: int = None):
        if id_ is None:
            return await ctx.send("<:oc_status:519896814225457152>│``O ID NÃO PODE SER VAZIO!``")
        guild = self.bot.get_guild(id_)
        if guild is None:
            user = self.bot.get_user(id_)
            if user is None:
                return await ctx.send("<:oc_status:519896814225457152>│``ID INVALIDO!``")
        self.bot.un_ban_(id_)
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'<:confirmado:519896822072999937>│``Banimento revogado com sucesso!``')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ActionsClass(bot))
    print('\033[1;32mO comando \033[1;34mACTIONS\033[1;32m foi carregado com sucesso!\33[m')
