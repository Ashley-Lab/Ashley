from random import choice, randint
from asyncio import sleep, TimeoutError
from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from datetime import datetime


class HeadsOrTails(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.extra = ['Melted_Bone', 'Life_Crystal', 'Death_Blow', 'Stone_of_Soul', 'Vital_Force']

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='hot', aliases=['moeda'])
    async def hot(self, ctx):
        """use ash hot ou ash moeda, cara ou coroa, acho que não preciso explicar"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        try:
            if data['inventory']['coins']:
                pass
        except KeyError:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE NÃO TEM FICHA!``')
            return await ctx.send(embed=embed)

        ct = 25
        if data['rpg']['active']:
            date_old = data['rpg']['activated_at']
            date_now = datetime.today()
            days = abs((date_old - date_now).days)
            if days <= 10:
                ct = 5

        if data['inventory']['coins'] > ct and not data['config']['playing']:
            update['config']['playing'] = True
            await self.bot.db.update_data(data, update, 'users')

            await ctx.send("<:game:519896830230790157>│``Vamos brincar de`` **CARA** ``ou`` **COROA**"
                           " ``Escolha uma dessas opções abaixo:`` \n"
                           "**[ 1 ]** - ``Para Cara``\n"
                           "**[ 2 ]** - ``Para Coroa``")
            choice_ = choice(['1', '2'])

            def check(m):
                return m.author == ctx.author and m.content == '1' or m.author == ctx.author and m.content == '2'

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['playing'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` **COMANDO'
                                      ' CANCELADO**')

            update['inventory']['coins'] -= ct
            await self.bot.db.update_data(data, update, 'users')
            reward = ['crystal_fragment_light', 'crystal_fragment_energy', 'crystal_fragment_dark', 'Energy']
            change = randint(5, 100)
            if change == 50:
                reward.append(choice(self.extra))

            if choice_ == '1':
                msg_r = await ctx.send("Cara!")
                await msg_r.add_reaction('🙂')
                await sleep(1)
                if answer.content == choice_:
                    answer_ = await self.bot.db.add_money(ctx, change, True)
                    await ctx.send('<:rank:519896825411665930>│``VOCÊ ACERTOU!`` 🎊 **PARABENS** 🎉 '
                                   '``você GANHOU:``\n {}'.format(answer_))
                    if change < 50:
                        response = await self.bot.db.add_reward(ctx, reward)
                        await ctx.send('<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS DO RPG** ✨ '
                                       '{}'.format(response))
                else:
                    await ctx.send('<:negate:721581573396496464>│``INFELIZMENTE VOCE PERDEU!``')
            if choice_ == '2':
                msg_r = await ctx.send("Coroa!")
                await msg_r.add_reaction('👑')
                await sleep(1)
                if answer.content == choice_:
                    answer_ = await self.bot.db.add_money(ctx, change, True)
                    await ctx.send('<:rank:519896825411665930>│``VOCÊ ACERTOU!`` 🎊 **PARABENS** 🎉 '
                                   '``você GANHOU:``\n {}'.format(answer_))
                    if change < 50:
                        response = await self.bot.db.add_reward(ctx, reward)
                        await ctx.send('<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS DO RPG** ✨ '
                                       '{}'.format(response))
                else:
                    await ctx.send('<:negate:721581573396496464>│``INFELIZMENTE VOCE PERDEU!``')
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['config']['playing'] = False
            await self.bot.db.update_data(data, update, 'users')
        else:
            if data['config']['playing']:
                await ctx.send('<:alert:739251822920728708>│``VOCÊ JÁ ESTÁ JOGANDO!``')
            else:
                await ctx.send(f'<:alert:739251822920728708>│``VOCÊ PRECISA DE + DE {ct} FICHAS PARA JOGAR``\n'
                               f'**OBS:** ``USE O COMANDO`` **ASH SHOP** ``PARA COMPRAR FICHAS!``')


def setup(bot):
    bot.add_cog(HeadsOrTails(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mCARA_OU_COROA\033[1;32m foi carregado com sucesso!\33[m')
