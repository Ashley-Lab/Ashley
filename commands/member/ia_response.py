import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class IaResponseClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='ia', aliases=['ai'])
    async def ia(self, ctx):
        """comando para habilitar/desabilitar a iteração com a IA da ashley
        use ash ia ou ash ai"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        update['user']['ia_response'] = not update['user']['ia_response']
        response = update['user']['ia_response']
        await self.bot.db.update_data(data, update, "users")
        if response:
            embed = discord.Embed(
                color=discord.Color.green(),
                description=f'<:confirmado:519896822072999937>│``Iteração com a Inteligencia Artificial '
                            f'habilitada com sucesso!``')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'<:confirmado:519896822072999937>│``Iteração com a Inteligencia Artificial '
                            f'desabilitada com sucesso!``')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(IaResponseClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mIA_RESPONSE\033[1;32m foi carregado com sucesso!\33[m')
