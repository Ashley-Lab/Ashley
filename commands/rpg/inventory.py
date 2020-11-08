import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import paginator
from resources.img_edit import equips
from asyncio import sleep, TimeoutError

botmsg = {}


class InventoryClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.i = self.bot.items
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='equip', aliases=['e', 'equipamento'])
    async def equip(self, ctx):
        """Comando para mostrar o painel de equipamentos do seu personagem"""
        if ctx.invoked_subcommand is None:
            global botmsg
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")

            if not data['rpg']['active']:
                embed = discord.Embed(
                    color=self.bot.color,
                    description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
                return await ctx.send(embed=embed)

            eq = dict()
            for ky in self.bot.config['equips'].keys():
                for k, v in self.bot.config['equips'][ky].items():
                    eq[k] = v

            set_armor = list()
            sts = {"atk": 0, "agi": 0, "prec": 0, "con": 0}
            set_value = ["shoulder", "breastplate", "gloves", "leggings", "boots"]
            for key in data['rpg']["equipped_items"].keys():
                if data['rpg']["equipped_items"][key] is not None:
                    if key in set_value:
                        set_armor.append(data['rpg']["equipped_items"][key])
                    for k in sts.keys():
                        sts[k] += eq[data['rpg']["equipped_items"][key]]["modifier"][k]

            for kkk in self.bot.config["set_equips"].values():
                if kkk['set'] == set_armor:
                    for name in sts.keys():
                        try:
                            sts[name] += kkk['modifier'][name]
                        except KeyError:
                            pass

            if data['rpg']['level'] > 25:
                atk = self.bot.config['skills'][data['rpg']['next_class']]['modifier']['atk']
                dex = self.bot.config['skills'][data['rpg']['next_class']]['modifier']['agi']
                acc = self.bot.config['skills'][data['rpg']['next_class']]['modifier']['prec']
                con = self.bot.config['skills'][data['rpg']['next_class']]['modifier']['con']
            else:
                atk = 0
                dex = 0
                acc = 0
                con = 0

            data_test = {
                "name": ctx.author.name,
                "class": str(data['rpg']['next_class']),

                "status_base": {
                    "atk": str(data['rpg']['status']['atk']),
                    "dex": str(data['rpg']['status']['agi']),
                    "acc": str(data['rpg']['status']['prec']),
                    "con": str(data['rpg']['status']['con']),
                    "luk": str(data['rpg']['status']['luk'])
                },

                "status_class": {
                    "atk": str(atk),
                    "dex": str(dex),
                    "acc": str(acc),
                    "con": str(con),
                    "luk": str(0)
                },

                "status_equip": {
                    "atk": str(sts["atk"]),
                    "dex": str(sts["agi"]),
                    "acc": str(sts["prec"]),
                    "con": str(sts["con"]),
                    "luk": str(0)
                },

                'equipped': {
                    "breastplate": data['rpg']["equipped_items"]['breastplate'],
                    "leggings": data['rpg']["equipped_items"]['leggings'],
                    "boots": data['rpg']["equipped_items"]['boots'],
                    "gloves": data['rpg']["equipped_items"]['gloves'],
                    "shoulder": data['rpg']["equipped_items"]['shoulder'],
                    "sword": data['rpg']["equipped_items"]['sword'],
                    "shield": data['rpg']["equipped_items"]['shield'],
                    "consumable": data['rpg']["equipped_items"]['consumable'],
                    "necklace": data['rpg']["equipped_items"]['necklace'],
                    "earring": data['rpg']["equipped_items"]['earring'],
                    "ring": data['rpg']["equipped_items"]['ring']
                }
            }

            equips(data_test)
            if discord.File('equips.png') is None:
                return await ctx.send("<:negate:721581573396496464>│``ERRO!``")
            botmsg[ctx.author.id] = await ctx.send(file=discord.File('equips.png'))
            await botmsg[ctx.author.id].add_reaction('<a:help:767825933892583444>')

            text = "```Markdown\n[>>]: PARA EQUIPAR UM ITEM USE O COMANDO\n<ASH EQUIP ITEM NOME_DO_ITEM>\n" \
                   "[>>]: PARA RESETAR OS EQUIPAMENTOS USE O COMANDO\n<ASH EQUIP RESET>\n\n" \
                   "[>>]: PARA MAIS INFORMAÇÕES USE O COMANDO\n<ASH EQUIP INFO>```"

            again = False
            msg = None

            while not self.bot.is_closed():
                try:
                    reaction = await self.bot.wait_for('reaction_add', timeout=60.0)
                    while reaction[1].id != ctx.author.id:
                        reaction = await self.bot.wait_for('reaction_add', timeout=60.0)

                    emo = "<a:help:767825933892583444>"
                    emoji = str(emo).replace('<a:', '').replace(emo[emo.rfind(':'):], '')
                    try:
                        try:
                            _reaction = reaction[0].emoji.name
                        except AttributeError:
                            _reaction = reaction[0].emoji
                        if _reaction == emoji and not again and reaction[0].message.id == botmsg[ctx.author.id].id:
                            again = True
                            try:
                                await botmsg[ctx.author.id].remove_reaction("<a:help:767825933892583444>", ctx.author)
                            except discord.errors.Forbidden:
                                pass
                            msg = await ctx.send(text)

                        elif _reaction == emoji and again and reaction[0].message.id == botmsg[ctx.author.id].id:
                            again = False
                            try:
                                await botmsg[ctx.author.id].remove_reaction("<a:help:767825933892583444>", ctx.author)
                            except discord.errors.Forbidden:
                                pass
                            await msg.delete()

                    except AttributeError:
                        pass
                except TimeoutError:
                    return await botmsg[ctx.author.id].remove_reaction("<a:help:767825933892583444>", ctx.me)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @equip.command(name='info')
    async def _info(self, ctx):
        """Comando que mostra as informações dos equipamentos do seu personagem"""
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

        equips_list = list()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                equips_list.append((k, v))

        equipped_items = list()
        for value in update['rpg']["equipped_items"].values():
            for i in equips_list:
                if i[0] == value:
                    equipped_items.append(i[1])

        if len(equipped_items) == 0:
            msg = "VOCE NAO TEM ITENS EQUIPADOS NO MOMENTO, USE O COMANDO \"ASH I E\" PARA VER OS ITEMS PARA EQUIPAR," \
                  " LOGO APOS USE O COMANDO \"ASH E I <NOME_DO_ITEM>\" PARA EQUIPAR O SEU ITEM."
            return await ctx.send(f"<:confirmed:721581574461587496>│``ITENS EQUIPADOS EM VOCE:``\n```{msg}```")

        msg = '```Markdown\n'
        for item in equipped_items:
            text = "DAMAGE_ABSORPTION"
            msg += f"[>>]: {item['name'].upper()}\n<{text} = {item['armor']} RARITY = \"{item['rarity']}\">\n" \
                   f"<STATUS: ATK = \"{item['modifier']['atk']}\" DEX = \"{item['modifier']['agi']}\" " \
                   f"ACC = \"{item['modifier']['prec']}\" CON = \"{item['modifier']['con']}\">\n\n"
        msg += "```"
        await ctx.send(f"<:confirmed:721581574461587496>│``ITENS EQUIPADOS EM VOCE:``\n{msg}")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @equip.command(name='reset', aliases=['r'])
    async def _reset(self, ctx):
        """Esse comando retira todos os equipamentos do seu persoangem, para o seu inventario"""
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

        equips_list = list()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                equips_list.append((k, v))

        equipped_items = list()
        for value in update['rpg']["equipped_items"].values():
            for i in equips_list:
                if i[0] == value:
                    equipped_items.append(i[1]["name"])

        equip_out = list()
        for key in update['rpg']["equipped_items"].keys():
            if update['rpg']["equipped_items"][key] is not None:
                for name in equips_list:
                    if name[0] == update['rpg']["equipped_items"][key]:
                        equip_out.append(update['rpg']['equipped_items'][key])
                        update['rpg']['equipped_items'][key] = None

        if len(equip_out) > 0:
            for item in equip_out:
                try:
                    update['rpg']['items'][item] += 1
                except KeyError:
                    update['rpg']['items'][item] = 1

            await self.bot.db.update_data(data, update, 'users')
            await ctx.send(f"<:confirmed:721581574461587496>│``OS ITENS ESTAO NO SEU INVENTARIO DE EQUIPAMENTOS!``")

        else:
            msg = '<:negate:721581573396496464>│``VOCE NÃO TEM ITEM EQUIPADO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @equip.command(name='item', aliases=['i'])
    async def _item(self, ctx, *, item=None):
        """Esse comando equipa um item do seu inventario de equipamento no seu personagem"""
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
                                  "equipar em voce:`` **ash equip i <nome_do_item>** ``voce consegue ver os itens "
                                  "usando o comando:`` **ash inventory e**")

        equips_list = list()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                equips_list.append((k, v))

        if item not in [i[1]["name"] for i in equips_list]:
            if "sealed" in item.lower():
                return await ctx.send("<:negate:721581573396496464>│``ESSE ITEM ESTÁ SELADO, ANTES DISSO TIRE O SELO "
                                      "USANDO O COMANDO:`` **ASH LIBERAR** ``E USE O NOME DO COMANDO:`` "
                                      "**ASH INVENTORY EQUIP** ``OU`` **ASH I E**")
            return await ctx.send("<:negate:721581573396496464>│``ESSE ITEM NAO EXISTE...``")

        equipped_items = list()
        for value in update['rpg']["equipped_items"].values():
            for i in equips_list:
                if i[0] == value:
                    equipped_items.append(i[1]["name"])

        items_inventory = list()
        for key in update['rpg']["items"].keys():
            for i in equips_list:
                if i[0] == key:
                    items_inventory.append(i[1]["name"])

        if item in equipped_items:
            msg = await ctx.send("<a:loading:520418506567843860>│``O ITEM JA ESTA EQUIPADO EM VOCE, DESEQUIPANDO...``")
            plus = "DESEQUIPADO"
            equip_out = None

            for key in update['rpg']["equipped_items"].keys():
                if update['rpg']["equipped_items"][key] is not None:
                    for name in equips_list:
                        if name[1]["name"] == item and name[0] == update['rpg']["equipped_items"][key]:
                            equip_out = update['rpg']['equipped_items'][key]
                            update['rpg']['equipped_items'][key] = None

            if equip_out is not None:
                try:
                    update['rpg']['items'][equip_out] += 1
                except KeyError:
                    update['rpg']['items'][equip_out] = 1

        elif item in items_inventory:
            msg = await ctx.send("<a:loading:520418506567843860>│``O ITEM ESTA NO SEU INVENTARIO, EQUIPANDO...``")
            await sleep(1)
            plus = "EQUIPADO"
            equip_in = None

            # aqui esta verificando qual o ID do item
            for key in update['rpg']['items'].keys():
                for name in equips_list:
                    if name[0] == key and name[1]["name"] == item:
                        equip_in = name

            if equip_in is not None:
                if data['rpg']['next_class'] in equip_in[1]["class"]:

                    # aqui esta tirando o item do inventario
                    update['rpg']['items'][equip_in[0]] -= 1
                    if update['rpg']['items'][equip_in[0]] < 1:
                        del update['rpg']['items'][equip_in[0]]

                    # se o slot do item esta vazio, apenas equipa o item!
                    if update['rpg']["equipped_items"][equip_in[1]["slot"]] is None:
                        update['rpg']["equipped_items"][equip_in[1]["slot"]] = equip_in[0]

                    # caso contrario, inicia os testes...
                    else:
                        await sleep(1)
                        await msg.delete()
                        return await ctx.send("<:negate:721581573396496464>│``VOCE PRECISA DESEQUIPAR O ITEM "
                                              "EXISTENTE...``\n**Use o comando: \"ash e info\" verifique o nome do "
                                              "item existente, entao use o comando \"ash e i <nome_do_item>\" "
                                              "para desequipar o item atual, entao voce usa o comando novamente "
                                              "com o nome do item que voce quer equipar.**")

                else:
                    await sleep(1)
                    await msg.delete()
                    return await ctx.send("<:negate:721581573396496464>│``SUA CLASSE NAO PODE USAR ESSE ITEM...``")

        else:
            return await ctx.send("<:negate:721581573396496464>│``VOCE NAO TEM ESSE ITEM...``")

        await sleep(1)
        await msg.delete()
        await ctx.send(f"<:confirmed:721581574461587496>│``O ITEM {item.upper()} FOI {plus} COM SUCESSO!``")
        await self.bot.db.update_data(data, update, 'users')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='inventory', aliases=['inventario', 'i'])
    async def inventory(self, ctx):
        """Comando usado pra ver seu inventario
        Use ash i ou ash inventory"""
        if ctx.invoked_subcommand is None:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            embed = ['Inventário de itens:', self.color, 'Items: \n']
            await paginator(self.bot, self.i, data['inventory'], embed, ctx)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @inventory.command(name='equip', aliases=['equipamento', 'e'])
    async def _equip(self, ctx):
        """Comando usado pra ver seu inventario de equipamentos
                Use ash i ou ash inventory"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")

        if len(data['rpg']['items'].keys()) == 0:
            return await ctx.send(f"<:negate:721581573396496464>|``SEU INVENTARIO DE EQUIPAMENTOS ESTÁ VAZIO!``")

        embed = ['Inventário de equipamentos:', self.color, 'Equipamentos: \n']

        eq = dict()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                eq[k] = v

        await paginator(self.bot, eq, data['rpg']['items'], embed, ctx)


def setup(bot):
    bot.add_cog(InventoryClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mINVENTORYCLASS\033[1;32m foi carregado com sucesso!\33[m')
