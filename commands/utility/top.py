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
        """Comando usado pra retornar a lista de subcomandos de top
        Use ash top"""
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
                                f"{self.st[67]}│**money** ``or`` **dinheiro**\n"
                                f"{self.st[67]}│**ethernya black** ``or`` **eb**\n"
                                f"{self.st[67]}│**ethernya purple** ``or`` **ep**\n"
                                f"{self.st[67]}│**ethernya yellow** ``or`` **ey**\n"
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
        """Comando usado pra retornar o top 20 em questão de xp da Ashley
        Use ash top xp"""
        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")
        top = await self.bot.data.get_rank_xp(20)
        await ctx.send(f'<:rank:519896825411665930>|**TOP XP**```py\n{top}```')
        await msg.delete()

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='level', aliases=['nivel'])
    async def _level(self, ctx):
        """Comando usado pra retornar o top 20 em questão de level da Ashley
        Use ash top level"""
        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")
        top = await self.bot.data.get_rank_level(20)
        await ctx.send(f'<:rank:519896825411665930>|**TOP LEVEL/NIVEL**```py\n{top}```')
        await msg.delete()

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='money', aliases=['dinheiro', 'ethernya'])
    async def _money(self, ctx):
        """Comando usado pra retornar o top 20 em questão de ethernia da Ashley
        Use ash top ethernia"""
        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")
        top = await self.bot.data.get_rank_money(20)
        await ctx.send(f'<:rank:519896825411665930>|**TOP MONEY/ETHERNYA**```py\n{top}```')
        await msg.delete()

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='black', aliases=['preto', 'ethernia black', 'eb'])
    async def _black(self, ctx):
        """Comando usado pra retornar o top 20 em questão de ethernia negra da Ashley
        Use ash top preto"""
        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")
        top = await self.bot.data.get_rank_gold(20)
        await ctx.send(f'<:rank:519896825411665930>|**TOP ETHERNYA BLACK**```py\n{top}```')
        await msg.delete()

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='purple', aliases=['roxo', 'ethernia purple', 'ep'])
    async def _purple(self, ctx):
        """Comando usado pra retornar o top 20 em questão de ethernia roxa da Ashley
        Use ash top roxo"""
        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")
        top = await self.bot.data.get_rank_silver(20)
        await ctx.send(f'<:rank:519896825411665930>|**TOP ETHERNYA PURPLE**```py\n{top}```')
        await msg.delete()

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='yellow', aliases=['amarelo', 'ethernia yellow', 'ey'])
    async def _yellow(self, ctx):
        """Comando usado pra retornar o top 20 em questão de ethernia amarela da Ashley
        Use ash top amarelo"""
        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")
        top = await self.bot.data.get_rank_bronze(20)
        await ctx.send(f'<:rank:519896825411665930>|**TOP ETHENYA YELLOW**```py\n{top}```')
        await msg.delete()

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='point', aliases=['ponto'])
    async def _point(self, ctx):
        """Comando usado pra retornar o top 20 em questão de pontos da Ashley
        Use ash top point"""
        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")
        top = await self.bot.data.get_rank_point(20)
        await ctx.send(f'<:rank:519896825411665930>|**TOP POINT**```py\n{top}```')
        await msg.delete()

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @top.group(name='command', aliases=['comando'])
    async def _command(self, ctx):
        """Comando usado pra retornar o top 20 em questão de comandos usados
        Use ash top command"""
        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``\n"
                             "**mesmo que demore, aguarde o fim do processamento...**")
        top = await self.bot.data.get_rank_commands(20)
        await ctx.send(f'<:rank:519896825411665930>|**TOP COMMAND**```py\n{top}```')
        await msg.delete()


def setup(bot):
    bot.add_cog(TopClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mTOPCLASS\033[1;32m foi carregado com sucesso!\33[m')
