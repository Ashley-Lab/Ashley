import io
import discord
import inspect

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import make_doc_blocked

link = "https://discordapp.com/oauth2/authorize?client_id=478977311266570242&scope=bot&permissions=8"
header = f"""
# 🧙‍♀️Ashley🧝‍♀️
<p align="center">
<img height="384" src="https://i.imgur.com/3gxnqkI.png">
</p>

## Sobre Mim
>Meu primeiro projeto no GITHUB - Daniel Amaral (26 Anos) Recife/PE
- Email: danielamaral.f@hotmail.com
- Criado por: Denky#5960🤴

Adicione ela em seu servidor [clicando aqui]({link})!😁

Entre no servidor de suporte [clicando aqui](https://discord.gg/rYT6QrM)!👈

## Grupo de Staffs:

**Núcleo de Programação**

- Denky#5960 (Daniel Amaral)
- Patchouli Knowledge#9732 (Olivia Martins)

**Designers e Ilustradores**

- Patchouli Knowledge#9732 (Olivia Martins)
- zNunshei#8659 (Matheus Vilares)
- 餅(Mochi)#1030 (Momochi)

## Roteiristas

**Scripts da IA**

- Denky#5960 (Daniel Amaral)
- Bublee#9482 (Geórgia Bezerra)
"""


class CreateDoc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='make_doc', aliases=['create_doc', 'cd', 'md'])
    async def make_doc(self, ctx):
        """apenas desenvolvedores"""
        cogs = {name: {} for name in ctx.bot.cogs.keys()}

        all_commands = []
        for command in ctx.bot.commands:
            all_commands.append(command)
            if isinstance(command, commands.Group):
                all_commands.extend(command.commands)

        for c in all_commands:
            if c.cog_name not in cogs or c.help is None:
                continue

            if c.qualified_name in make_doc_blocked:
                continue

            if c.qualified_name not in cogs[c.cog_name]:
                skip = False
                for ch in c.checks:
                    if 'is_owner' in repr(ch):
                        skip = True
                if skip:
                    continue
                help_ = c.help.replace('\n\n', '\n>')
                cogs[c.cog_name][c.qualified_name] = f'#### {c.qualified_name}\n>' \
                                                     f'**Descrição:** {help_}\n\n>' \
                                                     f'**Modo de Uso:** ' \
                                                     f'`{ctx.prefix + str(ctx.command) + " " + c.signature}`'

        index = '\n\n# Commands\n\n'
        data = ''
        index += header

        for cog in sorted(cogs):
            index += '- [{0}](#{1})\n'.format(cog, (cog + ' Commands').replace(' ', '-').lower())
            data += '## {0}\n\n'.format(cog)
            extra = inspect.getdoc(ctx.bot.get_cog(cog))
            if extra is not None:
                data += '#### ***{0}***\n\n'.format(extra)

            for command in sorted(cogs[cog]):
                index += '  - [{0}](#{1})\n'.format(command, command.replace(' ', '-').lower())
                data += cogs[cog][command] + '\n\n'

        fp = io.BytesIO((index.rstrip() + '\n\n' + data.strip()).encode('utf-8'))
        await ctx.author.send(file=discord.File(fp, 'README.md'))


def setup(bot):
    bot.add_cog(CreateDoc(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mCREATEDOC\033[1;32m foi carregado com sucesso!\33[m')
