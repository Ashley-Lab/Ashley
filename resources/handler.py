import traceback
import sys
from discord.ext import commands
# para mais tipos de erros, consulte as docs:
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=qualified_name#exceptions


@client.listen("on_command_error")
async def error_handler(ctx, error):
    error = getattr(error, 'original', error)
    cmd_name = ctx.message.content.split()[0]  #pegar nome do cmd com prefixo

    if isinstance(error, commands.CommandOnCooldown):
        s = error.retry_after
        s = round(s, 2)
        h, r = divmod(int(s), 3600)
        m, s = divmod(r, 60)
        return await ctx.send(
            f'Você terá que aguardar **{str(h) + "h: " if h != 0 else ""}{str(m) + "m: " if m != 0 else ""}'
            f'{str(s) + "s" if s != 0 else ""}** para usar este comando novamente.')

    if isinstance(error, commands.MissingPermissions):
        perms = "\n".join(error.missing_perms)
        return await ctx.send(f"Você não tem as seguintes permissões:\n{perms}")

    if isinstance(error, commands.BotMissingPermissions):
        perms = "\n".join(error.missing_perms)
        return await ctx.send(f"Não tenho as seguintes permissões:\n{perms}")

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(f"este comando não existe: {cmd_name}")

    if isinstance(error, commands.UserInputError):
        try:
            usage = "\nComo Usar: " + ctx.command.usage.replace('<<command>>', cmd_name)
            # recomendo por <<command>> no usage dos cmds, ex: @client.commands(name="ban",
            # usage="<<command>> [@membro] [motivo]")
        except:
            usage = None
        return await ctx.send(f'Você usou o comando de forma incorreta!{usage if usage else ""}')

    if isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'ban':
            return await ctx.send('usuário não encontrado')

    # Demais erros vão aparecer apenas no console
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
