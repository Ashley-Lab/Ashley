import copy

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import sleep


class RepeatCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True, aliases=['rc'])
    async def repeat_command(self, ctx, times: int, *, command):
        """apenas desenvolvedores"""
        msg = copy.copy(ctx.message)
        msg.content = command
        ctx_ = await self.bot.get_context(msg)
        for i in range(times):
            await self.bot.invoke(ctx_)
            await sleep(7)


def setup(bot):
    bot.add_cog(RepeatCommand(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mREPEAT_COMMAND\033[1;32m foi carregado com sucesso!\33[m')
