from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice, randint
from resources.giftmanage import register_gift, open_gift


class OpenClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='open', aliases=['abrir'])
    async def open(self, ctx):
        """Evento de Caixas..."""
        if ctx.guild.id in self.bot.box:
            BOX = choice(self.bot.box[ctx.guild.id]['boxes'])
            I_BOX = self.bot.box[ctx.guild.id]['boxes'].index(BOX)
            del(self.bot.box[ctx.guild.id]['boxes'][I_BOX])
            self.bot.box[ctx.guild.id]['quant'] -= 1
            time = randint(60, 600)
            GIFT = await register_gift(self.bot, time)
            await ctx.send(f"Caixa aberta com sucesso! **COMANDO EM FASE TE TESTES**\n"
                           f"VOCÊ GANHOU UM GIFT: {GIFT}\n"
                           f"COM O TEMPO DE ATIVAÇÃO DE: {time} SEGUNDOS!")
        else:
            await ctx.send(f"<:negate:520418505993093130>│``Esse Servidor não tem caixas disponiveis...``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='gift', aliases=['g'])
    async def gift(self, ctx, *, gift=None):
        """Evento de Caixas..."""
        if gift is None:
            return await ctx.send("<:negate:520418505993093130>│``Você precisa gigitar um numero de GIFT!``")

        reward = await open_gift(self.bot, gift)

        if reward is None:
            return await ctx.send("<:negate:520418505993093130>│``Você precisa gigitar um numero de GIFT VALIDO!``")
        else:
            await ctx.send("🎊 **PARABENS** 🎉 ``VC USOU SEU GIFT COM SUCESSO!!``")

            answer_ = await self.bot.db.add_money(ctx, reward['money'], True)
            await ctx.send(f'<:rank:519896825411665930>│``VOCÊ GANHOU!`` 🎊 **PARABENS** 🎉 '
                           f'``você GANHOU:``\n {answer_}')

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['inventory']['coins'] += reward["coins"]
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                           f'<:coin:519896843388452864> **{reward["coins"]}** ``fichas!``')

            response = await self.bot.db.add_reward(ctx, reward['list'])
            await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS DO RPG** ✨ {response}')


def setup(bot):
    bot.add_cog(OpenClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mOPEN\033[1;32m foi carregado com sucesso!\33[m')
