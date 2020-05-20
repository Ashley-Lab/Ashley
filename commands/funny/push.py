import discord

from random import choice, randint
from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class PushClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='push', aliases=['empurrao'])
    async def push(self, ctx):
        """Comando de gifs de empurrão
        Use ash push <@usuario a sua escolha>"""
        try:
            pushimg = ['https://media1.tenor.com/images/a8e2bfdbf0d3e4fb8c52fab9e4cb249e/tenor.gif?itemid=16131433',
                       'https://media1.tenor.com/images/b7f788f5b4c5cf79df1bbe9a421e4826/tenor.gif?itemid=5634617',
                       'https://media1.tenor.com/images/afec3a41fea91183852f5447edfaea68/tenor.gif?itemid=15996103',
                       'https://media1.tenor.com/images/281ed25c27493bdde34109c98c4a553e/tenor.gif?itemid=16546201',
                       'https://pa1.narvii.com/6968/8ecedea605b7e13d285e20e177739b79149f8498r1-338-200_00.gif']

            chance = randint(1, 100)

            if ctx.message.mentions[0].id == self.bot.owner_id:
                chance = 1

            if ctx.message.mentions[0].id == self.bot.user.id:
                return await ctx.send('<:negate:520418505993093130>│``Você quer me bater com meu proprio recurso?``')

            if chance <= 10:
                push = "https://media1.tenor.com/images/9494639a2ffe5afef9d045d949bf35ee/tenor.gif?itemid=12960265"
                text = "Ele(a) iria receber um empurrão de"
                end = 'Mas ele(a) falhou miseravelmente...'
            elif chance <= 90:
                text = "Ele(a) recebeu um empurrão de"
                end = "Acho que doeu... SOLDADO FERIDO! :broken_heart:"
                push = choice(pushimg)
            else:
                text = "Ele(a) recebeu um empurrão daqueles de"
                end = 'QUE ACABOU COM ELE(A)! **DEPOIS DESSA VAI PRECISAR IR PARA O HOSPITAL!**'
                push = 'https://media1.tenor.com/images/2eae03fe2318d2faeda08364834f69b7/tenor.gif?itemid=15113203'

            if ctx.author.id == self.bot.owner_id:
                text = "Ele(a) recebeu um empurrão animal de"
                end = 'QUE ACABOU COM A VIDA DELE(A)! **DEPOIS DESSA VAI PRECISAR NASCER DE NOVO!**'
                push = 'https://media1.tenor.com/images/62ef360ace36ba9e60a11e6dec2edb59/tenor.gif?itemid=5416860'

            pushemb = discord.Embed(title='Empurrão :raised_hands:',
                                    description='**{}** {} **{}**! {}'.format(ctx.message.mentions[0].name, text,
                                                                              ctx.author.name, end),
                                    color=self.color)
            pushemb.set_image(url=push)
            pushemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=pushemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'empurrar!``')


def setup(bot):
    bot.add_cog(PushClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPUSHCLASS\033[1;32m foi carregado com sucesso!\33[m')
