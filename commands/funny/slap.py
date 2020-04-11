import discord

from random import choice, randint
from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class SlapClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='slap', aliases=['tapa'])
    async def slap(self, ctx):
        try:
            slapimg = ['https://media1.tenor.com/images/9ea4fb41d066737c0e3f2d626c13f230/tenor.gif?itemid=7355956',
                       'https://media1.tenor.com/images/53d180f129f51575a46b6d3f0f5eeeea/tenor.gif?itemid=5373994',
                       'https://media1.tenor.com/images/153b2f1bfd3c595c920ce60f1553c5f7/tenor.gif?itemid=10936993',
                       'https://media1.tenor.com/images/9391aa8ffd14eace17a3f14b857a3f7d/tenor.gif?itemid=16121405',
                       'https://media1.tenor.com/images/1c986c555ed0b645670596d978c88f6e/tenor.gif?itemid=13142581',
                       'https://media1.tenor.com/images/74db8b0b64e8d539aebebfbb2094ae84/tenor.gif?itemid=15144612']

            chance = randint(1, 100)

            if ctx.message.mentions[0].id == self.bot.owner_id:
                chance = 1

            if ctx.message.mentions[0].id == self.bot.user.id:
                return await ctx.send('<:negate:520418505993093130>│``Você quer me bater com meu proprio recurso?``')

            if chance <= 10:
                slap = "https://i.gifer.com/VF8X.gif"
                text = "Ele(a) iria levar um tapa de"
                end = 'Mas ele(a) falhou miseravelmente...'
            elif chance <= 90:
                text = "Ele(a) levou um tapa de"
                end = "Acho que doeu... SOLDADO FERIDO! :broken_heart:"
                slap = choice(slapimg)
            else:
                text = "Ele(a) levou um tapão de"
                end = 'QUE ACABOU COM A CARA DELE(A)! **DEPOIS DESSA VAI PRECISAR DE OUTRA!**'
                slap = 'https://media1.tenor.com/images/1ba1ea1786f0b03912b1c9138dac707c/tenor.gif?itemid=5738394'

            if ctx.author.id == self.bot.owner_id:
                text = "Ele(a) levou um tapa animal de"
                end = 'QUE ACABOU COM A VIDA DELE(A)! **DEPOIS DESSA VAI PRECISAR NASCER DE NOVO!**'
                slap = 'https://media1.tenor.com/images/b8ff9e6e9cb5a8652f18cc388c4028b0/tenor.gif?itemid=5389796'

            slapemb = discord.Embed(title='Tapa :wave:',
                                    description='**{}** {} **{}**! {}'.format(ctx.message.mentions[0].name, text,
                                                                              ctx.author.name, end),
                                    color=self.color)
            slapemb.set_image(url=slap)
            slapemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=slapemb)
        except IndexError:
            await ctx.send('<:negate:520418505993093130>│``Você precisa mencionar um usuário específico para '
                           'dar um tapa!``')


def setup(bot):
    bot.add_cog(SlapClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mSLAPCLASS\033[1;32m foi carregado com sucesso!\33[m')
