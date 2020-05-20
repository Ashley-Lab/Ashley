from random import choice


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


def register_gift(bot, time):
    while True:
        gift_t, _id = generate_gift()
        data = bot.db.get_data("_id", _id, "gift")
        if data is None:
            data = {"_id": _id, "gift_t": gift_t, "validity": time}
            bot.db.push_data(data, "cooldown")
            return gift_t


def open_gift(bot, gift_t):
    data = bot.db.get_data("gift_t", gift_t, "gift")
    if data is not None:
        _id = data['_id']
        bot.db.delete_data({"_id": _id}, "gift")
        return [0]
    else:
        return None
