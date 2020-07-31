import discord

from random import choice, randint
from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class KickClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='kick', aliases=['chute'])
    async def kick(self, ctx):
        """Comando de gifs de chute
        Use ash kick <@usuario a sua escolha>"""
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        try:
            kickimg = ['https://media1.tenor.com/images/cc217519af48fe13bea6004afb36f1f2/tenor.gif?itemid=5738223',
                       'https://media1.tenor.com/images/2427d33c1c97a12b5ed4eda5ca2c63b7/tenor.gif?itemid=16733357',
                       'https://media1.tenor.com/images/fb2a19c9b689123e6254ad9ac6719e96/tenor.gif?itemid=4922649',
                       'https://media1.tenor.com/images/ea2c3b49edf2080e0ef2a2325ddb4381/tenor.gif?itemid=14835708',
                       'https://media1.tenor.com/images/a3fdbd8e26ad73a0fa410c6c04e15714/tenor.gif?itemid=16022961']

            chance = randint(1, 100)

            if ctx.message.mentions[0].id == self.bot.owner_id:
                chance = 1

            if ctx.message.mentions[0].id == self.bot.user.id:
                return await ctx.send('<:negate:520418505993093130>│``Você quer me bater com meu proprio recurso?``')

            if chance <= 10:
                kick = 'https://media1.tenor.com/images/9494639a2ffe5afef9d045d949bf35ee/tenor.gif?itemid=12960265'
                text = "Ele(a) iria levar um chute de"
                end = 'Mas ele(a) falhou miseravelmente...'
            elif chance <= 90:
                kick = choice(kickimg)
                text = "Ele(a) levou um chute de"
                end = 'GAME! :regional_indicator_k: :regional_indicator_o:'
            else:
                text = "Ele(a) levou um chutasso de"
                kick = "https://media1.tenor.com/images/a120a10ab8905a7b74deebe835a3e65a/tenor.gif?itemid=15126208"
                end = 'QUE ACABOU COM ELE(A)! **DEPOIS DESSA VAI PRECISAR IR PRO HOSPITAL!**'

            if ctx.author.id == self.bot.owner_id:
                text = "Ele(a) levou um chute animal de"
                kick = "https://media1.tenor.com/images/51dcdf7d7c418d356e86c20112361b26/tenor.gif?itemid=17370976"
                end = 'QUE ACABOU COM A VIDA DELE(A)! **DEPOIS DESSA VAI PRECISAR NASCER DE NOVO!**'

            kickemb = discord.Embed(title='Chute :boot:',
                                    description='**{}** {} **{}**! {}'.format(ctx.message.mentions[0].name, text,
                                                                              ctx.author.name, end),
                                    color=self.color)
            kickemb.set_image(url=kick)
            kickemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=kickemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'chutar!``')


def setup(bot):
    bot.add_cog(KickClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mKICKCLASS\033[1;32m foi carregado com sucesso!\33[m')
