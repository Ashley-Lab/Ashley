import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class UtilityClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                    if role in [r for r in ctx.author.roles]:
                        await user.add_roles(role)
                        await ctx.send("<:confirmado:519896822072999937>│``VOCE AGORA É UM LOVER MEU!! FALE NO "
                                       "CHAT_VIP PARA COMEMORAR!!``")
                    else:
                        await ctx.send("<:alert_status:519896811192844288>│``VOCE JA É UM LOVER MEU! MAS OBG POR "
                                       "TANTO AMOR``")
                else:
                    await ctx.send("<:alert_status:519896811192844288>│``O MEU CARGO NAO EXISTE MAIS, PEÇA PRA UM ADM"
                                   " CRIAR O CARGO NOVAMENTE!``")
            except discord.Forbidden:
                await ctx.send("<:oc_status:519896814225457152>│``NAO TENHO PERMISSÃO DE ADICIONAR CARGOS!``")

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
                        await user.remove_roles(role)
                        await ctx.send("<:confirmado:519896822072999937>│``QUE PENA, VOCE NAO ME AMA MAIS?!``")
                    else:
                        await ctx.send("<:alert_status:519896811192844288>│``VOCE NAO TEM MAIS O MEU CARGO, POXA..."
                                       " ME ODEIA TANTO ASSIM?``")
                else:
                    await ctx.send("<:alert_status:519896811192844288>│``O MEU CARGO NAO EXISTE MAIS, PEÇA PRA UM ADM"
                                   " CRIAR O CARGO NOVAMENTE!``")
            except discord.Forbidden:
                await ctx.send("<:oc_status:519896814225457152>│``NAO TENHO PERMISSÃO DE RETIRAR CARGOS!``")


def setup(bot):
    bot.add_cog(UtilityClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDOOR_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
