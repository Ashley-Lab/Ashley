import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class AutoDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.command(name='gossip', aliases=['fofoca'])
    async def gossip(self, ctx, *, msg: str = "coloque uma fofoca aqui"):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        await ctx.channel.send(f'```Markdown\n [>]: {msg.upper()}```', delete_after=5.0)


def setup(bot):
    bot.add_cog(AutoDelete(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDELETE\033[1;32m foi carregado com sucesso!\33[m')
