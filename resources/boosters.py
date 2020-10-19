from random import randint, choice


class Booster(object):
    def __init__(self, items_):
        self.items = items_
        self.ranking = None
        self.is_vip = None
        self.item_ = None
        self.key_item = None

        # box configs
        self.box = {"status": {"active": True, "secret": 0, "ur": 0, "sr": 0, "r": 0, "i": 0, "c": 0}}
        self.legend = {"Comum": 0, "Incomum": 1, "Raro": 2, "Super Raro": 3, "Ultra Raro": 4, "Secret": 5}
        self.bl = {"Comum": "c", "Incomum": "i", "Raro": "r", "Super Raro": "sr", "Ultra Raro": "ur",
                   "Secret": "secret"}
        self.rarity = {
            "Comum": [600, [0.01, 0.02, 0.07, 0.10, 0.20, 0.60]],
            "Incomum": [500, [0.02, 0.04, 0.10, 0.24, 0.50, 0.10]],
            "Raro": [400, [0.03, 0.07, 0.10, 0.50, 0.20, 0.10]],
            "Super Raro": [300, [0.04, 0.06, 0.40, 0.10, 0.20, 0.20]],
            "Ultra Raro": [200, [0.20, 0.40, 0.10, 0.10, 0.10, 0.10]],
            "Secret": [100, [0.40, 0.20, 0.15, 0.10, 0.10, 0.05]]
        }

        # booster configs
        self.booster_choice = {"Comum": 0, "Incomum": 0, "Raro": 0, "Super Raro": 0, "Ultra Raro": 0, "Secret": 0}
        # rarity configs
        self.rarity_choice = {"Comum": 25, "Incomum": 25, "Raro": 20, "Super Raro": 15, "Ultra Raro": 10, "Secret": 5}

        # contadores de itens
        self.secret = 0
        self.ur = 0
        self.sr = 0
        self.r = 0
        self.i = 0
        self.c = 0

        # contador de itens por box
        self.box_count = 0

        # Limites dos itens
        self.l_secret = 0
        self.l_ur = 0
        self.l_sr = 0
        self.l_r = 0
        self.l_i = 0
        self.l_c = 0

    def reset_counts(self):
        self.box = {"status": {"active": True, "secret": 0, "ur": 0, "sr": 0, "r": 0, "i": 0, "c": 0}}
        self.box_count = 0
        self.secret = 0
        self.ur = 0
        self.sr = 0
        self.r = 0
        self.i = 0
        self.c = 0

    def define_limit(self, rarity):
        # Limites dos itens
        self.l_secret = int(rarity[0] * rarity[1][0])
        self.l_ur = int(rarity[0] * rarity[1][1])
        self.l_sr = int(rarity[0] * rarity[1][2])
        self.l_r = int(rarity[0] * rarity[1][3])
        self.l_i = int(rarity[0] * rarity[1][4])
        self.l_c = int(rarity[0] * rarity[1][5])

    def create_box(self, summon):
        rarity_choice = []
        for i_, amount in self.rarity_choice.items():
            rarity_choice += [i_] * amount
        rarity = choice(rarity_choice)

        if summon is not None:
            rarity = summon

        size = self.rarity[rarity][0]
        self.reset_counts()
        self.define_limit(self.rarity[rarity])
        self.box['status']['rarity'] = rarity
        self.box['status']['size'] = size
        self.box['items'] = dict()
        while self.box_count < size:
            item = choice(list(self.items.keys()))
            if self.items[item][3] == 5:
                if self.secret < self.l_secret:
                    if item not in self.box['items']:
                        self.box['items'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['secret'] += 1
                    else:
                        self.box['items'][item]['size'] += 1
                        self.box['status']['secret'] += 1
                    self.secret += 1
                    self.box_count += 1
            elif self.items[item][3] == 4:
                if self.ur < self.l_ur:
                    if item not in self.box['items']:
                        self.box['items'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['ur'] += 1
                    else:
                        self.box['items'][item]['size'] += 1
                        self.box['status']['ur'] += 1
                    self.ur += 1
                    self.box_count += 1
            elif self.items[item][3] == 3:
                if self.sr < self.l_sr:
                    if item not in self.box['items']:
                        self.box['items'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['sr'] += 1
                    else:
                        self.box['items'][item]['size'] += 1
                        self.box['status']['sr'] += 1
                    self.sr += 1
                    self.box_count += 1
            elif self.items[item][3] == 2:
                if self.r < self.l_r:
                    if item not in self.box['items']:
                        self.box['items'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['r'] += 1
                    else:
                        self.box['items'][item]['size'] += 1
                        self.box['status']['r'] += 1
                    self.r += 1
                    self.box_count += 1
            elif self.items[item][3] == 1:
                if self.i < self.l_i:
                    if item not in self.box['items']:
                        self.box['items'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['i'] += 1
                    else:
                        self.box['items'][item]['size'] += 1
                        self.box['status']['i'] += 1
                    self.i += 1
                    self.box_count += 1
            elif self.items[item][3] == 0:
                if self.c < self.l_c:
                    if item not in self.box['items']:
                        self.box['items'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['c'] += 1
                    else:
                        self.box['items'][item]['size'] += 1
                        self.box['status']['c'] += 1
                    self.c += 1
                    self.box_count += 1
        return self.box

    async def buy_box(self, bot, ctx, summon):
        data = await bot.db.get_data("user_id", ctx.author.id, "users")
        if data['treasure']['money'] > 2000:
            answer = await bot.db.take_money(ctx, 2000)
        else:
            return await ctx.send("<:alert:739251822920728708>│``VOCÊ NÃO TEM DINHEIRO PARA COMPRAR "
                                  "A BOX!\nVOCÊ PRECISA DE 2.000 ETHERNYAS PARA COMPRAR UMA BOX.``")
        data = await bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        box = self.create_box(summon)
        update['box'] = box
        await bot.db.update_data(data, update, 'users')
        await ctx.send(answer)
        await ctx.send("```A BOX ENCONTRA-SE NA SUA CONTA!```")

    def buy_item(self, box_):
        self.item_ = None

        for k, v in self.bl.items():
            self.booster_choice[k] = box_['status'][v]

        list_items = []
        for i_, amount in self.booster_choice.items():
            list_items += [i_] * amount

        for _ in range(len(list_items)):
            result = choice(list_items)
            if box_['status'][self.bl[result]] > 0:
                self.item_ = choice(list(box_['items'].values()))
                while list(self.legend.keys())[list(self.legend.values()).index(self.item_['data'][3])] != result:
                    self.item_ = choice(list(box_['items'].values()))
                break

        return self.item_

    async def buy_booster(self, bot, ctx, vip):
        data = await bot.db.get_data("user_id", ctx.author.id, "users")
        if not data['box']['status']['active']:
            return "<:alert:739251822920728708>|``BOX INATIVA!``", None

        price = 500
        if data['user']['ranking'] == "Bronze":
            price -= 50
        if data['user']['ranking'] == "Silver":
            price -= 75
        if data['user']['ranking'] == "Gold":
            price -= 125
        if data['config']['vip']:
            price -= 50

        if data['treasure']['money'] < price:
            return (f"<:alert:739251822920728708>│``VOCÊ NÃO TEM DINHEIRO PARA COMPRAR UM BOOSTER"
                    f"\nVOCÊ PRECISA DE {price} ETHENYAS PARA COMPRAR UM BOOSTER.``", None)

        answer = await bot.db.take_money(ctx, price)
        if not vip:
            await ctx.send(answer)
        data = await bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        item = self.buy_item(data['box'])
        if item is None:
            return "<:alert:739251822920728708>│``VOCÊ FALHOU EM COMPRAR O ITEM...``", None

        for k, v in self.items.items():
            if v == item['data']:
                self.key_item = k

        Empty = False
        rarity = list(self.legend.keys())[list(self.legend.values()).index(item['data'][3])]
        update['box']['status'][self.bl[rarity]] -= 1
        update['box']['status']['size'] -= 1
        update['box']['items'][self.key_item]['size'] -= 1

        if update['box']['status']['size'] <= 0:
            update['box']['status']['active'] = False
            Empty = True

        bonus_1 = choice(['crystal_fragment_light', 'crystal_fragment_energy', 'crystal_fragment_dark'])
        bonus_2 = choice(["Melted_Bone", "Life_Crystal", "Death_Blow", "Stone_of_Soul", "Vital_Force", "Energy"])
        quant_1 = randint(1, 3)
        quant_2 = randint(1, 3)
        quant_3 = randint(1, 3)

        try:
            update['inventory'][self.key_item] += quant_1
        except KeyError:
            update['inventory'][self.key_item] = quant_1

        try:
            update['inventory'][bonus_1] += quant_2
        except KeyError:
            update['inventory'][bonus_1] = quant_2

        try:
            update['inventory'][bonus_2] += quant_3
        except KeyError:
            update['inventory'][bonus_2] = quant_3

        await bot.db.update_data(data, update, 'users')

        if Empty:
            item_1 = choice(['Unearthly', 'Surpassing', 'Hurricane', 'Heavenly', 'Blazing', 'Augur'])
            item_2 = choice(['Crystal_of_Energy', 'Discharge_Crystal', 'Acquittal_Crystal'])
            item_3 = choice(['SoulStoneYellow', 'SoulStoneRed', 'SoulStonePurple', 'SoulStoneGreen',
                             'SoulStoneDarkGreen', 'SoulStoneBlue'])
            reward = [item_1, item_2, item_3]
            response = await bot.db.add_reward(ctx, reward)
            empty = f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCE ACABA DE ESVAZIAR SUA BOX, " \
                    f"COMO PREMIO VOCE ACABA DE GANHAR UM ITEM:`` ✨ **HEROIC** ✨\n{response.upper()}"
        else:
            empty = None

        if rarity.lower() in ["ultra raro", "secret"]:
            if vip:
                return (f"``{quant_1}`` - **{item['data'][1]}**\n"
                        f"**+{quant_2}** - {self.items[bonus_1][1]} | "
                        f"**+{quant_3}** - {self.items[bonus_2][1]}", empty)

            return (f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCE TIROU:``\n"
                    f"``{quant_1}`` {item['data'][0]} **{item['data'][1]}** "
                    f"``ELE TEM O TIER`` ✨ **{rarity.upper()}** ✨\n"
                    f"``+{quant_2}`` {self.items[bonus_1][0]} **{self.items[bonus_1][1]}** | "
                    f"``+{quant_3}`` {self.items[bonus_2][0]} **{self.items[bonus_2][1]}**", empty)

        if vip:
            return (f"**{quant_1}** - {item['data'][1]}\n"
                    f"**+{quant_2}** - {self.items[bonus_1][1]} | "
                    f"**+{quant_3}** - {self.items[bonus_2][1]}", empty)

        return (f"<:mito:745375589145247804>│``VOCE TIROU:``\n"
                f"``{quant_1}`` {item['data'][0]} **{item['data'][1]}** "
                f"``ELE TEM O TIER`` **{rarity.upper()}**\n"
                f"``+{quant_2}`` {self.items[bonus_1][0]} **{self.items[bonus_1][1]}** | "
                f"``+{quant_3}`` {self.items[bonus_2][0]} **{self.items[bonus_2][1]}**", empty)
