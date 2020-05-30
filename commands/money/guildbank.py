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

        self.money_ = 0
        self.gold_ = 0
        self.silver_ = 0
        self.bronze_ = 0

    @staticmethod
    def format_num(num):
        a = '{:,.0f}'.format(float(num))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')
        return d

    async def get_atr(self, guild_id, atr, is_true=False):
        data = await self.bot.db.get_data("guild_id", guild_id, "guilds")
        if data is not None:
            if is_true:
                return data['treasure'][atr]
            return data['data'][atr] + data['treasure'][atr]
        else:
            return -1

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='treasure', aliases=['tesouro'])
    async def treasure(self, ctx):
        """Comando usado pra ver a quantia de dinheiro de um server
        Use ash treasure"""
        self.money = await self.get_atr(ctx.guild.id, 'total_money')
        self.gold = await self.get_atr(ctx.guild.id, 'total_gold')
        self.silver = await self.get_atr(ctx.guild.id, 'total_silver')
        self.bronze = await self.get_atr(ctx.guild.id, 'total_bronze')

        self.money_ = await self.get_atr(ctx.guild.id, 'total_money', True)
        self.gold_ = await self.get_atr(ctx.guild.id, 'total_gold', True)
        self.silver_ = await self.get_atr(ctx.guild.id, 'total_silver', True)
        self.bronze_ = await self.get_atr(ctx.guild.id, 'total_bronze', True)

        a = '{:,.2f}'.format(float(self.money))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        a_ = '{:,.2f}'.format(float(self.money_))
        b_ = a_.replace(',', 'v')
        c_ = b_.replace('.', ',')
        d_ = c_.replace('v', '.')

        msg = f"<:coins:519896825365528596>│ **{ctx.author}** No total há **R$ {d}** de ``ETHERNYAS`` dentro desse " \
              f"servidor!\n {self.bot.money[2]} **{self.format_num(self.gold)}** | " \
              f"{self.bot.money[1]} **{self.format_num(self.silver)}** | " \
              f"{self.bot.money[0]} **{self.format_num(self.bronze)}**\n\n" \
              f"``SENDO`` **{d_}** ``DISPONIVEL PARA EMPRESTIMOS`` **CONTENDO:**\n" \
              f"{self.bot.money[2]} **{self.format_num(self.gold_)}** | " \
              f"{self.bot.money[1]} **{self.format_num(self.silver_)}** | " \
              f"{self.bot.money[0]} **{self.format_num(self.bronze_)}**"

        await ctx.send(msg)


def setup(bot):
    bot.add_cog(GuildBank(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mGUILDBANK\033[1;32m foi carregado com sucesso!\33[m')
