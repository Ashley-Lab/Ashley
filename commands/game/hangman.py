from discord.ext import commands
from random import choice
from resources.utility import enforcado, forca
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError

erros = {}


class ForceCass(object):
    def __init__(self, bot):
        self.bot = bot
        self.trying = {}

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='hangman', aliases=['forca'])
    async def hangman(self, ctx):

        global resp, erros

        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['inventory']['coins'] > 0 and not data['config']['playing']:
            update['config']['playing'] = True
            self.bot.db.update_data(data, update, 'users')

            self.trying[ctx.author.id] = 0

            def check(m):
                return m.author == ctx.author

            def check_response(m):
                return m.author == ctx.author and m.content.upper() in ['S', 'N']

            lista = list(forca.keys())
            dica = choice(lista)
            palavra = forca[dica]
            digitadas = []
            acertos = [' ', ]
            erros[ctx.author.id] = 0

            while True:
                senha = ""
                for letra in palavra:
                    senha += '{}.'.format(letra.upper()) if letra in acertos else "_."
                await ctx.send('''
`{}`
Dica: **{}**'''.format(senha, dica))

                if senha.count('_') > 3:
                    await ctx.send('<a:seila:525105069637632000>│``Ja quer adivinhar?`` **S/N**')

                    try:
                        resp = await self.bot.wait_for('message', check=check_response, timeout=60.0)
                    except TimeoutError:
                        update['config']['playing'] = False
                        self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                              ' CANCELADO**')

                if senha.count('_') <= 3 or resp.content.upper() == 'S':

                    update['inventory']['coins'] -= 1

                    if senha.count('_') <= 3:
                        await ctx.send('<:pqp:530031187331121152>│``Só faltam 3 ou menos letras, chute a palavra!``')
                    else:
                        await ctx.send('<a:blue:525032762256785409>│``VC ESTÁ DESPERDIÇANDO UMA DAS SUAS 3 CHANGES DE '
                                       'ADVINHAR``')

                    for c in range(self.trying[ctx.author.id], 3):
                        await ctx.send('<a:red:525032764211200002>│``Tentativa {}/3``\n``QUAL A '
                                       'PALAVRA?``'.format(self.trying[ctx.author.id] + 1))

                        if ctx.author.id == self.bot.owner_id:
                            await ctx.send(f"**{palavra}**")

                        try:
                            resp = await self.bot.wait_for('message', check=check, timeout=60.0)
                        except TimeoutError:
                            update['config']['playing'] = False
                            self.bot.db.update_data(data, update, 'users')
                            return await ctx.send(
                                '<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                ' CANCELADO**')

                        if resp.content.lower() == palavra:
                            update['config']['playing'] = False
                            self.bot.db.update_data(data, update, 'users')
                            await self.bot.db.add_money(ctx, 20)
                            return await ctx.send("<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``você GANHOU:``"
                                                  "<:coin:519896843388452864> **20** ``moedas de "
                                                  "{}``".format(data['user']['ranking']))
                        elif self.trying[ctx.author.id] == 2:
                            update['config']['playing'] = False
                            self.bot.db.update_data(data, update, 'users')
                            return await ctx.send("<:oc_status:519896814225457152>│``Infelizmente você perdeu`` "
                                                  "**Tente Novamente!**")
                        elif senha.count('_') > 0:

                            self.trying[ctx.author.id] += 1
                            await ctx.send('<:oc_status:519896814225457152>│``InfelizmenteVocê errou a palavra...``')
                            break

                if senha.count('_') > 3:
                    await ctx.send("\n<:safada:530029764061298699>│``Digite uma letra:``")

                    try:
                        tentativa = await self.bot.wait_for('message', check=check)
                        tentativa = tentativa.content.lower()
                    except TimeoutError:
                        update['config']['playing'] = False
                        self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                              ' CANCELADO**')

                    if tentativa in digitadas:
                        await ctx.send("<:alert_status:519896811192844288>│``Você já tentou esta letra!``")
                        continue
                    else:
                        digitadas += tentativa
                        if tentativa in palavra:
                            acertos += tentativa
                        else:
                            erros[ctx.author.id] += 1
                            await ctx.send("<:oc_status:519896814225457152>│``A palavra não tem essa letra!``")

                    await ctx.send(enforcado[erros[ctx.author.id]])

                    if erros[ctx.author.id] == 6:
                        update['config']['playing'] = False
                        self.bot.db.update_data(data, update, 'users')
                        return await ctx.send(f"<:oc_status:519896814225457152>│``INFORCADO`` **Tente Novamente!**"
                                              f"\n A palavra era **{palavra}**")

        else:
            if data['config']['playing']:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ JÁ ESTÁ JOGANDO!``')
            else:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ PRECISA DE FICHAS PARA JOGAR``')


def setup(bot):
    bot.add_cog(ForceCass(bot))
    print('\033[1;32mO comando de \033[1;34mFORCECLASS\033[1;32m foi carregado com sucesso!\33[m')
