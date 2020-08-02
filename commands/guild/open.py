import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice, randint
from resources.giftmanage import register_gift, open_gift
from resources.img_edit import gift as gt


class OpenClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.legend = {"-": -1, "Comum": 0, "Incomum": 1, "Raro": 2, "Super Raro": 3, "Ultra Raro": 4, "Secret": 5,
                       "Legendary": 6, "Heroic": 7, "Divine": 8, "Sealed": 9, "For Pet": 10}

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='open', aliases=['abrir'])
    async def open(self, ctx):
        """Evento de Caixas..."""
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
            time = randint(60, 600)
            gift = await register_gift(self.bot, time)
            await ctx.send(f"> 🎊 **PARABENS** 🎉 ``VOCÊ GANHOU UM GIFT``\n"
                           f"``USE O COMANDO:`` **ASH GIFT** ``PARA RECEBER SEU PRÊMIO!!``")
            gt(gift, f"{time} SEGUNDOS")
            await ctx.send(file=discord.File('giftcard.png'))
        else:
            await ctx.send(f"<:negate:721581573396496464>│``Esse Servidor não tem presentes disponiveis...``\n"
                           f"**OBS:** se eu for reiniciada, todos os presentes disponiveis sao resetados. Isso é feito"
                           f" por medidas de segurança da minha infraestrutura!")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='gift', aliases=['g'])
    async def gift(self, ctx, *, gift=None):
        """Evento de Caixas..."""
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

        key_item = None
        rarity = None
        if reward['rare'] is not None:
            for k, v in self.bot.items.items():
                if v == reward['rare']:
                    key_item = k
            rarity = list(self.legend.keys())[list(self.legend.values()).index(reward['rare'][3])]

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        update['inventory']['coins'] += reward["coins"]
        if reward['rare'] is not None:
            try:
                update['inventory'][key_item] += 1
            except KeyError:
                update['inventory'][key_item] = 1
        await self.bot.db.update_data(data, update, 'users')
        await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                       f'<:coin:519896843388452864> **{reward["coins"]}** ``fichas!``')

        if reward['rare'] is not None:
            await ctx.send(f"<a:fofo:524950742487007233>│``O ITEM ``{reward['rare'][0]}**{reward['rare'][1]}** "
                           f"``ENCONTRA-SE NO SEU INVENTÁRIO!``\n``ELE TEM O TIER`` **{rarity.upper()}**")

        response = await self.bot.db.add_reward(ctx, reward['items'])
        await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS DO RPG** ✨ {response}')


def setup(bot):
    bot.add_cog(OpenClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mOPEN\033[1;32m foi carregado com sucesso!\33[m')
