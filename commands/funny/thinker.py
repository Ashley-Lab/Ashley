from discord.ext import commands
from random import choice
from resources.db import Database
from resources.check import check_it


class Thinkers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='thinker', aliases=['pensador'])
    async def thinker(self, ctx):
        """comando usado pra enviar uma frase do pensador
        Use ash thinker"""
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        thinker = self.bot.config['thinker']['list']
        answer = choice(thinker)
        await ctx.send("Assim diz o **pensador**: ``{}``".format(answer))


def setup(bot):
    bot.add_cog(Thinkers(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPENSADOR\033[1;32m foi carregado com sucesso!\33[m')
