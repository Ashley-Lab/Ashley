import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice
from asyncio import sleep, TimeoutError
from resources.utility import convert_item_name


git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class MergeClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.i = self.bot.items
        self.merge_data = self.bot.config['attribute']['merge_data']
        self.max_level = self.bot.config['attribute']['max_level']
        self.sealed_items = [k for k, v in self.bot.items.items() if v[3] == 9]

        self.cost = {
            "solution_agent_green": 1,
            "solution_agent_blue": 1,
            "Discharge_Crystal": 15,
            "Acquittal_Crystal": 15,
            "Crystal_of_Energy": 15
        }

        self.cost_convert = {
            "crystal_fragment_light": 50,
            "crystal_fragment_energy": 50,
            "crystal_fragment_dark": 50
        }

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='merge', aliases=['fundir'])
    async def merge(self, ctx, *, item=None):
        """Comando especial para fundir itens de uma mesma raridade para uma maior"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if not update['rpg']['active']:
            msg = "<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``"
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if update['config']['battle']:
            msg = '<:negate:721581573396496464>│``VOCE ESTÁ BATALHANDO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if update['rpg']['level'] < 26:
            msg = '<:negate:721581573396496464>│``VOCE PRECISA ESTA NO NIVEL 26 OU MAIOR PARA USAR EQUIPAMENTOS!\n' \
                  'OLHE O SEU NIVEL NO COMANDO:`` **ASH SKILL**'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if item is None:
            return await ctx.send("<:negate:721581573396496464>│``Você precisa colocar o nome de um item que deseja "
                                  "fundir:`` **ash merge <nome_do_item>** ``voce consegue ver os itens "
                                  "usando o comando:`` **ash inventory e**")

        equips_list = list()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                equips_list.append((k, v))

        if item not in [i[1]["name"] for i in equips_list]:
            if "sealed" in item.lower():
                return await ctx.send("<:negate:721581573396496464>│``ESSE ITEM ESTÁ SELADO, ANTES DISSO TIRE O SELO "
                                      "USANDO O COMANDO:`` **ASH LIBERAR** ``E USE O NOME DO COMANDO:`` **ASH MERGE**")
            return await ctx.send("<:negate:721581573396496464>│``ESSE ITEM NAO EXISTE...``")

        items_inventory = list()
        key_item = None
        for key in update['rpg']["items"].keys():
            for i in equips_list:
                if i[0] == key:
                    items_inventory.append(i[1]["name"])
                    if i[1]["name"] == item:
                        key_item = (key, update['rpg']["items"][key])

        if item not in items_inventory or key_item is None:
            return await ctx.send("<:negate:721581573396496464>│``VOCE NAO TEM ESSE ITEM OU ELE ESTÁ EQUIPADO...``")

        if key_item[1] < 3:
            return await ctx.send("<:negate:721581573396496464>│``VOCE NAO TEM 3 DESSE ITEM PARA FUNDIR...``")
        if key_item[0] in self.max_level:
            return await ctx.send("<:negate:721581573396496464>│``ESSE ITEM JA ESTA NO NIVEL MAXIMO!``")

        # =========================================================================================

        msg = f"\n".join([f"{self.i[k][0]} ``{v}`` ``{self.i[k][1]}``" for k, v in self.cost.items()])
        msg += "\n\n**OBS:** ``PARA CONSEGUIR OS ITENS VOCE PRECISA USAR O COMANDO`` **ASH BOX**"

        Embed = discord.Embed(
            title="O CUSTO PARA VOCE FUNDIR UM EQUIPAMENTO:",
            color=self.bot.color,
            description=msg)
        Embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        Embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
        Embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=Embed)

        cost = {}
        for i_, amount in self.cost.items():
            if i_ in data['inventory']:
                if data['inventory'][i_] < self.cost[i_]:
                    cost[i_] = self.cost[i_]
            else:
                cost[i_] = self.cost[i_]

        if len(cost) > 0:
            msg = f"\n".join([f"{self.i[key][0]} **{key.upper()}**" for key in cost.keys()])
            return await ctx.send(f"<:alert:739251822920728708>│``Lhe faltam esses itens para fundir um equipamento:``"
                                  f"\n{msg}\n``OLHE SEU INVENTARIO E VEJA A QUANTIDADE QUE ESTÁ FALTANDO.``")

        def check_option(m):
            return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

        msg = await ctx.send(f"<:alert:739251822920728708>│``VOCE JA TEM TODOS OS ITEM NECESSARIOS, DESEJA FUNDIR "
                             f"SEU EQUIPAMENTO AGORA?``\n**1** para ``SIM`` ou **0** para ``NÃO``")
        try:
            answer = await self.bot.wait_for('message', check=check_option, timeout=30.0)
        except TimeoutError:
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``COMANDO CANCELADO!``")
        if answer.content == "0":
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``COMANDO CANCELADO!``")

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``removendo os itens de custo e os equipamentos da sua"
                               f" conta...``")

        # =========================================================================================

        for i_, amount in self.cost.items():
            update['inventory'][i_] -= amount
            if update['inventory'][i_] < 1:
                del update['inventory'][i_]

        update['rpg']['items'][key_item[0]] -= 3
        if update['rpg']['items'][key_item[0]] < 1:
            del update['rpg']['items'][key_item[0]]

        try:
            update['rpg']['items'][self.merge_data[key_item[0]]] += 1
        except KeyError:
            update['rpg']['items'][self.merge_data[key_item[0]]] = 1

        await msg.edit(content=f"<:confirmed:721581574461587496>│``itens retirados com sucesso...``")
        await sleep(2)
        await msg.delete()

        await self.bot.db.update_data(data, update, 'users')
        await ctx.send(f"<:confirmed:721581574461587496>│``O ITEM {item.upper()} FOI FUNDIDO COM SUCESSO, "
                       f"OLHE O SEU INVENTARIO DE ITENS E VEJA SEU NOVO ITEM!``")
        img = choice(git)
        embed = discord.Embed(color=self.bot.color)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='convert', aliases=['converter'])
    async def convert(self, ctx, *, item=None):
        if item is None:
            return await ctx.send("<:alert:739251822920728708>│``Você esqueceu de falar o nome do item para "
                                  "converter!``")

        item_key = convert_item_name(item, self.bot.items)
        if item_key is None:
            return await ctx.send("<:alert:739251822920728708>│``Item Inválido!``")

        if item_key not in self.sealed_items:
            return await ctx.send("<:alert:739251822920728708>│``Esse item nao é um equipamento selado!``")

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if item_key not in data['inventory']:
            return await ctx.send("<:alert:739251822920728708>│``Você não tem esse item no seu inventario!``")

        # =========================================================================================

        msg = f"\n".join([f"{self.i[k][0]} ``{v}`` ``{self.i[k][1]}``" for k, v in self.cost_convert.items()])
        msg += "\n\n**OBS:** ``PARA CONSEGUIR OS ITENS VOCE PRECISA USAR O COMANDO`` **ASH BOX**"

        Embed = discord.Embed(
            title="O CUSTO PARA VOCE CONVERTER UM EQUIPAMENTO SELADO:",
            color=self.bot.color,
            description=msg)
        Embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        Embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
        Embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=Embed)

        cost = {}
        for i_, amount in self.cost_convert.items():
            if i_ in data['inventory']:
                if data['inventory'][i_] < self.cost_convert[i_]:
                    cost[i_] = self.cost_convert[i_]
            else:
                cost[i_] = self.cost_convert[i_]

        if len(cost) > 0:
            msg = f"\n".join([f"{self.i[key][0]} **{key.upper()}**" for key in cost.keys()])
            return await ctx.send(f"<:alert:739251822920728708>│``Falta esses itens para converter um equipamento:``"
                                  f"\n{msg}\n``OLHE SEU INVENTARIO E VEJA A QUANTIDADE QUE ESTÁ FALTANDO.``")

        def check_option(m):
            return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

        msg = await ctx.send(f"<:alert:739251822920728708>│``VOCE JA TEM TODOS OS ITEM NECESSARIOS, DESEJA CONVERTER "
                             f"SEU EQUIPAMENTO SELADO AGORA?``\n**1** para ``SIM`` ou **0** para ``NÃO``")
        try:
            answer = await self.bot.wait_for('message', check=check_option, timeout=30.0)
        except TimeoutError:
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``COMANDO CANCELADO!``")
        if answer.content == "0":
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``COMANDO CANCELADO!``")

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``removendo os itens de custo e o equipamento da sua"
                               f" conta...``")

        # =========================================================================================

        for i_, amount in self.cost_convert.items():
            update['inventory'][i_] -= amount
            if update['inventory'][i_] < 1:
                del update['inventory'][i_]

        update['inventory'][item_key] -= 1
        if update['inventory'][item_key] < 1:
            del update['inventory'][item_key]

        def check_item(m):
            return m.author == ctx.author

        msg = await ctx.send(f"<:alert:739251822920728708>│``QUAL O NOME DO EQUIPAMENTO SELADO, QUE VOCE SEJA QUE SEU"
                             f" EQUIPAMENTO ATUAL SEJA CONVERTIDO?``")
        try:
            answer = await self.bot.wait_for('message', check=check_item, timeout=30.0)
        except TimeoutError:
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``COMANDO CANCELADO!``")

        item_convert = convert_item_name(answer.content, self.bot.items)
        if item_convert is None:
            await msg.delete()
            return await ctx.send("<:alert:739251822920728708>│``Item Inválido!``")
        if item_convert not in self.sealed_items:
            await msg.delete()
            return await ctx.send("<:alert:739251822920728708>│``Esse item nao é um equipamento selado!``")

        try:
            update['inventory'][item_convert] += 1
        except KeyError:
            update['inventory'][item_convert] = 1

        await msg.edit(content=f"<:confirmed:721581574461587496>│``itens retirados com sucesso...``")
        await sleep(2)
        await msg.delete()

        await self.bot.db.update_data(data, update, 'users')
        await ctx.send(f"<:confirmed:721581574461587496>│``O ITEM {item.upper()} FOI CONVERTIDO PARA "
                       f"{item_convert.upper()} COM SUCESSO, OLHE O SEU INVENTARIO DE ITENS E VEJA SEU NOVO ITEM!``")


def setup(bot):
    bot.add_cog(MergeClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMERGE_ITEM\033[1;32m foi carregado com sucesso!\33[m')
