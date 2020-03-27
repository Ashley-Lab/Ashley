import time
import random


def id_creator():
    date = time.localtime()
    id_ = ''
    for c in range(6):
        if c == 5:
            num = str(random.randint(1, 999))
            if len(num) < 2:
                num = f"00{num}"
            elif len(num) < 3:
                num = f"0{num}"
            id_ += num
        else:
            id_ += str(date[c])
    return int(id_)


def skill_level():
    level = random.randint(1, 10)
    return level


def choice_equips(bot):
    set_equips = list()
    for c in range(5):
        armor_name = random.choice(list(bot.config['set_equips'].keys()))
        set_armor = bot.config['set_equips'][armor_name]
        set_equips.append((set_armor['set'][c], armor_name))
    armor = {"breastplate": set_equips[0], "leggings": set_equips[1], "boots": set_equips[2],
             "gloves": set_equips[3], "shoulder": set_equips[4]}
    return armor


class_ = random.choice(['paladin', 'necromancer', 'wizard', 'warrior', 'priest', 'warlock', 'assassin', 'default'])
Class_rpg = {'Class': class_,
             'Name': None,
             'Status': {
                 'con': random.randint(14, 18),
                 'prec': random.randint(4, 8),
                 'agi': random.randint(4, 8),
                 'atk': random.randint(5, 10)
             },
             'XP': int(8000),
             'img': None,
             'itens': list()}
