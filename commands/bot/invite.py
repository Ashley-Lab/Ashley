import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class InviteClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://discordapp.com/oauth2/authorize?client_id=478977311266570242&scope=bot&permissions=8"
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='invite', aliases=['convite'])
    async def invite(self, ctx):
        await ctx.send("<:send:519896817320591385>│``Obrigado por querer participar da`` "
                                       "**MINHA COMUNIDADE** ``irei enviar para seu privado um convite "
                                       "para que você possa entrar!``")
        try:
            embed = discord.Embed(
                color=self.color,
                description=f'<:safada:530029764061298699>│[CLIQUE AQUI PARA ME ADICIONAR NO SEU '
                            f'SERVIDOR]({self.url})')

            await ctx.author.send("<:confirmado:519896822072999937>│https://discord.gg/rYT6QrM")
            await ctx.author.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send('<:negate:520418505993093130>│``INFELIZMENTE NÃO FOI POSSIVEL ENVIAR A MENSAGEM PRA VOCÊ``')


def setup(bot):
    bot.add_cog(InviteClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mINVITE\033[1;32m foi carregado com sucesso!\33[m')
