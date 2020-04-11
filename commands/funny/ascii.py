from pyfiglet import Figlet
from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class AsciiText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.command(name='ascii', aliases=['textao'])
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    async def ascii(self, ctx, *, msg="Digite Algo"):
        f = Figlet(font='slant')
        text = f.renderText(msg)
        await ctx.send("```{}```".format(text))


def setup(bot):
    bot.add_cog(AsciiText(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mASCII\033[1;32m foi carregado com sucesso!\33[m')
