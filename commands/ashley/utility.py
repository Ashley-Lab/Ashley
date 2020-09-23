import discord
import datetime

import time as date
from random import choice
from asyncio import sleep
from discord.ext import commands
from datetime import datetime as dt

from resources.db import Database
from resources.check import check_it
from resources.img_edit import gift as gt
from resources.giftmanage import register_gift
from resources.utility import convert_item_name


epoch = datetime.datetime.utcfromtimestamp(0)
git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class UtilityClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def format_num(num):
        a = '{:,.0f}'.format(float(num))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')
        return d

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='create_vip', aliases=['cv'])
    async def create_vip(self, ctx, member: discord.Member = None):
        """raspadinha da sorte da ashley"""
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem.``")

        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_member = data_member
        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if data_member['config']['playing']:
            return await ctx.send("<:alert:739251822920728708>│``O membro está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        awards = self.bot.config['artifacts']
        for reward in list(awards.keys()):
            if reward in update_member["artifacts"]:
                try:
                    update_member['inventory'][reward] += 1
                except KeyError:
                    update_member['inventory'][reward] = 1
                await ctx.send(f">>> <a:blue:525032762256785409> ``VOCE TIROU UM ARTEFATO`` "
                               f"**{self.bot.items[reward][1]}** ``REPETIDO, PELO MENOS VOCE GANHOU ESSA "
                               f"RELIQUIA NO SEU INVENTARIO``")
            else:
                file = discord.File(awards[reward]["url"], filename="reward.png")
                embed = discord.Embed(title='VOCÊ GANHOU! 🎊 **PARABENS** 🎉', color=self.bot.color)
                embed.set_author(name=member.name, icon_url=member.avatar_url)
                embed.set_image(url="attachment://reward.png")
                await ctx.send(file=file, embed=embed)
            update_member["artifacts"][reward] = awards[reward]
            if len(update_member['artifacts'].keys()) == 24 and not update_member['rpg']['vip']:
                update_member['rpg']['vip'] = True
            await sleep(1)

        img = choice(git)
        embed = discord.Embed(color=self.bot.color)
        embed.set_image(url=img)
        await self.bot.db.update_data(data_member, update_member, 'users')
        await ctx.send(embed=embed)
        await ctx.send(f"<a:hack:525105069994278913>│🎊 **PARABENS** 🎉 {member.mention} ``COMPLETOU TODOS OS "
                       f"ARTEFATOS!`` ✨ **AGORA VC É VIP NO RPG** ✨")

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='create_money', aliases=['cm'])
    async def create_money(self, ctx, member: discord.Member = None, amount: int = None):
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem.``")
        if amount is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa dizer uma quantia.``")

        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_member = data_member
        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if data_member['config']['playing']:
            return await ctx.send("<:alert:739251822920728708>│``O membro está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        data_guild_native_member = await self.bot.db.get_data("guild_id", data_member['guild_id'], "guilds")
        update_guild_native_member = data_guild_native_member
        update_member['treasure']['money'] += amount
        update_guild_native_member['data'][f'total_money'] += amount
        await self.bot.db.update_data(data_member, update_member, 'users')
        await self.bot.db.update_data(data_guild_native_member, update_guild_native_member, 'guilds')
        return await ctx.send(f'<a:hack:525105069994278913>│``PARABENS, VC CRIOU R$ {self.format_num(amount)},00 '
                              f'DE ETHERNYAS PARA`` **{member.name}** ``COM SUCESSO!``')

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='create_item', aliases=['ci'])
    async def create_item(self, ctx, member: discord.Member = None, amount: int = None, *, item=None):
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem!``")
        if amount is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa dizer uma quantia!``")
        if item is None:
            return await ctx.send("<:alert:739251822920728708>│``Você esqueceu de falar o nome do item para dar!``")

        item_key = convert_item_name(item, self.bot.items)
        if item_key is None:
            return await ctx.send("<:alert:739251822920728708>│``Item Inválido!``")

        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_member = data_member

        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if data_member['config']['playing']:
            return await ctx.send("<:alert:739251822920728708>│``O membro está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        item_name = self.bot.items[item_key][1]
        try:
            update_member['inventory'][item_key] += amount
        except KeyError:
            update_member['inventory'][item_key] = amount
        await self.bot.db.update_data(data_member, update_member, 'users')
        return await ctx.send(f'<a:hack:525105069994278913>│``PARABENS, VC CRIOU`` **{amount}** ``DE`` '
                              f'**{item_name.upper()}** ``PARA`` **{member.name}** ``COM SUCESSO!``')

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='create_equip', aliases=['ce'])
    async def create_equip(self, ctx, member: discord.Member = None, amount: int = None, *, item=None):
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem!``")
        if amount is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa dizer uma quantia!``")
        if item is None:
            return await ctx.send("<:alert:739251822920728708>│``Você esqueceu de falar o nome do item para dar!``")

        equips_list = list()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                equips_list.append((k, v))

        if item not in [i[1]["name"] for i in equips_list]:
            return await ctx.send("<:negate:721581573396496464>│``ESSE ITEM NAO EXISTE...``")

        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_member = data_member

        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)

        if data_member['config']['playing']:
            return await ctx.send("<:alert:739251822920728708>│``O usuario está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        if not data_member['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``O USUARIO DEVE USAR O COMANDO`` **ASH RPG** ``ANTES!``')
            return await ctx.send(embed=embed)

        if data_member['config']['battle']:
            msg = '<:negate:721581573396496464>│``O USUARIO ESTÁ BATALHANDO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        item_key = None
        for name in equips_list:
            if name[1]["name"] == item:
                item_key = name
        if item_key is None:
            return await ctx.send("<:negate:721581573396496464>│``ERRO NO COMANDO VERIFIQUE O CODIGO OU O "
                                  "NOME DO ITEM...``")

        try:
            update_member['rpg']['items'][item_key[0]] += amount
        except KeyError:
            update_member['rpg']['items'][item_key[0]] = amount
        await self.bot.db.update_data(data_member, update_member, 'users')
        return await ctx.send(f'<a:hack:525105069994278913>│``PARABENS, VC CRIOU`` **{amount}** ``DE`` '
                              f'**{item_key[1]["name"].upper()}** ``PARA`` **{member.name}** ``COM SUCESSO!``')

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
    bot.add_cog(UtilityClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUTILITY_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
