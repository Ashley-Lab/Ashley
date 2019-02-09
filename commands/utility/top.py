import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class TopClass(object):
    def __init__(self, bot):
        self.bot = bot
        self.st = []

    def status(self):
        for v in self.bot.data_cog.values():
            self.st.append(v)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.group(name='top', aliases=['tops'])
    async def top(self, ctx):
        if ctx.invoked_subcommand is None:
            self.status()
            top = discord.Embed(title="Commands Status", color=color,
                                description=f"<:on_status:519896814799945728>│On\n"
                                f"<:alert_status:519896811192844288>│Alert\n"
                                f"<:oc_status:519896814225457152>│Off\n"
                                f"<:stream_status:519896814825242635>│Vip")
            top.add_field(name="Top Commands:",
                          value=f"``PREFIX:`` **top** ``+``\n"
                                f"{self.st[67]}│**xp** ``or`` **exp**\n"
                                f"{self.st[67]}│**level** ``or`` **nivel**\n"
                                f"{self.st[67]}│**money** ``or`` **dinheiro**\n"
                                f"{self.st[67]}│**gold** ``or`` **ouro**\n"
                                f"{self.st[67]}│**silver** ``or`` **prata**\n"
                                f"{self.st[67]}│**bronze**\n"
                                f"{self.st[67]}│**point**\n")
            top.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            top.set_thumbnail(url=self.bot.user.avatar_url)
            top.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=top)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='xp', aliases=['exp'])
    async def _xp(self, ctx):
        top = self.bot.data.get_rank_xp(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='level', aliases=['nivel'])
    async def _level(self, ctx):
        top = self.bot.data.get_rank_level(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='money', aliases=['dinheiro'])
    async def _money(self, ctx):
        top = self.bot.data.get_rank_money(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='gold', aliases=['ouro'])
    async def _gold(self, ctx):
        top = self.bot.data.get_rank_gold(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='silver', aliases=['prata'])
    async def _silver(self, ctx):
        top = self.bot.data.get_rank_silver(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='bronze')
    async def _bronze(self, ctx):
        top = self.bot.data.get_rank_bronze(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='point')
    async def _point(self, ctx):
        top = self.bot.data.get_rank_point(20)
        await ctx.send(f'```py\n{top}```')


def setup(bot):
    bot.add_cog(TopClass(bot))
    print('\033[1;32mO comando \033[1;34mTOPCLASS\033[1;32m foi carregado com sucesso!\33[m')
