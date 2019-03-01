from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class RegisterAnnounce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='announce', aliases=['anuncio'])
    async def announce(self, ctx, *, announce: str = None):
        if announce is None:
            await ctx.send('<:oc_status:519896814225457152>│``Você precisa colocar um anuncio, para que eu adicione no'
                           ' banco de dados!``')
        else:
            await self.bot.data.add_announcement(ctx, announce)


def setup(bot):
    bot.add_cog(RegisterAnnounce(bot))
    print('\033[1;32mO comando \033[1;34mREGISTER_ANNOUNCE\033[1;32m foi carregado com sucesso!\33[m')
