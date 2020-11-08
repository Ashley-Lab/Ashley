from discord.ext import commands
from resources.check import check_it
from resources.db import Database

ON = ['locked', 'block', 'on', 'add']
OFF = ['unlocked', 'unblock', 'off', 'remove']


class ChannelClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.em = self.bot.em

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='channel', aliases=['locker', 'ch', 'lk'])
    async def channel(self, ctx, locker=None):
        """Esse comando bloqueia a ashley de usar comandos em determinados canais, usando o sistema de
        lista branca e lista negra.
        ash channel (troca de listra negra e branca)
        ash channel on/off (libera/bloqueia variando do tipo de lista)"""
        data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_guild = data_guild
        if locker is None:

            update_guild['command_locked']['status'] = not update_guild['command_locked']['status']
            await self.bot.db.update_data(data_guild, update_guild, 'guilds')

            if update_guild['command_locked']['status']:
                await ctx.send(f"{self.em['confirm']}│``BLOQUEADOR DE COMANDOS EM CANAIS ATIVADO COM SUCESSO!``")
            else:
                await ctx.send(f"{self.em['negate']}│``BLOQUEADOR DE COMANDOS EM CANAIS DESATIVADO COM SUCESSO!``")

        elif locker in ON:

            if update_guild['command_locked']['status']:
                if ctx.channel.id not in update_guild['command_locked']['while_list']:
                    update_guild['command_locked']['while_list'].append(ctx.channel.id)
                    await self.bot.db.update_data(data_guild, update_guild, 'guilds')
                    await ctx.send(f"{self.em['confirm']}│``O CANAL`` **{ctx.channel.name}** ``FOI DESBLOQUEADO COM "
                                   f"SUCESSO!``")
                else:
                    await ctx.send(f"{self.em['alert']}│``ESSE CANAL JA ESTA DESBLOQUEADO!``")

            else:
                if ctx.channel.id not in update_guild['command_locked']['black_list']:
                    update_guild['command_locked']['black_list'].append(ctx.channel.id)
                    await self.bot.db.update_data(data_guild, update_guild, 'guilds')
                    await ctx.send(f"{self.em['confirm']}│``O CANAL`` **{ctx.channel.name}**``FOI BLOQUEADO COM "
                                   f"SUCESSO!``")
                else:
                    await ctx.send(f"{self.em['alert']}│``ESSE CANAL JA ESTA BLOQUEADO!``")

        elif locker in OFF:

            if update_guild['command_locked']['status']:
                if ctx.channel.id in update_guild['command_locked']['while_list']:
                    update_guild['command_locked']['while_list'].remove(ctx.channel.id)
                    await self.bot.db.update_data(data_guild, update_guild, 'guilds')
                    await ctx.send(f"{self.em['confirm']}│``O CANAL`` **{ctx.channel.name}**``FOI BLOQUEADO COM "
                                   f"SUCESSO!``")
                else:
                    await ctx.send(f"{self.em['alert']}│``ESSE CANAL JA ESTA BLOQUEADO!``")

            else:
                if ctx.channel.id in update_guild['command_locked']['black_list']:
                    update_guild['command_locked']['black_list'].remove(ctx.channel.id)
                    await self.bot.db.update_data(data_guild, update_guild, 'guilds')
                    await ctx.send(f"{self.em['confirm']}│``O CANAL`` **{ctx.channel.name}** ``FOI DESBLOQUEADO COM "
                                   f"SUCESSO!``")
                else:
                    await ctx.send(f"{self.em['alert']}│``ESSE CANAL JA ESTA DESBLOQUEADO!``")

        else:
            await ctx.send(f"{self.em['negate']}│``OPÇÃO INVALIDA!``")

    @channel.error
    async def _check_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'{self.em["negate"]}│``Você não tem permissão para usar esse comando!``')


def setup(bot):
    bot.add_cog(ChannelClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mCHANNEL_LOCKER\033[1;32m foi carregado com sucesso!\33[m')
