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
        self.global_ranking = {"Bronze": 0, "Silver": 0, "Gold": 0}
        self.all_account = 0

    @staticmethod
    def format_num(num):
        a = '{:,.0f}'.format(float(num))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')
        return d

    async def get_all_guilds_atr(self, atr, qnt=0):
        for guild in self.bot.guilds:
            data = await self.bot.db.get_data("guild_id", guild.id, "guilds")
            if data is not None:
                qnt_total = data['data'][atr] + data['treasure'][atr]
                qnt += qnt_total
        return qnt

    async def get_all_list(self, atr):
        t_list = list()
        for guild in self.bot.guilds:
            data = await self.bot.db.get_data("guild_id", guild.id, "guilds")
            if data is not None:
                t_list.append(data['data'][atr])
        return t_list

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='economy', aliases=['economia'])
    async def economy(self, ctx):
        """Comando usado pra ver a quantidade total de dinheiro da ashley
        Use ash economy"""
        self.global_ranking = {"Bronze": 0, "Silver": 0, "Gold": 0}
        self.all_account = 0

        self.money = await self.get_all_guilds_atr('total_money')
        self.gold = await self.get_all_guilds_atr('total_gold')
        self.silver = await self.get_all_guilds_atr('total_silver')
        self.bronze = await self.get_all_guilds_atr('total_bronze')

        for ranking in await self.get_all_list('ranking'):
            self.global_ranking[ranking] += 1
        tot_guild = self.global_ranking['Bronze'] + self.global_ranking['Silver'] + self.global_ranking['Gold']

        for accounts in await self.get_all_list('accounts'):
            self.all_account += accounts

        a = '{:,.2f}'.format(float(self.money))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        msg = f"<:coins:519896825365528596>│ **{ctx.author}** No total há **R$ {d}** de ``ETHERNYAS`` em todos os " \
              f"servidores\n {self.bot.money[2]} **{self.format_num(self.gold)}** | " \
              f"{self.bot.money[1]} **{self.format_num(self.silver)}** | " \
              f"{self.bot.money[0]} **{self.format_num(self.bronze)}**\n\n" \

        if ctx.author.id == 300592580381376513:
            msg += f"Tenho **{self.format_num(tot_guild)}** Guildas\n" \
                   f"**{self.format_num(self.global_ranking['Bronze'])}** ``no ranking Bronze`` | " \
                   f"**{self.format_num(self.global_ranking['Silver'])}** ``no ranking Silver`` | " \
                   f"**{self.format_num(self.global_ranking['Gold'])}** ``no ranking Gold``\n" \
                   f"Tendo ``{self.format_num(self.all_account)}`` Contas no total!"

        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Economy(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mECONOMY\033[1;32m foi carregado com sucesso!\33[m')
