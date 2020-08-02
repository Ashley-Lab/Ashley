from asyncio import TimeoutError
from random import choice, randint
from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class GameThinker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extra = ['Melted_Bone', 'Life_Crystal', 'Energy', 'Death_Blow', 'Stone_of_Soul', 'Vital_Force']

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='guess', aliases=['advinhe', 'adivinhe'])
    async def guess(self, ctx):
        """Use ash guess ou ash adivinhe, e tente acertar o numero que ela pensou"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['inventory']['coins'] > 9 and not data['config']['playing']:
            update['config']['playing'] = True
            await self.bot.db.update_data(data, update, 'users')

            number = choice(['0', '1', '2', '3', '4', '5'])
            await ctx.send("<:game:519896830230790157>│``Acabei de pensar em um numero entre`` **0** ``até`` "
                           "**5**, ``tente advinhar qual foi o numero eu pensei:``")

            def check(m):
                return m.author == ctx.author and m.content.isdigit()

            try:
                resposta = await self.bot.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['playing'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito, o número que eu '
                                      'tinha escolhido era`` **{}**.'.format(number))

            update['inventory']['coins'] -= 10
            await self.bot.db.update_data(data, update, 'users')
            reward = ['crystal_fragment_light', 'crystal_fragment_enery', 'crystal_fragment_dark']
            change = randint(15, 100)
            if change == 15:
                reward.append(choice(self.extra))

            if resposta.content in ["0", "1", "2", "3", "4", "5"]:
                if resposta.content == number:
                    answer_ = await self.bot.db.add_money(ctx, change, True)
                    await ctx.send("<:rank:519896825411665930>│``O numero que eu pensei foi`` **{}** "
                                   "``e o número que vc falou foi`` **{}** 🎊 **PARABENS** 🎉 ``você GANHOU:``\n"
                                   "{}".format(number, resposta.content, answer_))
                    if change < 50:
                        response = await self.bot.db.add_reward(ctx, reward)
                        await ctx.send('<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS DO RPG** ✨ '
                                       '{}'.format(response))
                else:
                    await ctx.send("<:negate:721581573396496464>│``O numero que eu pensei foi`` **{}** "
                                   "``e o número que vc falou foi`` **{}**"
                                   " ``Infelizmente Você PERDEU!``".format(number, resposta.content))
            else:
                await ctx.send("<:negate:721581573396496464>│``Você não digitou um número válido!`` "
                               "**Tente Novamente!**")
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['config']['playing'] = False
            await self.bot.db.update_data(data, update, 'users')
        else:
            if data['config']['playing']:
                await ctx.send('<:alert:739251822920728708>│``VOCÊ JÁ ESTÁ JOGANDO!``')
            else:
                await ctx.send('<:alert:739251822920728708>│``VOCÊ PRECISA DE FICHAS PARA JOGAR``')


def setup(bot):
    bot.add_cog(GameThinker(bot))
    print('\033[1;32m( 🔶 ) | O comando de \033[1;34mGAME\033[1;32m foi carregado com sucesso!\33[m')
