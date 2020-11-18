import discord

from random import choice
from asyncio import sleep
from datetime import datetime as dt
from discord.ext import commands
from resources.db import Database
from resources.check import check_it
from resources.img_edit import gift as gt
from resources.giftmanage import register_gift
from resources.utility import convert_item_name

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
    @commands.command(name='reset_user', aliases=['ru'])
    async def reset_user(self, ctx, member: discord.Member = None):
        """Comando usado apelas por DEVS para resetar status bugados..."""
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

        update_member['security']['commands'] = 0
        update_member['security']['commands_today'] = 0
        update_member['security']['strikes'] = 0
        update_member['security']['strikes_to_ban'] = 0
        update_member['security']['last_verify'] = dt.today()
        update_member['security']['last_blocked'] = None
        update_member['security']['status'] = True
        update_member['security']['blocked'] = False
        await self.bot.db.update_data(data_member, update_member, 'users')
        await ctx.send(f"<a:hack:525105069994278913>│🎊 **PARABENS** 🎉 {member.mention} ``TODOS OS SEUS STATUS FORAM"
                       f" RESETADOS COM SUCESSO!`` ✨ **AGORA VC JA PODE UASR O BOT NOVAMENTE.** ✨")

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='create_vip', aliases=['cv'])
    async def create_vip(self, ctx, member: discord.Member = None):
        """Comando usado apelas por DEVS para dar vip para doadores."""
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
        """
        Comando usado apelas por DEVS para criar money para usuarios doadores
        """
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
        """Comando usado apelas por DEVS para criar itens de crafts para doadores"""
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
        """Comando usado apelas por DEVS para criar equipamentos para doadores"""
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
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='set_level', aliases=['sl'])
    async def set_level(self, ctx, member: discord.Member = None, lvl: int = None):
        """Comando usado apelas por DEVS para criar equipamentos para doadores"""
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem!``")
        if lvl is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa dizer um level!``")
        if lvl <= 0 or lvl > 80:
            return await ctx.send("<:alert:739251822920728708>│``level invalido!``")

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

        update_member['rpg']['status']['con'] = 5
        update_member['rpg']['status']['prec'] = 5
        update_member['rpg']['status']['agi'] = 5
        update_member['rpg']['status']['atk'] = 5
        update_member['rpg']['status']['luk'] = 0
        update_member['rpg']['status']['pdh'] = lvl
        update_member['rpg']['xp'] = lvl ** 5
        update_member['rpg']['level'] = lvl

        await self.bot.db.update_data(data_member, update_member, 'users')
        return await ctx.send(f'<a:hack:525105069994278913>│``PARABENS, VC SETOU O LEVEL`` **{lvl}** ``PARA`` '
                              f'**{member.name}** ``COM SUCESSO, ALEM DISSO RESETOU OS PONTOS DE HABILIDADE!``')

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='create_gift', aliases=['cg'])
    async def create_gift(self, ctx, time=None):
        """Comando usado apelas por DEVS para presentar eventos e doadores"""
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

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='create_star', aliases=['cs'])
    async def create_stars(self, ctx, member: discord.Member = None, stars: int = None):
        """Comando para DEVs, adicionar ou retirar estrelas de um usuario"""
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem!``")
        if stars is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa dizer uma quantidade de estrelas!``")
        if stars < 0 or stars > 25:
            return await ctx.send("<:alert:739251822920728708>│``quantidade de estrelas invalidas!``")

        data = await self.bot.db.get_data("user_id", member.id, "users")
        update = data
        if data is None:
            return await ctx.send('<:negate:721581573396496464>│``Usuário não encontrado!``', delete_after=10.0)

        update['user']['stars'] = stars
        await self.bot.db.update_data(data, update, "users")
        await ctx.send(f'<a:hack:525105069994278913>│``PARABENS, VC SETOU`` **{stars}** ``ESTRELAS PARA`` '
                       f'**{member.name}** ``COM SUCESSO!``')


def setup(bot):
    bot.add_cog(UtilityClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUTILITY_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
