import sys
import traceback

from discord.ext import commands
from resources.utility import ERRORS

cor = {
    'clear': '\033[m',
    'cian': '\033[1;36m',
    'roxo': '\033[1;35m',
    'azul': '\033[1;34m',
    'amar': '\033[1;33m',
    'verd': '\033[1;32m',
    'verm': '\033[1;31m',
    'pers': '\033[1;35;47m'
}


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Isso evita que quaisquer comandos com manipuladores locais sejam manipulados aqui em on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # Todos os eventos de erros ignorados, qualquer coisa ignorada retornará e impedirá que algo aconteça.
        if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.UserInputError):
            return

        # Qualquer comando desabilitado retornará uma mensagem de aviso
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'<:negate:520418505993093130>│**{ctx.command}** ``foi desabilitado``')

        # Manipulação de erros voltados para erro de checagem, aqui eu trato de maneira particular erros de Check
        # dentro dos comandos para fins pessoais, ignorando totalmente os padroes comuns.
        if isinstance(error, commands.CheckFailure):
            if error.__str__() == 'The check functions for command register guild failed.':
                return await ctx.send(f"<:negate:520418505993093130>│``VOCÊ NÃO TEM PERMISSÃO PARA USAR ESSE "
                                      f"COMANDO!``")
            elif error.__str__() not in ERRORS:
                return await ctx.send(f"{error}")

        # aqui faço as verificações dos cooldowns dos comandos padroes
        # obs: existem comandos com cooldowns personalizados que nao entram nesse contexto
        if isinstance(error, commands.CommandOnCooldown):

            # exceção criada para os desenvolvedores e testers
            if ctx.author.id in self.bot.staff or ctx.author.id in self.bot.testers:
                return await ctx.reinvoke()

            return await ctx.send(f"<:negate:520418505993093130>│**Aguarde**: `Você deve esperar` **{{:.2f}}** "
                                  f"`segundos` `para mandar outro comando!`".format(error.retry_after),
                                  delete_after=float("{:.2f}".format(error.retry_after)))

        # aqui quando um erro nao é tratado eu registro sua ocorrencia para averiguar sua origem
        channel = self.bot.get_channel(530419409311760394)
        await channel.send(f"<:oc_status:519896814225457152>│``Ocorreu um erro no comando:`` "
                           f"**{ctx.command}**, ``no servidor:`` **{ctx.guild}**, ``no canal:`` "
                           f"**{ctx.channel}** ``com o membro:`` **{ctx.author}**  ``com o id:`` **{ctx.author.id}**")

        # Permite verificar exceções originais geradas e enviadas para CommandInvokeError.
        # Se nada for encontrado. Mantemos a exceção passada para on_command_error.
        error = getattr(error, 'original', error)

        # Todos os outros erros não retornados vêm aqui ... E podemos mostrar o TraceBack padrão.
        # como nao quero print de comando esperando para ser usado, faço a exceção
        if not isinstance(error, commands.CommandOnCooldown):
            # e como nao quero print de comando mal executado pelo usuario faço a outra exceção
            if not isinstance(error, commands.CheckFailure):
                print(f"{cor['verm']}( ❌ ) | error in command: {cor['azul']}{str(ctx.command).upper()}\n"
                      f"{cor['verm']}>> in Guild: "
                      f"{cor['azul']}{ctx.guild} {cor['verm']}- {cor['amar']}ID: {ctx.guild.id}\n"
                      f"{cor['verm']}>> in Channel: "
                      f"{cor['azul']}{ctx.channel} {cor['verm']}- {cor['amar']}ID: {ctx.channel.id}\n"
                      f"{cor['verm']}>> with the Member: "
                      f"{cor['azul']}{ctx.author} {cor['verm']}- {cor['amar']}ID: {ctx.author.id}\n"
                      f"{cor['verm']}>> with error:\n "
                      f"{cor['roxo']}{error}"
                      f"{cor['clear']}\n")
                # o print do traceback é para ver os erros mais detalhadamente
                traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mON_COMMAND_ERROR\033[1;33m foi carregado com sucesso!\33[m')
