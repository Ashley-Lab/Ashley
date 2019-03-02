import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class UserBank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.money = 0
        self.gold = 0
        self.silver = 0
        self.bronze = 0

    def get_atr(self, user_id, atr):
        data = self.bot.db.get_data("user_id", user_id, "users")
        result = data['treasure'][atr]
        if result is not None:
            return result
        else:
            return -1

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='wallet', aliases=['carteira'])
    async def wallet(self, ctx, atr: str = ''):
        if atr == 'money':
            self.money = self.get_atr(ctx.author.id, 'money')
            a = '{:,.2f}'.format(float(self.money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            await ctx.send(f'<:coins:519896825365528596>│ No total você tem **R$ {d}** de ``MONEY`` na sua '
                           f'carteira!')
        elif atr == 'gold':
            self.gold = self.get_atr(ctx.author.id, 'gold')
            await ctx.send(f'<:coins:519896825365528596>│ No total você tem **{self.gold}** de ``GOLD`` na sua '
                           f'carteira!')
        elif atr == 'silver':
            self.silver = self.get_atr(ctx.author.id, 'silver')
            await ctx.send(f'<:coins:519896825365528596>│ No total você tem **{self.silver}** de ``SILVER`` na sua '
                           f'carteira!')
        elif atr == 'bronze':
            self.bronze = self.get_atr(ctx.author.id, 'bronze')
            await ctx.send(f'<:coins:519896825365528596>│ No total você tem **{self.bronze}** de ``BRONZE`` na sua '
                           f'carteira!')
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você precisa dizer um atributo, que pode ser:`` \n'
                           '**money**, **gold**, **silver** ou **bronze**')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='pay', aliases=['pagar'])
    async def pay(self, ctx, member: discord.Member = None, amount: int = None):
        if member is None:
            return await ctx.send("<:oc_status:519896814225457152>│``Você precisa mensionar alguem.``")
        if amount is None:
            return await ctx.send("<:oc_status:519896814225457152>│``Você precisa dizer uma quantia.``")

        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        update_member = data_member
        if data_member is None:
            return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!`` **Você so pode se casar com membros '
                                  'cadastrados!**', delete_after=5.0)


def setup(bot):
    bot.add_cog(UserBank(bot))
    print('\033[1;32mO comando \033[1;34mUSERBANK\033[1;32m foi carregado com sucesso!\33[m')
