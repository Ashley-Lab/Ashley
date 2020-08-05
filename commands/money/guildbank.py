import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice, randint


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

        self.st = []

    def status(self):
        for v in self.bot.data_cog.values():
            self.st.append(v)

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

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.group(name='guild', aliases=['guilda', 'servidor'])
    async def guild(self, ctx):
        """Comando usado pra retornar uma lista de todos os subcomandos de guild
                Use ash guild"""
        if ctx.invoked_subcommand is None:
            self.status()
            embed = discord.Embed(color=self.bot.color)
            embed.add_field(name="Guilds Commands:",
                            value=f"{self.st[29]} `guild reward` Receba suas recompenças a cada hora.\n")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, g_vip=True, cooldown=True, time=3600))
    @guild.group(name='reward', aliases=['recompença'])
    async def _reward(self, ctx):
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if ctx.guild.id != data['guild_id']:
            try:
                data_ = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update_ = data_
                del data_['cooldown'][str(ctx.command)]
                await self.bot.db.update_data(data_, update_, 'users')
            except KeyError:
                pass
            return await ctx.send("<:alert:739251822920728708>│``VOCE NAO É REGISTRADO NESSA GUILDA, ESSE COMANDO SO"
                                  " PODE SER EXECUTADO NA SUA GUILDA DE REGISTRO.``")

        amount = 0
        response = '``Caiu pra você:`` \n'

        coins = randint(50, 150)
        energy = randint(25, 50)
        update['inventory']['coins'] += coins
        response += f"**{coins}**: ``{self.bot.items['coins'][1]}``\n"
        update['inventory']['Energy'] += energy
        response += f"**{energy}**: ``{self.bot.items['Energy'][1]}``\n"

        amount += (coins + energy)

        items = {
            'crystal_fragment_light': randint(10, 25),
            'crystal_fragment_enery': randint(10, 25),
            'crystal_fragment_dark': randint(10, 25)
        }

        chance = randint(1, 100)
        k_energy = 0
        if chance < 51:
            k_energy = randint(1, 3)
            response += f"**{k_energy}**: ``{self.bot.items['Crystal_of_Energy'][1]}``\n"

        amount += k_energy

        try:
            update['inventory']['Crystal_of_Energy'] += k_energy
        except KeyError:
            update['inventory']['Crystal_of_Energy'] = k_energy

        for k, v in items.items():
            try:
                update['inventory'][k] += v
                response += f"**{v}**: ``{self.bot.items[k][1]}``\n"
                amount += v
            except KeyError:
                update['inventory'][k] = v
                response += f"**{v}**: ``{self.bot.items[k][1]}``\n"
                amount += v

        amount = amount * 500
        response += '```dê uma olhada no seu inventario com o comando: "ash i"```'

        # DATA DO SERVIDOR ATUAL
        data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_guild = data_guild
        if update_guild['treasure']['total_money'] > amount:
            update_guild['treasure']['total_money'] += amount
            await self.bot.db.update_data(data_guild, update_guild, 'guilds')
        else:
            try:
                data_ = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update_ = data_
                del data_['cooldown'][str(ctx.command)]
                await self.bot.db.update_data(data_, update_, 'users')
            except KeyError:
                pass
            return await ctx.send(f"<:negate:721581573396496464>│``SUA GUILDA NAO TEM DINHEIRO PARA BANCAR ESSE "
                                  f"COMANDO ELE IRIA RETIRAR DO TESOURO`` **{amount}** ``DE ETHERNYAS, MAS NAO"
                                  f"DESANIME USE O COMANDO`` **ASH TESOURO** ``E FIQUE TENTE NOVAMENTE!``")

        await self.bot.db.update_data(data, update, 'users')
        await ctx.send(f"<a:fofo:524950742487007233>│``POR SER REGISTRADO NESSE SERVIDOR VOCÊ GANHOU`` "
                       f"✨ **MUITOS ITENS** ✨\n{response}")


def setup(bot):
    bot.add_cog(GuildBank(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mGUILDBANK\033[1;32m foi carregado com sucesso!\33[m')
