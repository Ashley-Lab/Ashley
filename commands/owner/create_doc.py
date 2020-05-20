import io
import discord
import inspect

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class CreateDoc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def make_doc(self, ctx):
        """apenas desenvolvedores"""
        cogs = {name: {} for name in ctx.bot.cogs.keys()}

        all_commands = []
        for command in ctx.bot.commands:
            all_commands.append(command)
            if isinstance(command, commands.Group):
                all_commands.extend(command.commands)

        for c in all_commands:
            if c.cog_name not in cogs or c.help is None or c.hidden:
                continue
            if c.qualified_name not in cogs[c.cog_name]:
                skip = False
                for ch in c.checks:
                    if 'is_owner' in repr(ch):
                        skip = True
                if skip:
                    continue
                help_ = c.help.replace('\n\n', '\n>')
                cogs[c.cog_name][
                    c.qualified_name] = f'#### {c.qualified_name}\n>**Description:** {help_}\n\n>**Usage:** ' \
                    f'`{ctx.prefix + c.signature}`'

        index = '\n\n# Commands\n\n'
        data = ''

        for cog in sorted(cogs):
            index += '- [{0} Commands](#{1})\n'.format(cog, (cog + ' Commands').replace(' ', '-').lower())
            data += '## {0} Commands\n\n'.format(cog)
            extra = inspect.getdoc(ctx.bot.get_cog(cog))
            if extra is not None:
                data += '#### ***{0}***\n\n'.format(extra)

            for command in sorted(cogs[cog]):
                index += '  - [{0}](#{1})\n'.format(command, command.replace(' ', '-').lower())
                data += cogs[cog][command] + '\n\n'

        fp = io.BytesIO((index.rstrip() + '\n\n' + data.strip()).encode('utf-8'))
        await ctx.author.send(file=discord.File(fp, 'commands.md'))


def setup(bot):
    bot.add_cog(CreateDoc(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mCREATEDOC\033[1;32m foi carregado com sucesso!\33[m')
