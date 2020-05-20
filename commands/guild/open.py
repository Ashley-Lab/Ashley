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
            await ctx.send(f"Esse Servidor não tem caixas disponiveis...")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='gift', aliases=['g'])
    async def gift(self, ctx, *, gift_t=None):
        """Evento de Caixas..."""
        if gift_t is None:
            return await ctx.send("Você precisa gigitar um numero de GIFT!")
        gift = await open_gift(self.bot, gift_t)
        if gift is None:
            return await ctx.send("Você precisa gigitar um numero de GIFT VALIDO!")
        else:
            return await ctx.send("PARABENS VC USOU SEU GIFT COM SUCESSO")


def setup(bot):
    bot.add_cog(OpenClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mOPEN\033[1;32m foi carregado com sucesso!\33[m')
