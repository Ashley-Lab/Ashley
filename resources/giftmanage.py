from random import choice, randint
from config import data as config
from resources.verify_cooldown import verify_cooldown


def generate_gift():
    gentype = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = ['AySeHlLhEsYa', 'aYsEhLlHeSyA']
    lgt = list()
    gift = str()
    fgift = str()
    for L in key[choice([0, 1])]:
        lgt.append(L.upper())
        lgt.append(ord(L))
    for c in range(len(lgt)):
        if c % 2 == 0:
            gift += str(lgt[c])
        else:
            gift += str(choice(gentype))
    for L in range(len(gift)):
        if L % 5 == 0 and L != 0:
            fgift += '-'
        fgift += gift[L]
    fgift += str(choice(gentype))
    gift += fgift[-1]
    return fgift, gift


async def register_gift(bot, time):
    while True:
        gift_t, _id = generate_gift()
        data = await bot.db.get_data("_id", _id, "gift")
        if data is None:
            data = {"_id": _id, "gift_t": gift_t, "validity": time}
            await bot.db.push_data(data, "gift")
            if not await verify_cooldown(bot, _id, time):
                return gift_t


async def open_gift(bot, gift):
    if "-" in gift:
        key = "gift_t"
    else:
        key = "_id"

    data = await bot.db.get_data(key, gift, "gift")

    if data is not None:

        _id = data['_id']
        time = data['validity']

        if await verify_cooldown(bot, _id, time, True):
            validity = True
        else:
            validity = False

        ethernyas = randint(250, 300)
        coins = randint(50, 100)
        items = ['crystal_fragment_light', 'crystal_fragment_energy', 'crystal_fragment_dark', 'Energy']

        rare = None
        chance = randint(1, 100)
        if chance <= 50:
            item_1 = choice(['Unearthly', 'Surpassing', 'Hurricane', 'Heavenly', 'Blazing', 'Augur'])
            item_2 = choice(['Crystal_of_Energy', 'Discharge_Crystal', 'Acquittal_Crystal'])
            item_3 = choice(['SoulStoneYellow', 'SoulStoneRed', 'SoulStonePurple', 'SoulStoneGreen',
                             'SoulStoneDarkGreen', 'SoulStoneBlue'])
            rare = [item_1, item_2, item_3]

            if chance < 15:
                item_plus = choice(["soul_crystal_of_love", "soul_crystal_of_love", "soul_crystal_of_love",
                                    "soul_crystal_of_hope", "soul_crystal_of_hope", "soul_crystal_of_hope",
                                    "soul_crystal_of_hate", "soul_crystal_of_hate", "soul_crystal_of_hate",
                                    "fused_diamond", "fused_diamond", "fused_ruby", "fused_ruby",
                                    "fused_sapphire", "fused_sapphire", "fused_emerald", "fused_emerald",
                                    "unsealed_stone", "melted_artifact"])
                rare.append(item_plus)

        return {"money": ethernyas, "coins": coins, "items": items, "rare": rare, "validity": validity}

    else:
        return None
