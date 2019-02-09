import random

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class DadoClass(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='roll', aliases=['rolar'])
    async def roll(self, ctx, dice: str = 'none'):
        if dice == 'none':
            return await ctx.send('<:alert_status:519896811192844288>│`` Você precisa dizer: quantos e qual tipo de '
                                  'dado você quer rolar!``')
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await ctx.send('<:alert_status:519896811192844288>│``Não foi um formado:`` **N**d**N**!')
            return
        global result
        result = ''
        for r in range(rolls):
            result += ''.join(str(random.randint(1, limit))) + ', '
        await ctx.send(f'```{result}```')


def setup(bot):
    bot.add_cog(DadoClass(bot))
    print('\033[1;32mO comando \033[1;34mROLARDADO\033[1;32m foi carregado com sucesso!\33[m')
