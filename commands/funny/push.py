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
        try:
            pushimg = ['https://media.giphy.com/media/2eqvwrFmCPz4ngW0DC/giphy.gif',
                       'https://media.giphy.com/media/4Q1I8CEIjkQAvZnmPx/giphy.gif',
                       'https://media.giphy.com/media/dB1Ds51ye6smSv09lX/giphy.gif',
                       'https://media.giphy.com/media/vcAXxIghuHWaPainqe/giphy.gif',
                       'https://media.giphy.com/media/65zUCIaDvzhyQdYThW/giphy.gif']

            chance = randint(1, 100)

            if ctx.message.mentions[0].id == self.bot.owner_id:
                chance = 1

            if ctx.message.mentions[0].id == self.bot.user.id:
                return await ctx.send('<:negate:520418505993093130>│``Você quer me bater com meu proprio recurso?``')

            if chance <= 10:
                push = "https://media2.giphy.com/media/bKrynkeJjTKow/giphy.gif"
                text = "Ele(a) iria receber um empurrão de"
                end = 'Mas ele(a) falhou miseravelmente...'
            elif chance <= 90:
                text = "Ele(a) recebeu um empurrão de"
                end = "Acho que doeu... SOLDADO FERIDO! :broken_heart:"
                push = choice(pushimg)
            else:
                text = "Ele(a) recebeu um empurrão daqueles de"
                end = 'QUE ACABOU COM ELE(A)! **DEPOIS DESSA VAI PRECISAR IR PARA O HOSPITAL!**'
                push = 'https://pa1.narvii.com/6968/8ecedea605b7e13d285e20e177739b79149f8498r1-338-200_00.gif'

            if ctx.author.id == self.bot.owner_id:
                text = "Ele(a) recebeu um empurrão animal de"
                end = 'QUE ACABOU COM A VIDA DELE(A)! **DEPOIS DESSA VAI PRECISAR NASCER DE NOVO!**'
                push = link

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
    print('\033[1;32m( * ) | O comando \033[1;34mPUSHCLASS\033[1;32m foi carregado com sucesso!\33[m')
