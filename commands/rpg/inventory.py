import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import paginator
from resources.img_edit import equips


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
        if ctx.invoked_subcommand is None:
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
            for key in data['rpg']["equipped_items"].keys():
                if data['rpg']["equipped_items"][key] is not None:
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
                    "shield": data['rpg']["equipped_items"]['shield']
                }
            }

            equips(data_test)
            await ctx.send("```Markdown\n[>>]: PARA EQUIPAR UM ITEM USE O COMANDO\n<ASH EQUIP ITEM NOME_DO_ITEM>\n"
                           "[>>]: PARA RESETAR OS EQUIPAMENTOS USE O COMANDO\n<ASH EQUIP RESET>```")
            if discord.File('equips.png') is None:
                return await ctx.send("<:negate:721581573396496464>│``ERRO!``")
            await ctx.send(file=discord.File('equips.png'), delete_after=60.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @equip.command(name='reset', aliases=['r'])
    async def _reset(self, ctx):
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
                return await ctx.send("<:negate:721581573396496464>│``ESSE ITEM ESTÁ SELADO, ANTES DISSO TIRE O SELO E"
                                      " USE O NOME DO COMANDO:`` **ASH INVENTORY EQUIP** ``OU`` **ASH I E**")
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
            plus = "EQUIPADO"
            equip_in = None

            for key in update['rpg']['items'].keys():
                for name in equips_list:
                    if name[0] == key and name[1]["name"] == item:
                        equip_in = name

            if equip_in is not None:

                update['rpg']['items'][equip_in[0]] -= 1
                if update['rpg']['items'][equip_in[0]] < 1:
                    del update['rpg']['items'][equip_in[0]]

                if data['rpg']['next_class'] in equip_in[1]["class"]:
                    update['rpg']["equipped_items"][equip_in[1]["slot"]] = equip_in[0]

                else:
                    await msg.delete()
                    return await ctx.send("<:negate:721581573396496464>│``SUA CLASSE NAO PODE USAR ESSE ITEM...``")

        else:
            return await ctx.send("<:negate:721581573396496464>│``VOCE NAO TEM ESSE ITEM...``")

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
            embed = ['Inventário:', self.color, 'Items: \n']
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

        embed = ['Inventário:', self.color, 'Equipamentos: \n']

        eq = dict()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                eq[k] = v

        await paginator(self.bot, eq, data['rpg']['items'], embed, ctx)


def setup(bot):
    bot.add_cog(InventoryClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mINVENTORYCLASS\033[1;32m foi carregado com sucesso!\33[m')
