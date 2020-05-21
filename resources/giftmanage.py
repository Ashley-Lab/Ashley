from random import choice, randint


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
    return fgift, gift


async def register_gift(bot, time):
    while True:
        gift_t, _id = generate_gift()
        data = await bot.db.get_data("_id", _id, "gift")
        if data is None:
            data = {"_id": _id, "gift_t": gift_t, "validity": time}
            await bot.db.push_data(data, "gift")
            return gift_t


async def open_gift(bot, gift):

    if "-" in gift:
        key = "gift_t"
    else:
        key = "_id"

    data = await bot.db.get_data(key, gift, "gift")

    if data is not None:
        _id = data['_id']
        await bot.db.delete_data({"_id": _id}, "gift")

        ethernyas = randint(1000, 3000)
        coins = randint(10, 50)
        items = ['crystal_fragment_light', 'crystal_fragment_enery', 'crystal_fragment_dark']

        return {"money": ethernyas, "coins": coins, "items": items}
    else:
        return None
