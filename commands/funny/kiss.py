import discord

from random import choice
from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class KissClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='kiss', aliases=['beijo'])
    async def kiss(self, ctx):
        """Comando de gifs de beijo
        Use ash kiss <@usuario a sua escolha>"""
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        try:
            kissimg = ['https://media1.tenor.com/images/ef4a0bcb6e42189dc12ee55e0d479c54/tenor.gif?itemid=12143127',
                       'https://media1.tenor.com/images/b8d0152fbe9ecc061f9ad7ff74533396/tenor.gif?itemid=5372258',
                       'https://media1.tenor.com/images/778d51aca07848160ad9b52e6df37b30/tenor.gif?itemid=16737083',
                       'https://media1.tenor.com/images/693602b39a071644cebebdce7c459142/tenor.gif?itemid=6206552',
                       'https://media1.tenor.com/images/e76e640bbbd4161345f551bb42e6eb13/tenor.gif?itemid=4829336']
            kiss = choice(kissimg)
            kissemb = discord.Embed(title='Beijo :heart:',
                                    description='**{}** Ele(a) recebeu um beijo de **{}**! Que casal fofo! '
                                                ':heart_eyes: '.format(ctx.message.mentions[0].name, ctx.author.name),
                                    color=self.color)
            kissemb.set_image(url=kiss)
            kissemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=kissemb)
        except IndexError:
            await ctx.send('<:negate:721581573396496464>│``Você precisa mencionar um usuário específico para '
                           'beijar!``')


def setup(bot):
    bot.add_cog(KissClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mKISSCLASS\033[1;32m foi carregado com sucesso!\33[m')
