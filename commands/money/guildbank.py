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
    async def treasure(self, ctx, atr: str = ''):
        if atr == 'money':
            self.money = self.get_atr(ctx.guild.id, 'total_money')
            a = '{:,.2f}'.format(float(self.money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            await ctx.send(f'<:coins:519896825365528596>│ No total há **R$ {d}** de ``MONEY`` dentro desse '
                           f'servidor!')
        elif atr == 'gold':
            self.gold = self.get_atr(ctx.guild.id, 'total_gold')
            await ctx.send(f'<:coins:519896825365528596>│ No total há **{self.gold}** de ``GOLD`` dentro desse '
                           f'servidor!')
        elif atr == 'silver':
            self.silver = self.get_atr(ctx.guild.id, 'total_silver')
            await ctx.send(f'<:coins:519896825365528596>│ No total há **{self.silver}** de ``SILVER`` dentro desse '
                           f'servidor!')
        elif atr == 'bronze':
            self.bronze = self.get_atr(ctx.guild.id, 'total_bronze')
            await ctx.send(f'<:coins:519896825365528596>│ No total há **{self.bronze}** de ``BRONZE`` dentro desse '
                           f'servidor!')
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você precisa dizer um atributo, que pode ser:`` \n'
                           '**money**, **gold**, **silver** ou **bronze**')


def setup(bot):
    bot.add_cog(GuildBank(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mGUILDBANK\033[1;32m foi carregado com sucesso!\33[m')
