from random import choice, randint
from asyncio import TimeoutError
from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class JoKenPo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='jkp', aliases=['jokenpo'])
    async def jkp(self, ctx):

        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['inventory']['coins'] > 0 and not data['config']['playing']:
            update['config']['playing'] = True
            self.bot.db.update_data(data, update, 'users')

            global player_
            jkp = choice(["Pedra", "Papel", "Tesoura"])
            await ctx.send("<:game:519896830230790157>│``Vamos brincar de`` **JO-KEN-PO!** ``Eu ja escolhi, "
                           "agora é sua vez! Escolha uma dessas opções abaixo:`` \n"
                           "**[ 1 ]** - ``Para Pedra``\n"
                           "**[ 2 ]** - ``Para Papel``\n"
                           "**[ 3 ]** - ``Para Tesoura``")

            def check(m):
                return m.author == ctx.author and m.content == '1' or m.author == ctx.author and m.content == '2' \
                       or m.author == ctx.author and m.content == '3'

            try:
                resposta = await self.bot.wait_for('message', check=check, timeout=60.0)
            except TimeoutError:
                data = self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['playing'] = False
                self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito, eu tinha '
                                      'escolhido:`` **{}**.'.format(jkp))

            update['inventory']['coins'] -= 1
            self.bot.db.update_data(data, update, 'users')

            if resposta.content == "1":
                player_ = "Pedra"
            elif resposta.content == "2":
                player_ = "Papel"
            elif resposta.content == "3":
                player_ = "Tesoura"

            if resposta.content == "1":  # jogador escolheu "Pedra"

                if jkp == "Pedra":
                    await ctx.send("<:game:519896830230790157>│``{}, você escolheu`` **{}** ``e eu "
                                   "escolhi`` **{}, {}** ``empata com`` "
                                   "**{}** ``EMPATAMOS.``".format(ctx.author, player_, jkp, player_, jkp))
                elif jkp == "Tesoura":
                    change = randint(1, 100)
                    if change < 50:
                        await self.bot.db.add_money(ctx, 10)
                        await ctx.send("<:rank:519896825411665930>│``{}, você escolheu`` **{}** ``e eu "
                                       "escolhi`` **{}, {}** ``ganha de`` "
                                       "**{}** 🎊 **PARABENS** 🎉 ``você GANHOU:``"
                                       "<:coin:519896843388452864> **10** ``moedas de "
                                       "{}``".format(ctx.author, player_, jkp, player_, jkp,
                                                     data['user']['ranking']))
                    else:
                        response = await self.bot.db.add_reward(ctx, ['crystal_fragment_light',
                                                                      'crystal_fragment_enery',
                                                                      'crystal_fragment_dark'])
                        await ctx.send('<:rank:519896825411665930>│``VOCÊ ACERTOU!`` 🎊 **PARABENS** 🎉 '
                                       '{}'.format(response))
                elif jkp == "Papel":
                    await ctx.send("<:negate:520418505993093130>│``{}, você escolheu`` **{}** ``e eu "
                                   "escolhi`` **{}, {}** ``perde para`` "
                                   "**{}** ``VOCÊ PERDEU!!``".format(ctx.author, player_, jkp, player_, jkp))

            elif resposta.content == "2":  # jogador escolheu "Papel"

                if jkp == "Pedra":
                    change = randint(1, 100)
                    if change < 50:
                        await self.bot.db.add_money(ctx, 10)
                        await ctx.send("<:rank:519896825411665930>│``{}, você escolheu`` **{}** ``e eu "
                                       "escolhi`` **{}, {}** ``ganha de`` "
                                       "**{}** 🎊 **PARABENS** 🎉 ``você GANHOU:``"
                                       "<:coin:519896843388452864> **10** ``moedas de "
                                       "{}``".format(ctx.author, player_, jkp, player_, jkp,
                                                     data['user']['ranking']))
                    else:
                        response = await self.bot.db.add_reward(ctx, ['crystal_fragment_light',
                                                                      'crystal_fragment_enery',
                                                                      'crystal_fragment_dark'])
                        await ctx.send('<:rank:519896825411665930>│``VOCÊ ACERTOU!`` 🎊 **PARABENS** 🎉 '
                                       '{}'.format(response))
                elif jkp == "Papel":
                    await ctx.send("<:game:519896830230790157>│``{}, você escolheu`` **{}** ``e eu "
                                   "escolhi`` **{}, {}** ``empata com`` "
                                   "**{}** ``EMPATAMOS.``".format(ctx.author, player_, jkp, player_, jkp))
                elif jkp == "Tesoura":
                    await ctx.send("<:negate:520418505993093130>│``{}, você escolheu`` **{}** ``e eu "
                                   "escolhi`` **{}, {}** ``perde para`` "
                                   "**{}** ``VOCÊ PERDEU!!``".format(ctx.author, player_, jkp, player_, jkp))

            elif resposta.content == "3":  # jogador escolheu "Tesoura"

                if jkp == "Pedra":
                    await ctx.send("<:negate:520418505993093130>│``{}, você escolheu`` **{}** ``e eu "
                                   "escolhi`` **{}, {}** ``perde para`` "
                                   "**{}** ``VOCÊ PERDEU!!``".format(ctx.author, player_, jkp, player_, jkp))
                elif jkp == "Papel":
                    change = randint(1, 100)
                    if change < 50:
                        await self.bot.db.add_money(ctx, 10)
                        await ctx.send("<:rank:519896825411665930>│``{}, você escolheu`` **{}** ``e eu "
                                       "escolhi`` **{}, {}** ``ganha de`` "
                                       "**{}** 🎊 **PARABENS** 🎉 ``você GANHOU:``"
                                       "<:coin:519896843388452864> **10** ``moedas de "
                                       "{}``".format(ctx.author, player_, jkp, player_, jkp,
                                                     data['user']['ranking']))
                    else:
                        response = await self.bot.db.add_reward(ctx, ['crystal_fragment_light',
                                                                      'crystal_fragment_enery',
                                                                      'crystal_fragment_dark'])
                        await ctx.send('<:rank:519896825411665930>│``VOCÊ ACERTOU!`` 🎊 **PARABENS** 🎉 '
                                       '{}'.format(response))
                elif jkp == "Tesoura":
                    await ctx.send("<:game:519896830230790157>│``{}, você escolheu`` **{}** ``e eu "
                                   "escolhi`` **{}, {}** ``empata com`` "
                                   "**{}** ``EMPATAMOS.``".format(ctx.author, player_, jkp, player_, jkp))

            data = self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['config']['playing'] = False
            self.bot.db.update_data(data, update, 'users')
        else:
            if data['config']['playing']:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ JÁ ESTÁ JOGANDO!``')
            else:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ PRECISA DE FICHAS PARA JOGAR``')


def setup(bot):
    bot.add_cog(JoKenPo(bot))
    print('\033[1;32mO comando \033[1;34mJOKENPO\033[1;32m foi carregado com sucesso!\33[m')
