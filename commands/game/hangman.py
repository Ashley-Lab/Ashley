from discord.ext import commands
from random import choice
from resources.utility import enforcado
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError

errors = {}
resp = None


class ForceCass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trying = {}

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='hangman', aliases=['forca'])
    async def hangman(self, ctx):
        """Use ash hangman ou ash forca pra começar o jogo
        Siga as instruções do comando e tente adivinhar"""
        global resp, errors

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['inventory']['coins'] > 0 and not data['config']['playing']:
            update['config']['playing'] = True
            update['inventory']['coins'] -= 1
            await self.bot.db.update_data(data, update, 'users')

            self.trying[ctx.author.id] = 0

            def check(m):
                return m.author == ctx.author

            def check_letter(m):
                return m.author == ctx.author and len(m.content) == 1

            def check_response(m):
                return m.author == ctx.author and m.content.upper() in ['S', 'N']

            forca = self.bot.config['forca']['list']
            lista = list(forca.keys())
            dica = choice(lista)
            palavra = forca[dica].lower()
            digitadas = []
            acertos = [' ', ]
            errors[ctx.author.id] = 0

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
                        resp = await self.bot.wait_for('message', check=check_response, timeout=30.0)
                    except TimeoutError:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['playing'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` '
                                              '**COMANDO CANCELADO**')

                if senha.count('_') <= 3 or resp.content.upper() == 'S':

                    if senha.count('_') <= 3:
                        await ctx.send('<:pqp:530031187331121152>│``Só faltam 3 ou menos letras, chute a palavra!``')
                    else:
                        await ctx.send('<a:blue:525032762256785409>│``VC ESTÁ DESPERDIÇANDO UMA DAS SUAS 3 CHANCES DE '
                                       'ADIVINHAR``')

                    for c in range(self.trying[ctx.author.id], 3):
                        await ctx.send('<a:red:525032764211200002>│``Tentativa {}/3``\n``QUAL A '
                                       'PALAVRA?``'.format(self.trying[ctx.author.id] + 1))

                        if ctx.author.id == self.bot.owner_id:
                            await ctx.send(f"``OLÁ MESTRE, SUA RESPOSTA É:`` **{palavra.upper()}**")

                        try:
                            resp = await self.bot.wait_for('message', check=check, timeout=30.0)
                        except TimeoutError:
                            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                            update = data
                            update['config']['playing'] = False
                            await self.bot.db.update_data(data, update, 'users')
                            return await ctx.send(
                                '<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                ' CANCELADO**')

                        if resp.content.lower() == palavra.lower():
                            msg = await self.bot.db.add_money(ctx, 20, True)
                            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                            update = data
                            update['config']['playing'] = False
                            await self.bot.db.update_data(data, update, 'users')
                            return await ctx.send("<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``você GANHOU:``\n"
                                                  "{}".format(msg))
                        elif self.trying[ctx.author.id] == 2:
                            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                            update = data
                            update['config']['playing'] = False
                            await self.bot.db.update_data(data, update, 'users')
                            return await ctx.send("<:oc_status:519896814225457152>│``Infelizmente você perdeu`` "
                                                  "**Tente Novamente!**")
                        elif senha.count('_') > 0:

                            self.trying[ctx.author.id] += 1
                            await ctx.send('<:oc_status:519896814225457152>│``InfelizmenteVocê errou a palavra...``')
                            break

                if senha.count('_') > 3:
                    await ctx.send("\n<:safada:530029764061298699>│``Digite uma letra:``")

                    try:
                        tentativa = await self.bot.wait_for('message', check=check_letter, timeout=30.0)
                        tentativa = tentativa.content.lower()
                    except TimeoutError:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['playing'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` '
                                              '**COMANDO CANCELADO**')

                    if tentativa in digitadas:
                        await ctx.send("<:alert_status:519896811192844288>│``Você já tentou esta letra!``")
                        continue
                    else:
                        digitadas += tentativa
                        if tentativa in palavra.lower():
                            acertos += tentativa
                        else:
                            errors[ctx.author.id] += 1
                            await ctx.send("<:oc_status:519896814225457152>│``A palavra não tem essa letra!``")

                    await ctx.send(enforcado[errors[ctx.author.id]])

                    if errors[ctx.author.id] == 6:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['playing'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send(f"<:oc_status:519896814225457152>│``INFORCADO`` **Tente Novamente!**"
                                              f"\n A palavra era **{palavra.upper()}**")

        else:
            if data['config']['playing']:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ JÁ ESTÁ JOGANDO!``')
            else:
                await ctx.send('<:negate:520418505993093130>│``VOCÊ PRECISA DE FICHAS PARA JOGAR``')


def setup(bot):
    bot.add_cog(ForceCass(bot))
    print('\033[1;32m( 🔶 ) | O comando de \033[1;34mFORCECLASS\033[1;32m foi carregado com sucesso!\33[m')
