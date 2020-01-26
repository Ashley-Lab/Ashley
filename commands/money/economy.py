from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.money = 0
        self.gold = 0
        self.silver = 0
        self.bronze = 0
        self.global_ranking = list()
        self.all_account = list()

    def get_all_guilds_atr(self, atr, qnt=0):
        for guild in self.bot.guilds:
            data = self.bot.db.get_data("guild_id", guild.id, "guilds")
            if data is not None:
                qnt_total = data['data'][atr] + data['treasure'][atr]
                qnt += qnt_total
        return qnt

    def get_all_list(self,  atr, t_list: list):
        for guild in self.bot.guilds:
            guild_id = guild.id
            data = self.bot.db.get_data("guild_id", guild_id, "guilds")
            if data is not None:
                t_list.append(data['data'][atr])
            else:
                t_list = list()
        return t_list

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='economy', aliases=['economia'])
    async def economy(self, ctx, atr: str = ''):
        if atr == 'money':
            self.money = self.get_all_guilds_atr('total_money')
            a = '{:,.2f}'.format(float(self.money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            await ctx.send(f'<:coins:519896825365528596>│ No total há **R$ {d}** de ``MONEY`` geral em '
                           f'todos os servidores')
        elif atr == 'gold':
            self.gold = self.get_all_guilds_atr('total_gold')
            await ctx.send(f'<:coins:519896825365528596>│ No total há **{self.gold}** de ``GOLD`` geral em todos '
                           f'os servidores')
        elif atr == 'silver':
            self.silver = self.get_all_guilds_atr('total_silver')
            await ctx.send(f'<:coins:519896825365528596>│ No total há **{self.silver}** de ``SILVER`` geral em todos '
                           f'os servidores')
        elif atr == 'bronze':
            self.bronze = self.get_all_guilds_atr('total_bronze')
            await ctx.send(f'<:coins:519896825365528596>│ No total há **{self.bronze}** de ``BRONZE`` geral em todos '
                           f'os servidores')
        elif atr == 'ranking':
            self.global_ranking = self.get_all_list('ranking', list())
            await ctx.send(self.global_ranking)
        elif atr == 'account':
            self.all_account = len(self.get_all_list('accounts', list()))
            await ctx.send(self.all_account)
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você precisa dizer um atributo, que pode ser:`` \n'
                           '**money**, **gold**, **silver**, **bronze**, **ranking** ou **account**')


def setup(bot):
    bot.add_cog(Economy(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mECONOMY\033[1;32m foi carregado com sucesso!\33[m')
