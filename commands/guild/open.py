import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice, randint
from resources.giftmanage import register_gift, open_gift, open_chest
from resources.img_edit import gift as gt


class OpenClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.legend = {"-": -1, "Comum": 0, "Incomum": 1, "Raro": 2, "Super Raro": 3, "Ultra Raro": 4, "Secret": 5,
                       "Legendary": 6, "Heroic": 7, "Divine": 8, "Sealed": 9, "For Pet": 10}

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='open', aliases=['abrir'])
    async def open(self, ctx):
        """Abra um presente para liberar seu giftcard."""
        if ctx.guild.id in self.bot.box:
            try:
                BOX = choice(self.bot.box[ctx.guild.id]['boxes'])
            except IndexError:
                return await ctx.send(f"<:negate:721581573396496464>│``Esse Servidor não tem presentes disponiveis!``\n"
                                      f"``TODOS OS PRESENTES FORAM UTILIZADOS, AGUARDE UM NOVO PRESENTE DROPAR E FIQUE "
                                      f"ATENTO!``")
            I_BOX = self.bot.box[ctx.guild.id]['boxes'].index(BOX)
            del (self.bot.box[ctx.guild.id]['boxes'][I_BOX])
            self.bot.box[ctx.guild.id]['quant'] -= 1
            time = randint(90, 600)
            gift = await register_gift(self.bot, time)

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")

            if not data['rpg']['vip']:
                await ctx.send(f"> 🎊 **PARABENS** 🎉 ``VOCÊ GANHOU UM GIFT``\n"
                               f"``USE O COMANDO:`` **ASH GIFT** ``PARA RECEBER SEU PRÊMIO!!``")
                gt(gift, f"{time} SEGUNDOS")
                if discord.File('giftcard.png') is None:
                    return await ctx.send("<:negate:721581573396496464>│``ERRO!``")
                await ctx.send(file=discord.File('giftcard.png'))
            else:
                if not data['security']['status']:
                    return await ctx.send("<:negate:721581573396496464>│'``USUARIO DE MACRO / OU USANDO COMANDOS "
                                          "RAPIDO DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**'")

                reward = await open_gift(self.bot, gift.upper())
                await ctx.send("🎊 **PARABENS** 🎉 ``VC USOU SEU GIFT COM SUCESSO!!``")
                answer_ = await self.bot.db.add_money(ctx, reward['money'], True)
                await ctx.send(f'<:rank:519896825411665930>│``você GANHOU:``\n {answer_}')

                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['inventory']['coins'] += reward["coins"]
                await self.bot.db.update_data(data, update, 'users')
                await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                               f'<:coin:546019942936608778> **{reward["coins"]}** ``fichas!``')

                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                response = '``Caiu pra você:`` \n'
                for item in reward['items']:
                    amount = randint(10, 25)
                    try:
                        update['inventory'][item] += amount
                    except KeyError:
                        update['inventory'][item] = amount
                    response += f"{self.bot.items[item][0]} ``{amount}`` ``{self.bot.items[item][1]}``\n"
                response += '```dê uma olhada no seu inventario com o comando: "ash i"```'
                await self.bot.db.update_data(data, update, 'users')
                await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ GANHOU`` ✨ **ITENS DO RPG** ✨ {response}')

                if reward['rare'] is not None:
                    response = await self.bot.db.add_reward(ctx, reward['rare'])
                    await ctx.send(f'<a:caralho:525105064873033764>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS RAROS** ✨ '
                                   f'{response}')

        else:
            await ctx.send(f"<:negate:721581573396496464>│``Esse Servidor não tem presentes disponiveis...``\n"
                           f"**OBS:** se eu for reiniciada, todos os presentes disponiveis sao resetados. Isso é feito"
                           f" por medidas de segurança da minha infraestrutura!")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='gift', aliases=['g'])
    async def gift(self, ctx, *, gift=None):
        """Esse comando libera premios do giftcard que voce abriu no comando 'ash open'"""
        if gift is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa digitar um numero de GIFT!``")

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        if not data_user['security']['status']:
            return await ctx.send("<:negate:721581573396496464>│'``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO "
                                  "DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**'")

        reward = await open_gift(self.bot, gift.upper())
        if reward is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa digitar um numero de GIFT VALIDO!``")

        if not reward['validity']:
            return await ctx.send("<:negate:721581573396496464>│``ESSE GIFT ESTÁ COM O TEMPO EXPIRADO!``")

        await ctx.send("🎊 **PARABENS** 🎉 ``VC USOU SEU GIFT COM SUCESSO!!``")
        answer_ = await self.bot.db.add_money(ctx, reward['money'], True)
        await ctx.send(f'<:rank:519896825411665930>│``você GANHOU:``\n {answer_}')

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        update['inventory']['coins'] += reward["coins"]
        await self.bot.db.update_data(data, update, 'users')
        await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                       f'<:coin:546019942936608778> **{reward["coins"]}** ``fichas!``')

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        response = '``Caiu pra você:`` \n'
        for item in reward['items']:
            amount = randint(10, 25)
            try:
                update['inventory'][item] += amount
            except KeyError:
                update['inventory'][item] = amount
            response += f"{self.bot.items[item][0]} ``{amount}`` ``{self.bot.items[item][1]}``\n"
        response += '```dê uma olhada no seu inventario com o comando: "ash i"```'
        await self.bot.db.update_data(data, update, 'users')
        await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ GANHOU`` ✨ **ITENS DO RPG** ✨ {response}')

        if reward['rare'] is not None:
            response = await self.bot.db.add_reward(ctx, reward['rare'])
            await ctx.send(f'<a:caralho:525105064873033764>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS RAROS** ✨ {response}')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='event', aliases=['evento'])
    async def event(self, ctx):
        """Abra um presente para liberar seu giftcard."""
        if not self.bot.event_special:
            return await ctx.send(f"<:negate:721581573396496464>│``ATUALMENTE NAO TEM NENHUM EVENTO ESPECIAL!``")

        if ctx.author.id in self.bot.chests_users:
            try:
                CHEST = choice(self.bot.chests_users[ctx.author.id]['chests'])
            except IndexError:
                return await ctx.send(f"<:negate:721581573396496464>│``Você nao tem mais baus disponiveis...``\n"
                                      f"``TODOS OS BAUS FORAM UTILIZADOS, DROPE UM NOVO BÁU UTILIZANDO O MAXIMO DE "
                                      f"COMANDOS DIFERENTES POSSIVEIS!``")

            I_CHEST = self.bot.chests_users[ctx.author.id]['chests'].index(CHEST)
            del (self.bot.chests_users[ctx.author.id]['chests'][I_CHEST])
            self.bot.chests_users[ctx.author.id]['quant'] -= 1
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            if not data['security']['status']:
                return await ctx.send("<:negate:721581573396496464>│'``USUARIO DE MACRO / OU USANDO COMANDOS "
                                      "RAPIDO DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**'")

            reward = open_chest(self.bot.chests_l[str(CHEST)])
            await ctx.send("🎊 **PARABENS** 🎉 ``VC ABRIU O SEU BAU COM SUCESSO!!``")
            answer_ = await self.bot.db.add_money(ctx, reward['money'], True)
            await ctx.send(f'<:rank:519896825411665930>│``você GANHOU:``\n {answer_}')

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['inventory']['coins'] += reward["coins"]
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                           f'<:coin:546019942936608778> **{reward["coins"]}** ``fichas!``')

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['inventory']['Energy'] += reward["Energy"]
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                           f'<:energy:546019943603503114> **{reward["Energy"]}** ``energias!``')

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            response = '``Caiu pra você:`` \n'
            for item in reward['items']:
                amount = randint(1, 5)
                try:
                    update['inventory'][item] += amount
                except KeyError:
                    update['inventory'][item] = amount
                response += f"{self.bot.items[item][0]} ``{amount}`` ``{self.bot.items[item][1]}``\n"
            response += '```dê uma olhada no seu inventario com o comando: "ash i"```'
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ GANHOU`` ✨ **ITENS DO RPG** ✨ {response}')

            if reward['relic'] is not None:
                response = await self.bot.db.add_reward(ctx, reward['relic'])
                await ctx.send(f'<a:caralho:525105064873033764>│``VOCÊ TAMBEM GANHOU`` ✨ **O ITEM SECRETO** ✨ '
                               f'{response}')

            relics = ["WrathofNatureCapsule", "UltimateSpiritCapsule", "SuddenDeathCapsule", "InnerPeacesCapsule",
                      "EternalWinterCapsule", "EssenceofAsuraCapsule", "DivineCalderaCapsule", "DemoniacEssenceCapsule"]
            cr = 0
            for relic in relics:
                if relic in update['inventory'].keys():
                    cr += 1
            if cr == 8:
                channel = self.bot.get_channel(774400939293409290)
                if channel is not None:
                    await channel.send(f'<a:caralho:525105064873033764>│``{ctx.author}`` ✨ **GANHOU O EVENTO** ✨')

        else:
            await ctx.send(f"<:negate:721581573396496464>│``Você nao tem mais baus disponiveis...``\n"
                           f"**OBS:** se eu for reiniciada, todos os baus disponiveis sao resetados. Isso é feito"
                           f" por medidas de segurança da minha infraestrutura!")


def setup(bot):
    bot.add_cog(OpenClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mOPEN\033[1;32m foi carregado com sucesso!\33[m')
