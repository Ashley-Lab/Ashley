import discord

from random import choice
from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class DanceClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='dance', aliases=['dançar'])
    async def dance(self, ctx):
        """Comando de gifs de dança
        Use ash dance <@usuario a sua escolha>"""
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        try:
            dance_img = ['https://media1.tenor.com/images/56350dfdcd3a5fa4fd66e9e87f9574bb/tenor.gif?itemid=4718162',
                         'https://media1.tenor.com/images/9ee571803fdbea520d723280a6c2c573/tenor.gif?itemid=15054962',
                         'https://media1.tenor.com/images/d119cd830e553054eadc9aa7f05ef888/tenor.gif?itemid=14040294',
                         'https://media1.tenor.com/images/dc24029de47091555c2ecd8ac91d2069/tenor.gif?itemid=13048072',
                         'https://media1.tenor.com/images/42803ed59f21b034f440243557ff2736/tenor.gif?itemid=11049076']
            dance = choice(dance_img)
            dance_embed = discord.Embed(title='Dance <a:dyno:541775159460102167>',
                                        description='**{}** Ele(a) esta dançando com **{}**! Alguem tira foto! EU '
                                                    'SHIPPO! :heart_eyes: '.format(ctx.message.mentions[0].name,
                                                                                   ctx.author.name),
                                        color=self.color)
            dance_embed.set_image(url=dance)
            dance_embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=dance_embed)
        except IndexError:
            await ctx.send('<:negate:721581573396496464>│``Você precisa mencionar um usuário específico para '
                           'dançar!``')


def setup(bot):
    bot.add_cog(DanceClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDANCE\033[1;32m foi carregado com sucesso!\33[m')
