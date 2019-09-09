from random import randint, choice


class Booster(object):
    def __init__(self, items_):
        self.items = items_
        self.ranking = None
        self.is_vip = None
        self.item_ = None
        self.key_item = None

        # box configs
        self.box = {"status": {"active": True, "secret": 0, "ur": 0, "sr": 0, "r": 0, "n": 0, "c": 0}}
        self.legend = {"Comum": 0, "Normal": 1, "Raro": 2, "Super Raro": 3, "Ultra Raro": 4, "Secret": 5}
        self.bl = {"Comum": "c", "Normal": "n", "Raro": "r", "Super Raro": "sr", "Ultra Raro": "ur", "Secret": "secret"}
        self.rarity = {"Comum": 500, "Normal": 400, "Raro": 300, "Super Raro": 200, "Ultra Raro": 150, "Secret": 100}

        # booster configs
        self.booster_choice = None
        self.booster_bronze = {"Comum": 95, "Normal": 1, "Raro": 1, "Super Raro": 1, "Ultra Raro": 1, "Secret": 1}
        self.booster_silver = {"Comum": 60, "Normal": 36, "Raro": 1, "Super Raro": 1, "Ultra Raro": 1, "Secret": 1}
        self.booster_gold = {"Comum": 50, "Normal": 46, "Raro": 1, "Super Raro": 1, "Ultra Raro": 1, "Secret": 1}
        self.booster_vip = {"Comum": 50, "Normal": 30, "Raro": 15, "Super Raro": 3, "Ultra Raro": 1, "Secret": 1}
        self.booster_secret = {"Comum": 40, "Normal": 30, "Raro": 20, "Super Raro": 7, "Ultra Raro": 2, "Secret": 1}

        # contadores de itens
        self.secret = 0
        self.ur = 0
        self.sr = 0
        self.r = 0
        self.n = 0
        self.c = 0

        # contador de itens por box
        self.box_count = 0

        # Limites dos itens
        self.l_secret = 1
        self.l_ur = 2 * len([x for x in self.items.keys() if self.items[x][3] == 4])
        self.l_sr = 3 * len([x for x in self.items.keys() if self.items[x][3] == 3])
        self.l_r = 6 * len([x for x in self.items.keys() if self.items[x][3] == 2])
        self.l_n = 28 * len([x for x in self.items.keys() if self.items[x][3] == 1])
        self.l_c = 60 * len([x for x in self.items.keys() if self.items[x][3] == 0])

    def reset_counts(self):
        self.box = {"status": {"active": True, "secret": 0, "ur": 0, "sr": 0, "r": 0, "n": 0, "c": 0}}
        self.box_count = 0
        self.secret = 0
        self.ur = 0
        self.sr = 0
        self.r = 0
        self.n = 0
        self.c = 0

    def create_box(self):
        self.reset_counts()
        rarity = choice(list(self.rarity.keys()))
        size = self.rarity[rarity]
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
                if self.n < self.l_n:
                    if item not in self.box['items']:
                        self.box['items'][item] = {"size": 1, "data": self.items[item]}
                        self.box['status']['n'] += 1
                    else:
                        self.box['items'][item]['size'] += 1
                        self.box['status']['n'] += 1
                    self.n += 1
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

    async def buy_box(self, bot, ctx):
        data = bot.db.get_data("user_id", ctx.author.id, "users")
        if data['treasure']['bronze'] > 5000:
            answer = await bot.db.take_money(ctx, 'bronze', 5000)
        elif data['treasure']['silver'] > 500:
            answer = await bot.db.take_money(ctx, 'silver', 500)
        elif data['treasure']['gold'] > 50:
            answer = await bot.db.take_money(ctx, 'gold', 50)
        else:
            return await ctx.send("<:alert_status:519896811192844288>│``VOCÊ NÃO TEM DINHEIRO PARA COMPRAR OU RESETAR "
                                  "A BOX!\nVOCÊ PRECISA DE 5.000 BRONZE, 500 SILVER OU 50 GOLD PARA COMPRAR.``")
        data = bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        box = self.create_box()
        update['box'] = box
        bot.db.update_data(data, update, 'users')
        await ctx.send(answer)
        await ctx.send("```A BOX ENCONTRA-SE NA SUA CONTA!```")

    def buy_item(self, box_, ranking, is_vip):
        self.ranking = ranking
        self.is_vip = is_vip

        if self.ranking == "Bronze":
            self.booster_choice = self.booster_bronze
        elif self.ranking == "Silver":
            self.booster_choice = self.booster_silver
        elif self.ranking == "Gold":
            self.booster_choice = self.booster_gold

        if self.is_vip:
            self.booster_choice = self.booster_vip

        chance = randint(1, 100)
        if chance == 100:
            self.booster_choice = self.booster_secret

        list_items = []
        for i_, amount in self.booster_choice.items():
            list_items += [i_] * amount

        while True:
            result = choice(list_items)
            if box_['status'][self.bl[result]] > 0:
                self.item_ = choice(list(box_['items'].values()))
                while list(self.legend.keys())[list(self.legend.values()).index(self.item_['data'][3])] != result:
                    self.item_ = choice(list(box_['items'].values()))
                break

        return self.item_

    async def buy_booster(self, bot, ctx):
        data = bot.db.get_data("user_id", ctx.author.id, "users")
        try:
            if data['box']['status']['active']:
                pass
            else:
                await ctx.send("<:alert_status:519896811192844288>│``VOCÊ NAO TEM UMA BOX ATIVA NA SUA CONTA!``")
        except KeyError:
            await ctx.send("<:alert_status:519896811192844288>│``VOCÊ PRECISA COMPRAR UMA BOX PARA PODER COMPRAR "
                           "BOOSTERS!")
        if data['treasure']['bronze'] > 100:
            answer = await bot.db.take_money(ctx, 'bronze', 100)
        elif data['treasure']['silver'] > 10:
            answer = await bot.db.take_money(ctx, 'silver', 10)
        elif data['treasure']['gold'] > 1:
            answer = await bot.db.take_money(ctx, 'gold', 1)
        else:
            return await ctx.send("<:alert_status:519896811192844288>│``VOCÊ NÃO TEM DINHEIRO PARA COMPRAR UM BOOSTER"
                                  "\nVOCÊ PRECISA DE 100 BRONZE, 10 SILVER OU 1 GOLD PARA COMPRAR.``")
        data = bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        item = self.buy_item(data['box'], data['user']['ranking'], data['config']['vip'])
        for k, v in self.items.items():
            if v == item['data']:
                self.key_item = k
        rarity = list(self.legend.keys())[list(self.legend.values()).index(item['data'][3])]
        update['box']['status'][self.bl[rarity]] -= 1
        update['box']['status']['size'] -= 1
        update['box']['items'][self.key_item]['size'] -= 1
        try:
            update['inventory'][self.key_item] += 1
        except KeyError:
            update['inventory'][self.key_item] = 1
        if update['box']['status']['size'] <= 0:
            update['box']['status']['active'] = False
        bot.db.update_data(data, update, 'users')
        await ctx.send(answer)
        await ctx.send(f"``O ITEM ``{item['data'][0]}**{item['data'][1]}** ``ENCONTRA-SE NO SEU INVENTÁRIO!``\n``ELE "
                       f"TEM O TIER`` **{rarity.upper()}**")
