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

        if validity:
            await bot.db.delete_data({"_id": _id}, "gift")

        ethernyas = randint(500, 1000)
        coins = randint(10, 30)
        items = ['crystal_fragment_light', 'crystal_fragment_enery', 'crystal_fragment_dark']

        rare = None
        chance = randint(1, 100)
        if chance <= 10:
            all_i = config['items']
            rare = choice([x for x in all_i.keys() if all_i[x][3] == 3 or all_i[x][3] == 4])

        return {"money": ethernyas, "coins": coins, "items": items, "rare": rare, "validity": validity}

    else:
        return None
