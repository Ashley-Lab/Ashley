import discord

from random import choice, randint
from discord.ext import commands
from resources.db import Database
from resources.check import check_it


class PunchClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='punch', aliases=['soco', 'murro'])
    async def punch(self, ctx):
        """Comando de gifs de soco
        Use ash punch <@usuario a sua escolha>"""
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        try:
            punchimg = ['https://media1.tenor.com/images/0d0afe2df6c9ff3499a81bf0dab1d27c/tenor.gif?itemid=15580060',
                        'https://media1.tenor.com/images/fb449fd335e73798806747062e2a8af7/tenor.gif?itemid=16733847',
                        'https://media1.tenor.com/images/c621075def6ca41785ef4aaea20cc3a2/tenor.gif?itemid=7679409',
                        'https://media1.tenor.com/images/5511a8309a1719987a27aa7b1ee7da04/tenor.gif?itemid=12303482',
                        'https://media1.tenor.com/images/517f63ce5ffc6426bddd17d7413ebaca/tenor.gif?itemid=5247335',
                        'https://media1.tenor.com/images/b2db2a7fe0b9f68f2869b4e0d11a9490/tenor.gif?itemid=8932977',
                        'https://media1.tenor.com/images/ee3f2a6939a68df9563a7374f131fd96/tenor.gif?itemid=14210784']

            fail = ['https://media1.tenor.com/images/bb51940fa340c5a4e1b3f2d94496a756/tenor.gif?itemid=16700275',
                    'https://media1.tenor.com/images/cff010b188084e1faed2905c0f1634c2/tenor.gif?itemid=10161883',
                    'https://media1.tenor.com/images/e2b232138773393ac3d5acd58936da83/tenor.gif?itemid=5003092']

            chance = randint(1, 100)

            if ctx.message.mentions[0].id == self.bot.owner_id:
                chance = 1

            if ctx.message.mentions[0].id == self.bot.user.id:
                return await ctx.send('<:pqp:530031187331121152>│``Você quer me bater com meu proprio recurso?``')

            if chance <= 10:
                punch = choice(fail)
                text = 'Ele(a) iria levar um soco de'
                end = 'Mas ele(a) falhou miseravelmente...'
            elif chance <= 90:
                punch = choice(punchimg)
                text = 'Ele(a) levou um soco de'
                end = 'GAME! :regional_indicator_k: :regional_indicator_o:'
            else:
                text = 'Ele(a) levou um soco de'
                end = 'QUE ACABOU COM A CARA DELE(A)! **DEPOIS DESSA VAI PRECISAR DE OUTRA!**'
                punch = 'https://thumbs.gfycat.com/PeskyApprehensiveCapeghostfrog-size_restricted.gif'

            if ctx.author.id == self.bot.owner_id:
                text = 'Ele(a) levou um soco de'
                end = 'QUE ACABOU COM A VIDA DELE(A)! **DEPOIS DESSA VAI PRECISAR NASCER DE NOVO!**'
                punch = 'https://i.makeagif.com/media/4-09-2016/E9n3n4.gif'

            punchemb = discord.Embed(title='Soco :boxing_glove: ',
                                     description=f'**{ctx.message.mentions[0].name}** {text} **{ctx.author.name}**! '
                                                 f'{end}',
                                     color=self.color)
            punchemb.set_image(url=punch)
            punchemb.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=punchemb)
        except IndexError:
            await ctx.send('<:negate:721581573396496464>│``Você precisa mencionar um usuário específico para '
                           'socar!``')


def setup(bot):
    bot.add_cog(PunchClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPUNCHCLASS\033[1;32m foi carregado com sucesso!\33[m')
