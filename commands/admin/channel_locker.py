from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class DoorClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='locker', aliases=['bloquear'])
    async def locker(self, ctx):
        """Esse nem eu sei..."""
        data_guild = await self.bot.db.get_data("guild_id", message.guild.id, "guilds")
        update_guild = data_guild
        update_guild['command_locked']['status'] = not data_guild['command_locked']['status']
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
        if data_guild['command_locked']['status']:
            await ctx.send("<:on_status:519896814799945728>│``BLOQUEADOR DE COMANDOS EM CANAIS ATIVADO COM SUCESSO!``")
        else:
            await ctx.send("<:negate:520418505993093130>│``BLOQUEADOR DE COMANDOS EM CANAIS DESATIVADO COM SUCESSO!``")

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='locked', aliases=['block'])
    async def locked(self, ctx):
        """Esse nem eu sei..."""
        data_guild = await self.bot.db.get_data("guild_id", message.guild.id, "guilds")
        update_guild = data_guild
        if data_guild['command_locked']['status']:
            update_guild['command_locked']['channel_locked'].append(ctx.channel.id)
        else:
            update_guild['command_locked']['channel_unlocked'].append(ctx.channel.id)
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
        await ctx.send(f"<:on_status:519896814799945728>│``O CANAL`` **{ctx.channel.name}**``FOI BLOQUEADO COM "
                       f"SUCESSO!``")

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='unlocked', aliases=['unblock'])
    async def unlocked(self, ctx):
        """Esse nem eu sei..."""
        data_guild = await self.bot.db.get_data("guild_id", message.guild.id, "guilds")
        update_guild = data_guild
        if not data_guild['command_locked']['status']:
            update_guild['command_locked']['channel_locked'].remove(ctx.channel.id)
        else:
            update_guild['command_locked']['channel_unlocked'].remove(ctx.channel.id)
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
        await ctx.send("<:on_status:519896814799945728>│``O CANAL`` **{ctx.channel.name}**``FOI DESBLOQUEADO COM "
                       f"SUCESSO!``")


def setup(bot):
    bot.add_cog(DoorClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDOOR_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
