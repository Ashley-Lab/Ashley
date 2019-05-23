from random import randint, choice


class Booster(object):
    def __init__(self, items_):
        self.items = items_
        self.ranking = None
        self.is_vip = None
        self.item_ = None
        self.legend = {"Comum": 0, "Normal": 1, "Raro": 2, "Super Raro": 3, "Ultra Raro": 4, "Secret": 5}
        self.booster_choice = None
        self.booster_bronze = {"Comum": 60, "Normal": 28, "Raro": 6, "Super Raro": 3, "Ultra Raro": 2, "Secret": 1}
        self.booster_silver = {"Comum": 60, "Normal": 28, "Raro": 6, "Super Raro": 3, "Ultra Raro": 2, "Secret": 1}
        self.booster_gold = {"Comum": 60, "Normal": 28, "Raro": 6, "Super Raro": 3, "Ultra Raro": 2, "Secret": 1}
        self.booster_vip = {"Comum": 60, "Normal": 28, "Raro": 6, "Super Raro": 3, "Ultra Raro": 2, "Secret": 1}
        self.booster_secret = {"Comum": 60, "Normal": 28, "Raro": 6, "Super Raro": 3, "Ultra Raro": 2, "Secret": 1}
        self.box = {"status": {"secret": 0, "ur": 0, "sr": 0, "r": 0, "n": 0, "c": 0}}

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
        self.box = {"status": {"secret": 0, "ur": 0, "sr": 0, "r": 0, "n": 0, "c": 0}}
        self.box_count = 0
        self.secret = 0
        self.ur = 0
        self.sr = 0
        self.r = 0
        self.n = 0
        self.c = 0

    def create_booster(self, ranking, is_vip):
        self.reset_counts()
        self.ranking = ranking
        self.is_vip = is_vip
        while self.box_count < 200:
            item = choice(self.items.keys())
            if self.items[item][3] == 5:
                if self.secret < self.l_secret:
                    if item not in self.box:
                        list_ = self.items[item]
                        list_.append(1)
                        self.box[item] = list_
                    self.secret += 1
                    self.box_count += 1
            elif self.items[item][3] == 4:
                if self.ur < self.l_ur:
                    if item not in self.box:
                        list_ = self.items[item]
                        list_.append(1)
                        self.box[item] = list_
                    else:
                        self.box[item][-1] += 1
                    self.ur += 1
                    self.box_count += 1
            elif self.items[item][3] == 3:
                if self.sr < self.l_sr:
                    if item not in self.box:
                        list_ = self.items[item]
                        list_.append(1)
                        self.box[item] = list_
                    else:
                        self.box[item][-1] += 1
                    self.sr += 1
                    self.box_count += 1
            elif self.items[item][3] == 2:
                if self.r < self.l_r:
                    if item not in self.box:
                        list_ = self.items[item]
                        list_.append(1)
                        self.box[item] = list_
                    else:
                        self.box[item][-1] += 1
                    self.r += 1
                    self.box_count += 1
            elif self.items[item][3] == 1:
                if self.n < self.l_n:
                    if item not in self.box:
                        list_ = self.items[item]
                        list_.append(1)
                        self.box[item] = list_
                    else:
                        self.box[item][-1] += 1
                    self.n += 1
                    self.box_count += 1
            elif self.items[item][3] == 0:
                if self.c < self.l_c:
                    if item not in self.box:
                        list_ = self.items[item]
                        list_.append(1)
                        self.box[item] = list_
                    else:
                        self.box[item][-1] += 1
                    self.c += 1
                    self.box_count += 1
        return self.box

    def buy_item(self, box, ranking, is_vip):
        self.ranking = ranking
        self.is_vip = is_vip

        if self.ranking == "Bronze":
            self.booster_choice = self.booster_bronze
        elif self.ranking == "Silver":
            self.booster_choice = self.booster_silver
        elif self.ranking == "Gold":
            self.booster_choice = self.booster_gold

        if self.is_vip:
            self.booster_choice = self.booster_bronze

        chance = randint(1, 100)
        if chance == 100:
            self.booster_choice = self.booster_secret

        list_items = []
        for item, amount in self.booster_choice.items():
            list_items += [item] * amount
        result = choice(list_items)

        self.item_ = choice(box)
        while list(self.legend.keys())[list(self.legend.values()).index(self.item_[-2])] != result:
            self.item_ = choice(box)

        return self.item_
