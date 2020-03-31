import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class TopClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.st = []
        self.color = self.bot.color

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
            top = discord.Embed(title="Commands Status", color=self.color,
                                description=f"<:on_status:519896814799945728>│On\n"
                                f"<:alert_status:519896811192844288>│Alert\n"
                                f"<:oc_status:519896814225457152>│Off\n"
                                f"<:stream_status:519896814825242635>│Vip")
            top.add_field(name="Top Commands:",
                          value=f"``PREFIX:`` **top** ``+``\n"
                                f"{self.st[67]}│**xp** ``or`` **exp**\n"
                                f"{self.st[67]}│**level** ``or`` **nivel**\n"
                                f"{self.st[67]}│**Ethernia** ``or`` **dinheiro**\n"
                                f"{self.st[67]}│**Ethernia Black** ``or`` **preto**\n"
                                f"{self.st[67]}│**Ethernia Purple** ``or`` **roxo**\n"
                                f"{self.st[67]}│**Ethernia Yellow** ``or`` **amarelo\n"
                                f"{self.st[67]}│**command** ``or`` **comando**\n"
                                f"{self.st[67]}│**point** ``or`` **ponto**\n")
            top.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            top.set_thumbnail(url=self.bot.user.avatar_url)
            top.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=top)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='xp', aliases=['exp'])
    async def _xp(self, ctx):
        top = await self.bot.data.get_rank_xp(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='level', aliases=['nivel'])
    async def _level(self, ctx):
        top = await self.bot.data.get_rank_level(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='ethernia', aliases=['dinheiro'])
    async def _ethernia(self, ctx):
        top = await self.bot.data.get_rank_money(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='black', aliases=['preto', 'Ethernia Black'])
    async def _black(self, ctx):
        top = await self.bot.data.get_rank_gold(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='purple', aliases=['roxo', 'Ethernia Purple'])
    async def _purple(self, ctx):
        top = await self.bot.data.get_rank_silver(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='yellow', aliases=['amarelo', 'Ethernia Yellow'])
    async def _yellow(self, ctx):
        top = await self.bot.data.get_rank_bronze(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='point', aliases=['ponto'])
    async def _point(self, ctx):
        top = await self.bot.data.get_rank_point(20)
        await ctx.send(f'```py\n{top}```')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='command', aliases=['comando'])
    async def _command(self, ctx):
        top = await self.bot.data.get_rank_commands(20)
        await ctx.send(f'```py\n{top}```')


def setup(bot):
    bot.add_cog(TopClass(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mTOPCLASS\033[1;32m foi carregado com sucesso!\33[m')
