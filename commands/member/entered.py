import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class EnterMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='entered', aliases=['entrou'])
    async def entered(self, ctx, member: discord.Member = None):
        if member is not None:
            await ctx.send('<:check:519896827374338048>│**{0.name}** ``entrou em:`` **{0.joined_at}**'.format(member))
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você precisa mensionar alguem.``')


def setup(bot):
    bot.add_cog(EnterMember(bot))
    print('\033[1;32mO comando \033[1;34mENTER_MEMBER\033[1;32m foi carregado com sucesso!\33[m')
