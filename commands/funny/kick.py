import json
import discord

from random import choice, randint
from discord.ext import commands
from resources.db import Database
from resources.check import check_it

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class KickClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='kick', aliases=['chute'])
    async def kick(self, ctx):
        try:
            kickimg = ['https://media.giphy.com/media/28dP8puMEC1iVGgUtY/giphy.gif',
                       'https://media.giphy.com/media/28DOzqSFj5RbODIeu8/giphy.gif',
                       'https://media.giphy.com/media/1eEDH9ib0DpJ48F1oF/giphy.gif',
                       'https://media.giphy.com/media/mMCXkn2YIFUdGcthIa/giphy.gif',
                       'https://media.giphy.com/media/5kFQ3Dt7dEmlrUduSR/giphy.gif']

            chance = randint(1, 100)

            if ctx.message.mentions[0].id == self.bot.owner_id:
                chance = 1

            if ctx.message.mentions[0].id == self.bot.user.id:
                return await ctx.send('<:negate:520418505993093130>│``Você quer me bater com meu proprio recurso?``')

            if chance <= 10:
                kick = 'https://media.giphy.com/media/C9U5DgKIde7fjOWHf6/giphy.gif'
                text = "Ele(a) iria levar um chute de"
                end = 'Mas ele(a) falhou miseravelmente...'
            elif chance <= 90:
                kick = choice(kickimg)
                text = "Ele(a) levou um chute de"
                end = 'GAME! :regional_indicator_k: :regional_indicator_o:'
            else:
                text = "Ele(a) levou um chutasso de"
                kick = "https://media.giphy.com/media/11sctbYIQPR280/giphy-downsized-large.gif"
                end = 'QUE ACABOU COM ELE(A)! **DEPOIS DESSA VAI PRECISAR IR PRO HOSPITAL!**'

            if ctx.author.id == self.bot.owner_id:
                text = "Ele(a) levou um chute animal de"
                kick = "https://media0dk-a.akamaihd.net/44/99/916f1eb9735b6b70784ca79889e07208.gif"
                end = 'QUE ACABOU COM A VIDA DELE(A)! **DEPOIS DESSA VAI PRECISAR NASCER DE NOVO!**'

            kickemb = discord.Embed(title='Chute :boot:',
                                    description='**{}** {} **{}**! {}'.format(ctx.message.mentions[0].name, text,
                                                                              ctx.author.name, end),
                                    color=color)
            kickemb.set_image(url=kick)
            kickemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=kickemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'chutar!``')


def setup(bot):
    bot.add_cog(KickClass(bot))
    print('\033[1;32mO comando \033[1;34mKICKCLASS\033[1;32m foi carregado com sucesso!\33[m')
