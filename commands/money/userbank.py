import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import convert_item_name


class UserBank(commands.Cog):
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
    async def wallet(self, ctx):
        self.money = self.get_atr(ctx.author.id, 'money')
        a = '{:,.2f}'.format(float(self.money))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')
        await ctx.send(f'<:coins:519896825365528596>│ No total você tem **R$ {d}** de ``ETHERNYAS`` na sua '
                       f'carteira!')
        self.gold = self.get_atr(ctx.author.id, 'gold')
        await ctx.send(f'{self.bot.money[2]} **{self.format_num(self.gold)}**')
        self.silver = self.get_atr(ctx.author.id, 'silver')
        await ctx.send(f'{self.bot.money[1]} **{self.format_num(self.silver)}**')
        self.bronze = self.get_atr(ctx.author.id, 'bronze')
        await ctx.send(f'{self.bot.money[0]} **{self.format_num(self.bronze)}**')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='pay', aliases=['pagar'])
    async def pay(self, ctx, member: discord.Member = None, amount: int = None):
        if member is None:
            return await ctx.send("<:oc_status:519896814225457152>│``Você precisa mensionar alguem.``")
        if amount is None:
            return await ctx.send("<:oc_status:519896814225457152>│``Você precisa dizer uma quantia.``")
        if member.id == ctx.author.id:
            return await ctx.send("<:oc_status:519896814225457152>│``Você não pode pagar a si mesmo.``")

        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        update_member = data_member
        if data_member is None:
            return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if data_member['config']['playing']:
            return await ctx.send("<:alert_status:519896811192844288>│``O membro está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        data_guild_native = self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        data_guild_native_member = self.bot.db.get_data("guild_id", data_member['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native_member = data_guild_native_member

        a = '{:,.0f}'.format(float(amount))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        if data_user['treasure']["money"] >= amount:
            update_user['treasure']['money'] -= amount
            update_guild_native['data'][f'total_money'] -= amount
            update_member['treasure']['money'] += amount
            update_guild_native_member['data'][f'total_money'] += amount
            self.bot.db.update_data(data_user, update_user, 'users')
            self.bot.db.update_data(data_member, update_member, 'users')
            self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            self.bot.db.update_data(data_guild_native_member, update_guild_native_member, 'guilds')
            return await ctx.send(f'<:coins:519896825365528596>│``PARABENS, VC PAGOU {d} DE ETHERNYAS '
                                  f'PARA {member.name} COM SUCESSO!``')
        else:
            return await ctx.send(f"<:oc_status:519896814225457152>│``VOCÊ NÃO TEM ESSE VALOR DISPONIVEL DE "
                                  f"{currency.upper()}!``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='give', aliases=['dar'])
    async def give(self, ctx, member: discord.Member = None, amount: int = None, *, item=None):
        if member is None:
            return await ctx.send("<:oc_status:519896814225457152>│``Você precisa mensionar alguem!``")
        if amount is None:
            return await ctx.send("<:oc_status:519896814225457152>│``Você precisa dizer uma quantia!``")
        if member.id == ctx.author.id:
            return await ctx.send("<:oc_status:519896814225457152>│``Você não pode dar um item a si mesmo!``")
        if item is None:
            return await ctx.send("<:oc_status:519896814225457152>│``Você esqueceu de falar o nome do item para dar!``")

        item_key = convert_item_name(item, self.bot.items)
        if item_key is None:
            return await ctx.send("<:oc_status:519896814225457152>│``Item Inválido!``")
        if item_key in self.bot.bl_item:
            return await ctx.send("<:oc_status:519896814225457152>│``Você não pode dar esse tipo de item.``")

        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        update_member = data_member

        if data_member is None:
            return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if data_member['config']['playing']:
            return await ctx.send("<:alert_status:519896811192844288>│``O membro está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        item_name = self.bot.items[item_key][1]

        if item_key in data_user['inventory']:
            if data_user['inventory'][item_key] >= amount:
                update_user['inventory'][item_key] -= amount
                try:
                    update_member['inventory'][item_key] += amount
                except KeyError:
                    update_member['inventory'][item_key] = amount
                self.bot.db.update_data(data_user, update_user, 'users')
                self.bot.db.update_data(data_member, update_member, 'users')
                return await ctx.send(f'<:coins:519896825365528596>│``PARABENS, VC DEU {amount} DE {item_name.upper()} '
                                      f'PARA {member.name} COM SUCESSO!``')
            else:
                return await ctx.send(f"<:oc_status:519896814225457152>│``VOCÊ NÃO TEM ESSA QUANTIDADE DISPONIVEL DE "
                                      f"{item_name.upper()}!``")
        else:
            return await ctx.send("<:oc_status:519896814225457152>│``Você não tem esse item no seu inventario!``")


def setup(bot):
    bot.add_cog(UserBank(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUSERBANK\033[1;32m foi carregado com sucesso!\33[m')
