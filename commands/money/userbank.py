import discord

from random import choice, randint
from asyncio import sleep, TimeoutError
from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import convert_item_name

coin, cost = 0, 0


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

    async def get_atr(self, user_id, atr):
        data = await self.bot.db.get_data("user_id", user_id, "users")
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
        """Comando usado para verificar quanto dinheiro você tem
        Use ash wallet"""
        self.money = await self.get_atr(ctx.author.id, 'money')
        self.gold = await self.get_atr(ctx.author.id, 'gold')
        self.silver = await self.get_atr(ctx.author.id, 'silver')
        self.bronze = await self.get_atr(ctx.author.id, 'bronze')

        a = '{:,.2f}'.format(float(self.money))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        msg = f"<:coins:519896825365528596>│ **{ctx.author}** No total  você tem **R$ {d}** de ``ETHERNYAS`` na sua " \
              f"carteira!\n {self.bot.money[2]} **{self.format_num(self.gold)}** | " \
              f"{self.bot.money[1]} **{self.format_num(self.silver)}** | " \
              f"{self.bot.money[0]} **{self.format_num(self.bronze)}**"

        await ctx.send(msg)

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

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        update_member = data_member
        if data_member is None:
            return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if data_member['config']['playing']:
            return await ctx.send("<:alert_status:519896811192844288>│``O membro está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        data_guild_native_member = await self.bot.db.get_data("guild_id", data_member['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native_member = data_guild_native_member

        if data_user['treasure']["money"] >= amount:
            update_user['treasure']['money'] -= amount
            update_guild_native['data'][f'total_money'] -= amount
            update_member['treasure']['money'] += amount
            update_guild_native_member['data'][f'total_money'] += amount
            await self.bot.db.update_data(data_user, update_user, 'users')
            await self.bot.db.update_data(data_member, update_member, 'users')
            await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            await self.bot.db.update_data(data_guild_native_member, update_guild_native_member, 'guilds')
            return await ctx.send(f'<:coins:519896825365528596>│``PARABENS, VC PAGOU {self.format_num(amount)} DE '
                                  f'ETHERNYAS PARA {member.name} COM SUCESSO!``')
        else:
            return await ctx.send(f"<:oc_status:519896814225457152>│``VOCÊ NÃO TEM ESSE VALOR DISPONIVEL DE "
                                  f"ETHERNYAS!``")

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

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = await self.bot.db.get_data("user_id", member.id, "users")
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
                await self.bot.db.update_data(data_user, update_user, 'users')
                await self.bot.db.update_data(data_member, update_member, 'users')
                return await ctx.send(f'<:coins:519896825365528596>│``PARABENS, VC DEU {amount} DE {item_name.upper()} '
                                      f'PARA {member.name} COM SUCESSO!``')
            else:
                return await ctx.send(f"<:oc_status:519896814225457152>│``VOCÊ NÃO TEM ESSA QUANTIDADE DISPONIVEL DE "
                                      f"{item_name.upper()}!``")
        else:
            return await ctx.send("<:oc_status:519896814225457152>│``Você não tem esse item no seu inventario!``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='ticket', aliases=['raspadinha', 'rifa'])
    async def ticket(self, ctx):
        """raspadinha da sorte da ashley"""
        global coin, cost
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")

        def check(m):
            return m.author == ctx.author and m.content == '1' or m.author == ctx.author and m.content == '2' or \
                   m.author == ctx.author and m.content == '3'

        await ctx.send("🎫│``Que tipo de`` **TICKET** ``voce deseja comprar?``"
                       " ``Escolha uma dessas opções abaixo:``\n"
                       "**[ 1 ]** - ``Para`` <:etherny_amarelo:691015381296480266> ``Custa:`` **300**\n"
                       "**[ 2 ]** - ``Para`` <:etherny_roxo:691014717761781851> ``Custa:`` **30**\n"
                       "**[ 3 ]** - ``Para`` <:etherny_preto:691016493957251152> ``Custa:`` **3**")

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=60.0)
        except TimeoutError:
            return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                  ' CANCELADO**')

        if int(answer.content) == 1:
            cost = 300
            coin = "bronze"
        if int(answer.content) == 2:
            cost = 30
            coin = "silver"
        if int(answer.content) == 3:
            cost = 3
            coin = "gold"

        if data['treasure'][coin] < cost:
            return await ctx.send('<:negate:520418505993093130>│``Desculpe, você não tem pedras suficientes.`` '
                                  '**COMANDO CANCELADO**')

        # DATA DO MEMBRO
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        update_user['treasure'][coin] -= cost
        await self.bot.db.update_data(data_user, update_user, 'users')

        # DATA NATIVA DO SERVIDOR
        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native['data'][f"total_{coin}"] -= cost
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')

        msg = await ctx.send("<a:loading:520418506567843860>│``RASPANDO TICKET...``")
        await sleep(1)
        await msg.delete()

        awards = self.bot.config['artifacts']
        reward = choice(list(awards.keys()))
        exodia = ["braço_direito", "braço_esquerdo", "perna_direita", "perna_esquerda", "the_one"]
        reliquia = ["anel", "balança", "chave", "colar", "enigma", "olho", "vara"]
        lucky = "EXODIA" if reward in exodia else "RELIQUIA" if reward in reliquia else "ARMADURA"
        a = await ctx.send(f"<:alert_status:519896811192844288>│``SUA SORTE ESTÁ PARA:`` **{lucky}**")

        msg = await ctx.send("<a:loading:520418506567843860>│``SEU PREMIO FOI...``")
        await sleep(3)
        await msg.delete()

        percent = randint(1, 100)
        bonus = awards[reward]["tier"]
        chance = 100 * awards[reward]["chance"] if randint(1, 10) > 3 else 100 * awards[reward]["chance"] * bonus
        if percent <= chance:
            if reward in data["artifacts"]:
                money = randint(6, 18)
                msg = await self.bot.db.add_money(ctx, money, True)
                return await ctx.send(f"> ``VOCE TIROU UM ARTEFATO REPETIDO, "
                                      f"PELO MENOS VOCE GANHOU`` {msg}", delete_after=30.0)
            file = discord.File(awards[reward]["url"], filename="reward.png")
            embed = discord.Embed(title='VOCÊ GANHOU! 🎊 **PARABENS** 🎉', color=self.bot.color)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_image(url="attachment://reward.png")
            await ctx.send(file=file, embed=embed)

            msg = await ctx.send("<a:loading:520418506567843860>│``SALVANDO SEU PREMIO...``")
            await sleep(3)
            await msg.delete()

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update["artifacts"][reward] = awards[reward]
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send(f"<:confirmado:519896822072999937>│``PREMIO SALVO COM SUCESSO!``", delete_after=5.0)
        else:
            money = randint(6, 18)
            msg = await self.bot.db.add_money(ctx, money, True)
            await ctx.send(f"> ``A SORTE NAO ESTAVA COM VOCE, PELO MENOS VOCE GANHOU`` {msg}", delete_after=30.0)
        await a.delete()


def setup(bot):
    bot.add_cog(UserBank(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUSERBANK\033[1;32m foi carregado com sucesso!\33[m')
