import discord
import time as date

from discord.ext import commands
from resources.db import Database
from resources.check import check_it
from datetime import datetime as dt

epoch = dt.utcfromtimestamp(0)


class LoverClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='lover', aliases=['al'])
    async def lover(self, ctx):
        """Esse nem eu sei..."""
        if ctx.guild.id == 519894833783898112:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            if data['config']['provinces'] is not None or ctx.channel.id == 576795574783705104:
                return await ctx.send(f'<:negate:721581573396496464>│``Você está numa provincia ou no inferno! '
                                      f'Retorne usando`` **(ash respawn)** ``para conseguir '
                                      f'pegar meu cargo``')

        try:
            role = discord.utils.find(lambda r: r.name == "</Ash_Lovers>", ctx.guild.roles)
            if role is not None:
                if role not in [r for r in ctx.author.roles]:
                    await ctx.author.add_roles(role)
                    await ctx.send("<:confirmed:721581574461587496>│``VOCE AGORA É UM LOVER MEU!!``")
                else:
                    await ctx.send("🌺``VOCE JA É UM LOVER MEU! MAS OBG POR TANTO AMOR``🌸")
            else:
                await ctx.send(f"<:alert:739251822920728708>│``PEÇA PRA UM ADMINISTRADOR CRIAR UM CARGO CHAMADO:`` "
                               f"**</Ash_Lovers>** ``PARA ESSE SERVIDOR DESFRUTAR DOS MEUS SERVIÇOS DE PING.``")
        except discord.Forbidden:
            await ctx.send("<:negate:721581573396496464>│``NAO TENHO PERMISSÃO DE ADICIONAR CARGOS!``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='unlover', aliases=['ual'])
    async def unlover(self, ctx):
        """Esse nem eu sei..."""
        if ctx.guild.id == 519894833783898112:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            if data['config']['provinces'] is not None or ctx.channel.id == 576795574783705104:
                return await ctx.send(f'<:negate:721581573396496464>│``Você está numa provincia ou no inferno! '
                                      f'Retorne usando`` **(ash respawn)** ``para conseguir '
                                      f'pegar meu cargo``')

        try:
            role = discord.utils.find(lambda r: r.name == "</Ash_Lovers>", ctx.guild.roles)
            if role is not None:
                if role in [r for r in ctx.author.roles]:
                    await ctx.author.remove_roles(role)
                    await ctx.send("<:confirmed:721581574461587496>│``QUE PENA, VOCE NAO ME AMA MAIS?!``")
                else:
                    await ctx.send("<:cry:530735037243719687>│``VOCE NAO TEM MAIS O MEU CARGO, POXA..."
                                   " ME ODEIA TANTO ASSIM?``")
            else:
                await ctx.send(f"<:alert:739251822920728708>│``PEÇA PRA UM ADMINISTRADOR CRIAR UM CARGO CHAMADO:``"
                               f" **</Ash_Lovers>** ``PARA ESSE SERVIDOR DESFRUTAR DOS MEUS SERVIÇOS DE PING.``")
        except discord.Forbidden:
            await ctx.send("<:negate:721581573396496464>│``NAO TENHO PERMISSÃO DE RETIRAR CARGOS!``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='status', aliases=['estado'])
    async def status(self, ctx):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        user = self.bot.user_commands[ctx.author.id]
        guild = self.bot.guilds_commands[ctx.guild.id]

        try:
            time_diff = (dt.utcnow() - epoch).total_seconds() - data["cooldown"]["daily coin"]
            coin = True if time_diff > 86400 else False
        except KeyError:
            coin = True

        try:
            time_diff = (dt.utcnow() - epoch).total_seconds() - data["cooldown"]["daily work"]
            work = True if time_diff > 86400 and guild > 50 and user > 20 else False
        except KeyError:
            work = True if guild > 50 and user > 20 else False

        try:
            time_diff = (dt.utcnow() - epoch).total_seconds() - data["cooldown"]["rec"]['date']
            rec = True if time_diff > 86400 or time_diff < 86400 and data['cooldown']['rec']['cont'] < 6 else False
        except KeyError:
            rec = True

        try:
            time_diff = (dt.utcnow() - epoch).total_seconds() - data["cooldown"]["daily energy"]
            energy = True if time_diff > 86400 else False
        except KeyError:
            energy = True

        try:
            time_diff = (dt.utcnow() - epoch).total_seconds() - data["cooldown"]["guild reward"]
            reward = True if time_diff > 3600 else False
        except KeyError:
            reward = True

        try:
            time_diff = (dt.utcnow() - epoch).total_seconds() - data["cooldown"]["daily vip"]
            vip = True if time_diff > 86400 else False
        except KeyError:
            vip = True

        date_now = dt.today()

        m_last_command = 0
        if data['security']['last_command'] is not None:
            last_command = data['security']['last_command']
            last_verify = date.mktime(date_now.timetuple())
            last_command = date.mktime(last_command.timetuple())
            m_last_command = int(int(last_verify - last_command) / 60)

        m_last_verify = 0
        if data['security']['last_verify'] is not None:
            last_command = data['security']['last_verify']
            last_verify = date.mktime(date_now.timetuple())
            last_command = date.mktime(last_command.timetuple())
            m_last_verify = int(int(last_verify - last_command) / 60)

        m_last_blocked = 0
        if data['security']['last_blocked'] is not None:
            last_command = data['security']['last_blocked']
            last_verify = date.mktime(date_now.timetuple())
            last_command = date.mktime(last_command.timetuple())
            m_last_blocked = int(int(last_verify - last_command) / 60)

        commands_today = data['security']['commands_today']
        last_command = f"Ha {m_last_command} minutos" if data['security']['last_command'] is not None else "Pendente..."
        last_channel = self.bot.get_channel(data['security']['last_channel'])
        last_verify = f"Ha {m_last_verify} minutos" if data['security']['last_verify'] is not None else "Pendente..."
        last_blocked = "Ficha Limpa" if data['security']['last_blocked'] is None else f"Ha {m_last_blocked} minutos"
        wa = data['security']['warns']
        strikes = data['security']['strikes']
        strikes_to_ban = data['security']['strikes_to_ban']
        status = "Liberado" if data['security']['status'] else "Bloqueado"
        blocked = "Liberado" if not data['security']['blocked'] else "Bloqueado"

        msg, n = "", 1
        for k in wa.keys():
            msg += f"**{n}º** {'``Avisado``' if wa[k] else '``Livre``'} **|** "
            n += 1

        s1 = "Comandos que voce usou desde que o bot iniciou."
        s2 = "Comandos que voce usou hoje."
        s3 = "Comandos que essa guilda usou desde que o bot iniciou."

        a1 = data['user']['marrieding']
        a2 = data['config']['playing']
        a3 = data['config']['battle']
        a4 = data['config']['buying']
        a5 = data['config']['provinces']

        embed = discord.Embed(color=self.bot.color)

        embed.add_field(name="-== STATUS DO USUARIO ==-", inline=False,
                        value=f"{'🟢' if a1 else '🔴'} `Casando` Se for verde esta ativado.\n"
                              f"{'🟢' if a2 else '🔴'} `Jogando` Se for verde esta ativado.\n"
                              f"{'🟢' if a3 else '🔴'} `Batalhando` Se for verde esta ativado.\n"
                              f"{'🟢' if a4 else '🔴'} `Comprando` Se for verde esta ativado.\n"
                              f"{'🟢' if a5 is not None else '🔴'} `Provincia` Se for verde esta ativado.")

        embed.add_field(name="-== COMANDOS DIARIOS ==-", inline=False,
                        value=f"{'🟢' if coin else '🔴'} `Coin` Se tiver verde está disponivel pra usar.\n"
                              f"{'🟢' if work else '🔴'} `Work` Se tiver verde está disponivel pra usar.\n"
                              f"{'🟢' if rec else '🔴'} `Rec` Se tiver verde está disponivel pra usar.\n"
                              f"{'🟢' if energy else '🔴'} `Energy` Se tiver verde está disponivel pra usar.\n"
                              f"{'🟢' if reward else '🔴'} `Reward` Se tiver verde está disponivel pra usar.\n"
                              f"{'🟢' if vip else '🔴'} `Vip` Se tiver verde está disponivel pra usar.")

        embed.add_field(name="--== COMANDOS USADOS ==--", inline=False,
                        value=f"``{user}{(' ' * (5 - len(str(user))))}`` {s1}\n"
                              f"``{commands_today}{(' ' * (5 - len(str(commands_today))))}`` {s2}\n"
                              f"``{guild}{(' ' * (5 - len(str(guild))))}`` {s3}")

        embed.add_field(name="--== SECURITY ==--", inline=False,
                        value=f"``{'last_command'.upper()}:`` **{last_command}**\n"
                              f"``{'last_channel'.upper()}:`` **{last_channel}**\n"
                              f"``{'last_verify'.upper()}:`` **{last_verify}**\n"
                              f"``{'last_blocked'.upper()}:`` **{last_blocked}**\n"
                              f"``{'warns'.upper()}:`` {msg}\n"
                              f"``{'strikes_to_block'.upper()}:`` **{strikes} / 10**\n"
                              f"``{'strikes_to_ban'.upper()}:`` **{strikes_to_ban} / 10**\n"
                              f"``{'blocked_today'.upper()}:`` **{status}**\n"
                              f"``{'blocked_to_72h'.upper()}:`` **{blocked}**\n")

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LoverClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mLOVER_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
