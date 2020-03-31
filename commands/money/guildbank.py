from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class GuildBank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.money = 0
        self.gold = 0
        self.silver = 0
        self.bronze = 0

    @staticmethod
    def format_num(num):
        a = '{:,.0f}'.format(float(num))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')
        return d

    def get_atr(self, guild_id, atr):
        data = self.bot.db.get_data("guild_id", guild_id, "guilds")
        if data is not None:
            return data['data'][atr] + data['treasure'][atr]
        else:
            return -1

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='treasure', aliases=['tesouro'])
    async def treasure(self, ctx):
        self.money = self.get_atr(ctx.guild.id, 'total_money')
        a = '{:,.2f}'.format(float(self.money))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')
        await ctx.send(f'<:coins:519896825365528596>│ No total há **R$ {d}** de ``ETHERNYAS`` dentro desse '
                       f'servidor!')
        self.gold = self.get_atr(ctx.guild.id, 'total_gold')
        await ctx.send(f'{self.bot.money[2]} **{self.format_num(self.gold)}**')
        self.silver = self.get_atr(ctx.guild.id, 'total_silver')
        await ctx.send(f'{self.bot.money[1]} **{self.format_num(self.silver)}**')
        self.bronze = self.get_atr(ctx.guild.id, 'total_bronze')
        await ctx.send(f'{self.bot.money[0]} **{self.format_num(self.bronze)}**')


def setup(bot):
    bot.add_cog(GuildBank(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mGUILDBANK\033[1;32m foi carregado com sucesso!\33[m')
