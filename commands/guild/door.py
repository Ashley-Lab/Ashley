from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class DoorClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='door', aliases=['porta'])
    async def door(self, ctx):
        """Sistema de segurança, controle de entra e sainda de membros (em desenvolvimento)"""
        pass


def setup(bot):
    bot.add_cog(DoorClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDOOR_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
