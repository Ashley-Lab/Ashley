import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.giftmanage import register_gift
from resources.img_edit import gift as gt


class UtilityClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='create_gift', aliases=['cg'])
    async def create_gift(self, ctx, time=None):
        """Esse nem eu sei..."""
        if time is None:
            return await ctx.send("<:alert:739251822920728708>│``Digite o tempo de cooldown do gift.``")
        try:
            time = int(time)
        except ValueError:
            return await ctx.send("<:alert:739251822920728708>│``O tempo de cooldown deve ser em numeros.``")

        gift = await register_gift(self.bot, time)
        gt(gift, f"{time} SEGUNDOS")
        await ctx.send(file=discord.File('giftcard.png'))
        await ctx.send(f"> 🎊 **PARABENS** 🎉 ``VOCÊ GANHOU UM GIFT``\n"
                       f"``USE O COMANDO:`` **ASH GIFT** ``PARA RECEBER SEU PRÊMIO!!``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='lover', aliases=['al'])
    async def lover(self, ctx):
        """Esse nem eu sei..."""
        if ctx.guild.id == 643936732236087306:
            try:
                role = discord.utils.find(lambda r: r.name == "</Ash_Lovers>", ctx.guild.roles)
                if role is not None:
                    if role not in [r for r in ctx.author.roles]:
                        await ctx.author.add_roles(role)
                        await ctx.send("<:confirmed:721581574461587496>│``VOCE AGORA É UM LOVER MEU!! FALE NO "
                                       "CHAT_VIP PARA COMEMORAR!!``")
                    else:
                        await ctx.send("<:alert:739251822920728708>│``VOCE JA É UM LOVER MEU! MAS OBG POR "
                                       "TANTO AMOR``")
                else:
                    await ctx.send("<:alert:739251822920728708>│``O MEU CARGO NAO EXISTE MAIS, PEÇA PRA UM ADM"
                                   " CRIAR O CARGO NOVAMENTE!``")
            except discord.Forbidden:
                await ctx.send("<:negate:721581573396496464>│``NAO TENHO PERMISSÃO DE ADICIONAR CARGOS!``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='unlover', aliases=['ual'])
    async def unlover(self, ctx):
        """Esse nem eu sei..."""
        if ctx.guild.id == 643936732236087306:
            try:
                role = discord.utils.find(lambda r: r.name == "</Ash_Lovers>", ctx.guild.roles)
                if role is not None:
                    if role in [r for r in ctx.author.roles]:
                        await ctx.author.remove_roles(role)
                        await ctx.send("<:confirmed:721581574461587496>│``QUE PENA, VOCE NAO ME AMA MAIS?!``")
                    else:
                        await ctx.send("<:alert:739251822920728708>│``VOCE NAO TEM MAIS O MEU CARGO, POXA..."
                                       " ME ODEIA TANTO ASSIM?``")
                else:
                    await ctx.send("<:alert:739251822920728708>│``O MEU CARGO NAO EXISTE MAIS, PEÇA PRA UM ADM"
                                   " CRIAR O CARGO NOVAMENTE!``")
            except discord.Forbidden:
                await ctx.send("<:negate:721581573396496464>│``NAO TENHO PERMISSÃO DE RETIRAR CARGOS!``")


def setup(bot):
    bot.add_cog(UtilityClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUTILITY_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
