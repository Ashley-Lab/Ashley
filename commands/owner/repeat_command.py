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
    @commands.command(hidden=True)
    async def repeat_command(self, ctx, times: int, *, command):
        """apenas desenvolvedores"""
        msg = copy.copy(ctx.message)
        msg.content = command
        for i in range(times):
            await self.bot.process_commands(msg)
            await sleep(10)


def setup(bot):
    bot.add_cog(RepeatCommand(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mREPEAT_COMMAND\033[1;32m foi carregado com sucesso!\33[m')
