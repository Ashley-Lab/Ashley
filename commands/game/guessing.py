from asyncio import TimeoutError
from random import choice
from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class GameThinker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='guess', aliases=['advinhe'])
    async def guess(self, ctx):

        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['inventory']['coins'] > 0 and not data['config']['playing']:
            update['config']['playing'] = True
            self.bot.db.update_data(data, update, 'users')

            number = choice(['0', '1', '2', '3', '4', '5'])
            await ctx.send("<:game:519896830230790157>│``Acabei de pensar em um numero entre`` **0** ``até`` "
                           "**5**, ``tente advinhar qual foi o numero eu pensei:``")

            def check(m):
                return m.author == ctx.author and m.content.isdigit()

            try:
                resposta = await self.bot.wait_for('message', check=check, timeout=60.0)
            except TimeoutError:
                update['config']['playing'] = False
                self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito, o número que eu '
                                      'tinha escolhido era`` **{}**.'.format(number))

            update['inventory']['coins'] -= 1
            if resposta.content in ["0", "1", "2", "3", "4", "5"]:
                update['inventory']['coins'] -= 1
                if resposta.content == number:
                    await ctx.send("<:rank:519896825411665930>│``O numero que eu pensei foi`` **{}** "
                                   "``e o número que vc falou foi`` **{}** 🎊 **PARABENS** 🎉 ``você GANHOU:``"
                                   "<:coin:519896843388452864> **15** ``moedas de "
                                   "{}``".format(number, resposta.content, data['user']['ranking']))
                    await self.bot.db.add_money(ctx, 15)
                else:
                    await ctx.send("<:negate:520418505993093130>│``O numero que eu pensei foi`` **{}** "
                                   "``e o número que vc falou foi`` **{}**"
                                   " ``Infelizmente Você PERDEU!``".format(number, resposta.content))
            else:
                await ctx.send("<:oc_status:519896814225457152>│``Você não digitou um número válido!`` "
                               "**Tente Novamente!**")
            update['config']['playing'] = False
            self.bot.db.update_data(data, update, 'users')
        else:
            if data['config']['playing']:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ JÁ ESTÁ JOGANDO!``')
            else:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ PRECISA DE FICHAS PARA JOGAR``')


def setup(bot):
    bot.add_cog(GameThinker(bot))
    print('\033[1;32mO comando de \033[1;34mGAME\033[1;32m foi carregado com sucesso!\33[m')
