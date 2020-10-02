import discord

from random import choice, randint
from asyncio import sleep, TimeoutError
from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import convert_item_name

coin, cost, plus = 0, 0, 0
git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class UserBank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.money = 0
        self.gold = 0
        self.silver = 0
        self.bronze = 0

        self.items = {
            "Fichas": 65,

            "Crystal Fragment Light": 154,
            "Crystal Fragment Energy": 167,
            "Crystal Fragment Dark": 178,

            "Energy": 200,
            "Melted Bone": 212,
            "Life Crystal": 211,
            "Death Blow": 221,
            "Stone of Soul": 222,
            "Vital Force": 213,

            "Stone Crystal White": 312,
            "Stone Crystal Red": 345,
            "Stone Crystal Green": 354,
            "Stone Crystal Blue": 364,
            "Stone Crystal Yellow": 365,

            "Dust Wind": 432,
            "Dust Water": 412,
            "Dust Light": 468,
            "Dust Fire": 454,
            "Dust Earth": 444,
            "Dust Dark": 468,

            "Stone Wind": 563,
            "Stone Water": 543,
            "Stone Light": 525,
            "Stone Fire": 512,
            "Stone Earth": 532,
            "Stone Dark": 587,

        }

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
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='shop', aliases=['buy', 'comprar', 'loja'])
    async def shop(self, ctx, quant=None, *, item=None):
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if item is None or quant is None:
            msg = "```Markdown\n"
            for k, v in self.items.items():
                msg += f"[>>]: {k.upper()}\n<1 UND = {v} ETHERNYAS>\n\n"
            msg += "```"
            return await ctx.send(f"<:alert:739251822920728708>│``ITENS DISPONIVEIS PARA COMPRA:``\n{msg}\n"
                                  f"**EXEMPLO:** ``USE`` **ASH SHOP 50 FICHAS** ``PARA COMPRAR 50 FICHAS!``")

        name = None
        for key in self.items.keys():
            if key.lower() == item.lower():
                name = key

        if name is None:
            return await ctx.send("<:alert:739251822920728708>│``ESSE ITEM NAO EXISTE OU NAO ESTA DISPONIVEL!``")

        if update['treasure']['money'] < self.items[name] * int(quant):
            return await ctx.send("<:alert:739251822920728708>│``VOCE NAO TEM ETHERNYAS SUFICIENTES DISPONIVEIS!``")

        item_reward = None
        for k, v in self.bot.items.items():
            if v[1] == name:
                item_reward = k
        if item_reward is None:
            return await ctx.send("<:negate:721581573396496464>│``ITEM NAO ENCONTRADO!``")

        try:
            update['inventory'][item_reward] += int(quant)
        except KeyError:
            update['inventory'][item_reward] = int(quant)

        update['treasure']['money'] -= self.items[name] * int(quant)
        await self.bot.db.update_data(data, update, 'users')
        a = '{:,.2f}'.format(float(self.items[name] * int(quant)))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')
        await ctx.send(f"<:confirmed:721581574461587496>|``SUA COMPRA FOI FEITA COM SUCESSO`` **{quant}** "
                       f"``{name.upper()} ADICIONADO NO SEU INVENTARIO COM SUCESSO QUE CUSTOU`` "
                       f"**R$ {d}** ``ETHERNYAS``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
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
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='pay', aliases=['pagar'])
    async def pay(self, ctx, member: discord.Member = None, amount: int = None):
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem.``")
        if amount is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa dizer uma quantia.``")
        if member.id == ctx.author.id:
            return await ctx.send("<:alert:739251822920728708>│``Você não pode pagar a si mesmo.``")

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        update_member = data_member
        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if data_member['config']['playing']:
            return await ctx.send("<:alert:739251822920728708>│``O membro está jogando, aguarde para quando"
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
            return await ctx.send(f'<:coins:519896825365528596>│``PARABENS, VC PAGOU R$ {self.format_num(amount)},00 '
                                  f'DE ETHERNYAS PARA {member.name} COM SUCESSO!``')
        else:
            return await ctx.send(f"<:alert:739251822920728708>│``VOCÊ NÃO TEM ESSE VALOR DISPONIVEL DE "
                                  f"ETHERNYAS!``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='give', aliases=['dar'])
    async def give(self, ctx, member: discord.Member = None, amount: int = None, *, item=None):
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem!``")
        if amount is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa dizer uma quantia!``")
        if member.id == ctx.author.id:
            return await ctx.send("<:alert:739251822920728708>│``Você não pode dar um item a si mesmo!``")
        if item is None:
            return await ctx.send("<:alert:739251822920728708>│``Você esqueceu de falar o nome do item para dar!``")

        item_key = convert_item_name(item, self.bot.items)
        if item_key is None:
            return await ctx.send("<:alert:739251822920728708>│``Item Inválido!``")
        if self.bot.items[item_key][2] is False:
            return await ctx.send("<:alert:739251822920728708>│``Você não pode dar esse tipo de item.``")

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        update_member = data_member

        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if data_member['config']['playing']:
            return await ctx.send("<:alert:739251822920728708>│``O membro está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        item_name = self.bot.items[item_key][1]

        if item_key in data_user['inventory']:
            if data_user['inventory'][item_key] >= amount:
                update_user['inventory'][item_key] -= amount
                if update_user['inventory'][item_key] < 1:
                    del update_user['inventory'][item_key]
                try:
                    update_member['inventory'][item_key] += amount
                except KeyError:
                    update_member['inventory'][item_key] = amount
                await self.bot.db.update_data(data_user, update_user, 'users')
                await self.bot.db.update_data(data_member, update_member, 'users')
                return await ctx.send(f'<:confirmed:721581574461587496>│``PARABENS, VC DEU {amount} DE '
                                      f'{item_name.upper()} PARA {member.name} COM SUCESSO!``')
            else:
                return await ctx.send(f"<:alert:739251822920728708>│``VOCÊ NÃO TEM ESSA QUANTIDADE DISPONIVEL DE "
                                      f"{item_name.upper()}!``")
        else:
            return await ctx.send("<:alert:739251822920728708>│``Você não tem esse item no seu inventario!``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='ticket', aliases=['raspadinha', 'rifa'])
    async def ticket(self, ctx, stone: int = None):
        """raspadinha da sorte da ashley"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        global coin, cost, plus

        def check(m):
            return m.author == ctx.author and m.content == '1' or m.author == ctx.author and m.content == '2' or \
                   m.author == ctx.author and m.content == '3'

        n_cost = [500, 75, 25]

        if stone not in [1, 2, 3]:
            await ctx.send(f"🎫│``Que tipo de`` **PEDRA** ``voce deseja gastar?"
                           f" Escolha uma dessas opções abaixo!``\n"
                           f"**[ 1 ]** - ``Para`` <:etherny_amarelo:691015381296480266> ``Custa:`` **{n_cost[0]}** "
                           f"``Bonus de Chance:`` **+1%**\n"
                           f"**[ 2 ]** - ``Para`` <:etherny_roxo:691014717761781851> ``Custa:`` **{n_cost[1]}** "
                           f"``Bonus de Chance:`` **+2%**\n"
                           f"**[ 3 ]** - ``Para`` <:etherny_preto:691016493957251152> ``Custa:`` **{n_cost[2]}** "
                           f"``Bonus de Chance:`` **+3%**")

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` **COMANDO'
                                      ' CANCELADO**')

            if int(answer.content) == 1:
                cost = n_cost[0]
                coin = "bronze"
                plus = 1
            if int(answer.content) == 2:
                cost = n_cost[1]
                coin = "silver"
                plus = 2
            if int(answer.content) == 3:
                cost = n_cost[2]
                coin = "gold"
                plus = 3
        else:
            if stone == 1:
                cost = n_cost[0]
                coin = "bronze"
                plus = 1
            if stone == 2:
                cost = n_cost[1]
                coin = "silver"
                plus = 2
            if stone == 3:
                cost = n_cost[2]
                coin = "gold"
                plus = 3

        if data['treasure'][coin] < cost:
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, você não tem pedras suficientes.`` '
                                  '**COMANDO CANCELADO**')

        # DATA DO MEMBRO
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        update_user['treasure'][coin] -= cost
        if update_user['treasure'][coin] < 0:
            update_user['treasure'][coin] = 0
        await self.bot.db.update_data(data_user, update_user, 'users')

        # DATA NATIVA DO SERVIDOR
        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native['data'][f"total_{coin}"] -= cost
        if update_guild_native['data'][f"total_{coin}"] < 0:
            update_guild_native['data'][f"total_{coin}"] = 0
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')

        msg = await ctx.send("<a:loading:520418506567843860>│``RASPANDO TICKET...``")
        await sleep(1)
        await msg.delete()

        awards = self.bot.config['artifacts']
        reward = choice(list(awards.keys()))
        exodia = ["braço_direito", "braço_esquerdo", "perna_direita", "perna_esquerda", "the_one"]
        reliquia = ["anel", "balança", "chave", "colar", "enigma", "olho", "vara"]
        lucky = "EXODIA" if reward in exodia else "RELIQUIA" if reward in reliquia else "ARMADURA"
        a = await ctx.send(f"<:alert:739251822920728708>│``SUA SORTE ESTÁ PARA:`` **{lucky}**")

        msg = await ctx.send("<a:loading:520418506567843860>│``SEU PREMIO FOI...``")
        await sleep(3)
        await msg.delete()

        percent = randint(1, 100)
        chance_ar = awards[reward]["chance"]
        chance = 100 * chance_ar + plus / 2 if randint(1, 10) > 5 else 100 * chance_ar + plus
        if percent <= chance:
            if reward in data["artifacts"]:
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                try:
                    update['inventory'][reward] += 1
                except KeyError:
                    update['inventory'][reward] = 1
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send(f">>> <a:blue:525032762256785409> ``VOCE TIROU UM ARTEFATO`` "
                                      f"**{self.bot.items[reward][1]}** ``REPETIDO, PELO MENOS VOCE GANHOU ESSA "
                                      f"RELIQUIA NO SEU INVENTARIO``")
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
            await ctx.send(f"<:confirmed:721581574461587496>│``PREMIO SALVO COM SUCESSO!``", delete_after=5.0)

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            if len(data['artifacts'].keys()) == 24 and not update['rpg']['vip']:
                update['rpg']['vip'] = True
                img = choice(git)
                embed = discord.Embed(color=self.bot.color)
                embed.set_image(url=img)
                await ctx.send(embed=embed)
                await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCE COMPLETOU TODOS OS ARTEFATOS!``"
                               f" ✨ **AGORA VC É VIP NO RPG** ✨")
            await self.bot.db.update_data(data, update, 'users')

        else:
            await ctx.send(f"> ``A SORTE NAO ESTAVA COM VOCE``", delete_after=30.0)
        await a.delete()

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='bollash', aliases=['pokebola', 'boll', 'bola'])
    async def bollash(self, ctx, stone: int = None):
        """bola para capitura dos pets da ashley"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        global coin, cost, plus

        def check(m):
            return m.author == ctx.author and m.content == '1' or m.author == ctx.author and m.content == '2' or \
                   m.author == ctx.author and m.content == '3'

        n_cost = [1000, 150, 50]

        if stone not in [1, 2, 3]:
            await ctx.send(f"🎫│``Que tipo de`` **PEDRA** ``voce deseja gastar?"
                           f" Escolha uma dessas opções abaixo!``\n"
                           f"**[ 1 ]** - ``Para`` <:etherny_amarelo:691015381296480266> ``Custa:`` **{n_cost[0]}** "
                           f"``Bonus de Chance:`` **+1%**\n"
                           f"**[ 2 ]** - ``Para`` <:etherny_roxo:691014717761781851> ``Custa:`` **{n_cost[1]}** "
                           f"``Bonus de Chance:`` **+2%**\n"
                           f"**[ 3 ]** - ``Para`` <:etherny_preto:691016493957251152> ``Custa:`` **{n_cost[2]}** "
                           f"``Bonus de Chance:`` **+3%**")

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` **COMANDO'
                                      ' CANCELADO**')

            if int(answer.content) == 1:
                cost = n_cost[0]
                coin = "bronze"
                plus = 1
            if int(answer.content) == 2:
                cost = n_cost[1]
                coin = "silver"
                plus = 2
            if int(answer.content) == 3:
                cost = n_cost[2]
                coin = "gold"
                plus = 3
        else:
            if stone == 1:
                cost = n_cost[0]
                coin = "bronze"
                plus = 1
            if stone == 2:
                cost = n_cost[1]
                coin = "silver"
                plus = 2
            if stone == 3:
                cost = n_cost[2]
                coin = "gold"
                plus = 3

        if data['treasure'][coin] < cost:
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, você não tem pedras suficientes.`` '
                                  '**COMANDO CANCELADO**')

        # DATA DO MEMBRO
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        update_user['treasure'][coin] -= cost
        if update_user['treasure'][coin] < 0:
            update_user['treasure'][coin] = 0
        await self.bot.db.update_data(data_user, update_user, 'users')

        # DATA NATIVA DO SERVIDOR
        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native['data'][f"total_{coin}"] -= cost
        if update_guild_native['data'][f"total_{coin}"] < 0:
            update_guild_native['data'][f"total_{coin}"] = 0
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')

        msg = await ctx.send("<a:loading:520418506567843860>│``TENTANDO DROPAR UMA ASHBOLL...``")
        await sleep(1)
        await msg.delete()

        percent = randint(1, 100)
        chance = 100 * 0.04 + plus / 2 if randint(1, 10) > 5 else 100 * 0.04 + 100 * 0.04 / 2 + plus
        if percent <= chance:

            embed = discord.Embed(title='🎊 **PARABENS** 🎉 VOCÊ DROPOU', color=self.bot.color,
                                  description=f"{self.bot.items['?-Bollash'][0]} ``{1}`` "
                                              f"``{self.bot.items['?-Bollash'][1]}``")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            msg = await ctx.send("<a:loading:520418506567843860>│``SALVANDO SEU PREMIO...``")
            await sleep(3)
            await msg.delete()

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory']['?-Bollash'] += 1
            except KeyError:
                update['inventory']['?-Bollash'] = 1
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send(f"<:confirmed:721581574461587496>│``PREMIO SALVO COM SUCESSO!``", delete_after=5.0)

        else:
            await ctx.send(f"> ``A SORTE NAO ESTAVA COM VOCE``", delete_after=30.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='stone', aliases=['pedra'])
    async def stone(self, ctx, stone: int = None):
        """bola para capitura dos pets da ashley"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        global coin, cost, plus

        def check(m):
            return m.author == ctx.author and m.content == '1' or m.author == ctx.author and m.content == '2' or \
                   m.author == ctx.author and m.content == '3'

        n_cost = [2000, 300, 100]

        if stone not in [1, 2, 3]:
            await ctx.send(f"🎫│``Que tipo de`` **PEDRA** ``voce deseja gastar?"
                           f" Escolha uma dessas opções abaixo!``\n"
                           f"**[ 1 ]** - ``Para`` <:etherny_amarelo:691015381296480266> ``Custa:`` **{n_cost[0]}** "
                           f"``Bonus de Chance:`` **+1%**\n"
                           f"**[ 2 ]** - ``Para`` <:etherny_roxo:691014717761781851> ``Custa:`` **{n_cost[1]}** "
                           f"``Bonus de Chance:`` **+2%**\n"
                           f"**[ 3 ]** - ``Para`` <:etherny_preto:691016493957251152> ``Custa:`` **{n_cost[2]}** "
                           f"``Bonus de Chance:`` **+3%**")

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=30.0)
            except TimeoutError:
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` **COMANDO'
                                      ' CANCELADO**')

            if int(answer.content) == 1:
                cost = n_cost[0]
                coin = "bronze"
                plus = 1
            if int(answer.content) == 2:
                cost = n_cost[1]
                coin = "silver"
                plus = 2
            if int(answer.content) == 3:
                cost = n_cost[2]
                coin = "gold"
                plus = 3
        else:
            if stone == 1:
                cost = n_cost[0]
                coin = "bronze"
                plus = 1
            if stone == 2:
                cost = n_cost[1]
                coin = "silver"
                plus = 2
            if stone == 3:
                cost = n_cost[2]
                coin = "gold"
                plus = 3

        if data['treasure'][coin] < cost:
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, você não tem pedras suficientes.`` '
                                  '**COMANDO CANCELADO**')

        # DATA DO MEMBRO
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        update_user['treasure'][coin] -= cost
        if update_user['treasure'][coin] < 0:
            update_user['treasure'][coin] = 0
        await self.bot.db.update_data(data_user, update_user, 'users')

        # DATA NATIVA DO SERVIDOR
        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native['data'][f"total_{coin}"] -= cost
        if update_guild_native['data'][f"total_{coin}"] < 0:
            update_guild_native['data'][f"total_{coin}"] = 0
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')

        msg = await ctx.send("<a:loading:520418506567843860>│``TENTANDO DROPAR UMA UNSEALED STONE...``")
        await sleep(1)
        await msg.delete()

        percent = randint(1, 100)
        chance = 100 * 0.05 + plus / 2 if randint(1, 10) > 5 else 100 * 0.01 + 100 * 0.05 / 2 + plus
        if percent <= chance:

            embed = discord.Embed(title='🎊 **PARABENS** 🎉 VOCÊ DROPOU', color=self.bot.color,
                                  description=f"{self.bot.items['unsealed_stone'][0]} ``{1}`` "
                                              f"``{self.bot.items['unsealed_stone'][1]}``")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            msg = await ctx.send("<a:loading:520418506567843860>│``SALVANDO SEU PREMIO...``")
            await sleep(3)
            await msg.delete()

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory']['unsealed_stone'] += 1
            except KeyError:
                update['inventory']['unsealed_stone'] = 1
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send(f"<:confirmed:721581574461587496>│``PREMIO SALVO COM SUCESSO!``", delete_after=5.0)

        else:
            await ctx.send(f"> ``A SORTE NAO ESTAVA COM VOCE``", delete_after=30.0)


def setup(bot):
    bot.add_cog(UserBank(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUSERBANK\033[1;32m foi carregado com sucesso!\33[m')
