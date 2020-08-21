import discord
import datetime

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.giftmanage import register_gift
from resources.img_edit import gift as gt

epoch = datetime.datetime.utcfromtimestamp(0)


class UtilityClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='create_gift', aliases=['cg'])
    async def create_gift(self, ctx, time=None):
        """Esse nem eu sei..."""
        if time is None:
            return await ctx.send("<:alert:739251822920728708>│``Digite o tempo de cooldown do gift.``")
        try:
            time = int(time)
        except ValueError:
            return await ctx.send("<:alert:739251822920728708>│``O tempo de cooldown deve ser em numeros.``")

        gift = await register_gift(self.bot, time)
        gt(gift, f"{time} SEGUNDOS")
        await ctx.send(file=discord.File('giftcard.png'))
        await ctx.send(f"> 🎊 **PARABENS** 🎉 ``VOCÊ GANHOU UM GIFT``\n"
                       f"``USE O COMANDO:`` **ASH GIFT** ``PARA RECEBER SEU PRÊMIO!!``")

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
            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - data["cooldown"]["daily coin"]
            coin = True if time_diff > 86400 else False
        except KeyError:
            coin = True

        try:
            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - data["cooldown"]["daily work"]
            work = True if time_diff > 86400 and guild > 50 and user > 20 else False
        except KeyError:
            work = True if guild > 50 and user > 20 else False

        try:
            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - data["cooldown"]["rec"]['date']
            rec = True if time_diff > 86400 or time_diff < 86400 and data['cooldown']['rec']['cont'] < 6 else False
        except KeyError:
            rec = True

        try:
            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - data["cooldown"]["daily energy"]
            energy = True if time_diff > 86400 else False
        except KeyError:
            energy = True

        try:
            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - data["cooldown"]["guild reward"]
            reward = True if time_diff > 3600 else False
        except KeyError:
            reward = True

        try:
            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - data["cooldown"]["daily vip"]
            vip = True if time_diff > 86400 else False
        except KeyError:
            vip = True

        embed = discord.Embed(color=self.bot.color)
        embed.add_field(name="-== STATUS DO USUARIO ==-",
                        value=f"`{'🟢' if data['user']['marrieding'] else '🔴'}` `Casando` Se for verde esta ativado\n"
                              f"`{'🟢' if data['config']['playing'] else '🔴'}` `Jogando` Se for verde esta ativado\n"
                              f"`{'🟢' if data['config']['battle'] else '🔴'}` `Batalhando` Se for verde esta ativado\n"
                              f"`{'🟢' if data['config']['buying'] else '🔴'}` `Comprando` Se for verde esta ativado\n"
                              f"`{'🟢' if data['config']['provinces'] is not None else '🔴'}` `Provincia` "
                              f"Se for verde esta ativado\n\n"
                              f"**-== COMANDOS DIARIOS ==-**\n"
                              f"`{'🟢' if coin else '🔴'}` `Coin` Se tiver verde está disponivel pra usar.\n"
                              f"`{'🟢' if work else '🔴'}` `Work` Se tiver verde está disponivel pra usar.\n"
                              f"`{'🟢' if rec else '🔴'}` `Rec` Se tiver verde está disponivel pra usar.\n"
                              f"`{'🟢' if energy else '🔴'}` `Energy` Se tiver verde está disponivel pra usar.\n"
                              f"`{'🟢' if reward else '🔴'}` `Reward` Se tiver verde está disponivel pra usar.\n"
                              f"`{'🟢' if vip else '🔴'}` `Vip` Se tiver verde está disponivel pra usar.\n\n"
                              f"**--== COMANDOS USADOS ==--**\n"
                              f"**{user}** `Comando que o usuario usou desde que o bot iniciou`\n"
                              f"**{guild}** `Comando que a guilda usou desde que o bot iniciou`")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UtilityClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUTILITY_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
