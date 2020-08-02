from discord.ext import commands
from resources.check import check_it
from resources.db import Database

ON = ['locked', 'block', 'on']
OFF = ['unlocked', 'unblock', 'off']
EM = ['<:confirmed:721581574461587496>', '<:negate:721581573396496464>']


class ChannelClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='channel', aliases=['locker', 'ch', 'lk'])
    async def channel(self, ctx, locker=None):
        """Esse nem eu sei..."""
        if locker is None:
            data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            update_guild = data_guild
            update_guild['command_locked']['status'] = not data_guild['command_locked']['status']
            await self.bot.db.update_data(data_guild, update_guild, 'guilds')
            if data_guild['command_locked']['status']:
                await ctx.send(f"{EM[0]}│``BLOQUEADOR DE COMANDOS EM CANAIS ATIVADO COM SUCESSO!``")
            else:
                await ctx.send(f"{EM[1]}│``BLOQUEADOR DE COMANDOS EM CANAIS DESATIVADO COM SUCESSO!``")

        elif locker in ON:
            data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            update_guild = data_guild
            if data_guild['command_locked']['status']:
                if ctx.channel.id not in data_guild['command_locked']['while_list']:
                    update_guild['command_locked']['while_list'].append(ctx.channel.id)
                    await ctx.send(f"{EM[0]}│``O CANAL`` **{ctx.channel.name}** ``FOI DESBLOQUEADO COM SUCESSO!``")
                else:
                    return await ctx.send(f"{EM[0]}│``ESSE CANAL JA ESTA DESBLOQUEADO!``")
            else:
                if ctx.channel.id not in data_guild['command_locked']['black_list']:
                    update_guild['command_locked']['black_list'].append(ctx.channel.id)
                    await ctx.send(f"{EM[1]}│``O CANAL`` **{ctx.channel.name}**``FOI BLOQUEADO COM SUCESSO!``")
                else:
                    return await ctx.send(f"{EM[1]}│``ESSE CANAL JA ESTA BLOQUEADO!``")
            await self.bot.db.update_data(data_guild, update_guild, 'guilds')

        elif locker in OFF:
            data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            update_guild = data_guild
            if data_guild['command_locked']['status']:
                if ctx.channel.id in data_guild['command_locked']['while_list']:
                    update_guild['command_locked']['while_list'].remove(ctx.channel.id)
                    await ctx.send(f"{EM[1]}│``O CANAL`` **{ctx.channel.name}**``FOI BLOQUEADO COM SUCESSO!``")
                else:
                    return await ctx.send(f"{EM[1]}│``ESSE CANAL JA ESTA BLOQUEADO!``")
            else:
                if ctx.channel.id in data_guild['command_locked']['black_list']:
                    update_guild['command_locked']['black_list'].remove(ctx.channel.id)
                    await ctx.send(f"{EM[0]}│``O CANAL`` **{ctx.channel.name}** ``FOI DESBLOQUEADO COM SUCESSO!``")
                else:
                    return await ctx.send(f"{EM[0]}│``ESSE CANAL JA ESTA DESBLOQUEADO!``")
            await self.bot.db.update_data(data_guild, update_guild, 'guilds')

        else:
            return await ctx.send("<:negate:721581573396496464>│``OPÇÃO INVALIDA!``")


def setup(bot):
    bot.add_cog(ChannelClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mCHANNEL_LOCKER\033[1;32m foi carregado com sucesso!\33[m')
