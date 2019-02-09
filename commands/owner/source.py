import os

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.translation import t_


class SourceGit(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command()
    async def source(self, ctx, command: str = None):
        source_url = 'https://bitbucket.org/filizardproject/ashley/src/master/'
        if command is None:
            await ctx.send(source_url)
            return

        code_path = command.split('.')
        obj = self.bot
        for cmd in code_path:
            try:
                obj = obj.get_command(cmd)
                if obj is None:
                    await ctx.send(await t_(ctx, 'Não conseguir encontrar esse comando! ', 'guilds') + cmd)
                    return
            except AttributeError:
                await ctx.send((await t_(ctx, '{0.name} esse comando não tem sub-comandos!', 'guilds')).format(obj))
                return

        src = obj.callback.__code__

        if not obj.callback.__module__.startswith('discord'):
            location = os.path.relpath(src.co_filename).replace('\\', '/')
            final_url = '<{}/tree/master/{}#L{}>'.format(source_url, location, src.co_firstlineno)
        else:
            location = obj.callback.__module__.replace('.', '/') + '.py'
            base = 'https://github.com/Rapptz/discord.py'
            final_url = '<{}/blob/master/{}#L{}>'.format(base, location, src.co_firstlineno)

        await ctx.send(final_url)


def setup(bot):
    bot.add_cog(SourceGit(bot))
    print('\033[1;32mO comando \033[1;34mSOURCE\033[1;32m foi carregado com sucesso!\33[m')
