import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class LogClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logs = ['msg_delete', 'msg_edit', 'channel_edit_topic', 'channel_edit_name', 'channel_created',
                     'channel_deleted', 'channel_edit', 'role_created', 'role_deleted', 'role_edit', 'guild_update',
                     'member_edit_avatar', 'member_edit_nickname', 'member_voice_entered', 'member_voice_exit',
                     'member_ban', 'member_unBan', 'emoji_update']

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.group(name='logger', aliases=['log'])
    async def logger(self, ctx):
        """Usado pra mostrar os logs
        Use ash logger"""
        if ctx.invoked_subcommand is None:
            data = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            description = '```Markdown\n'
            for log in self.logs:
                description += '[>>]: {}\n<Status: {}>\n\n'.format(log, data['log_config'][log])
            description += '```'
            embed = discord.Embed(
                title='Logs Disponíveis',
                description=description,
                color=self.bot.color
            )
            await ctx.send(embed=embed)

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @logger.command(name='edit', aliases=['e'])
    async def _edit(self, ctx, *, log=None):
        """Usado pra ativar ou desativar logs
        Use ash logger edit <log desejado> e siga as instruções do comando"""
        if log is None:
            return await ctx.send(f'<:negate:721581573396496464>|``Você necessita dizer o log a qual deseja alterar '
                                  f'seu estado!``')
        if log in self.logs:
            data = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            if data['log_config'][log]:
                msg = f'<:confirmed:721581574461587496>|``Você acaba de desativar o log {log}``'
            else:
                msg = f'<:confirmed:721581574461587496>|``Você acaba de ativar o log {log}``'
            update = data
            update['log_config'][log] = not ['log_config'][log]
            await self.bot.db.update_data(data, update, 'guilds')
            await ctx.send(msg)
        return await ctx.send(f"<:negate:721581573396496464>|``O log {log} não está dentro da lista do logs "
                              f"disponiveis!``")

    @logger.error
    async def logger_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<:negate:721581573396496464>│``Você não tem permissão para usar esse comando!``')

    @_edit.error
    async def _edit_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<:negate:721581573396496464>│``Você não tem permissão para usar esse comando!``')


def setup(bot):
    bot.add_cog(LogClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mLOG\033[1;32m foi carregado com sucesso!\33[m')
