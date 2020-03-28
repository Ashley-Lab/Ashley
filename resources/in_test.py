import time
import random

from config import data


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


def skill_level(lvl):
    nivel = 1
    if 26 <= lvl <= 30:
        nivel = random.randint(1, 2)
    elif 31 <= lvl <= 35:
        nivel = random.randint(3, 4)
    elif 36 <= lvl <= 40:
        nivel = random.randint(5, 6)
    elif 41 <= lvl <= 45:
        nivel = random.randint(7, 8)
    elif 46 <= lvl <= 50:
        nivel = random.randint(9, 10)
    return nivel


def choice_equips(bot):
    set_equips = list()
    for c in range(5):
        armor_name = random.choice(list(bot.config['set_equips'].keys()))
        set_armor = bot.config['set_equips'][armor_name]
        set_equips.append((set_armor['set'][c], armor_name))
    armor = {"breastplate": set_equips[0], "leggings": set_equips[1], "boots": set_equips[2],
             "gloves": set_equips[3], "shoulder": set_equips[4]}
    return armor


def choice_mods():
    mods = random.choice([random.randint(1, 2), random.randint(3, 4), random.randint(5, 6), random.randint(7, 8),
                          random.randint(9, 10)])
    return mods


def chance_skill(level_skill):
    if level_skill <= 1:
        skill_chance = 100
    elif level_skill <= 2:
        skill_chance = 99
    elif level_skill <= 3:
        skill_chance = 98
    elif level_skill <= 4:
        skill_chance = 97
    elif level_skill <= 5:
        skill_chance = 96
    elif level_skill <= 6:
        skill_chance = 95
    elif level_skill <= 7:
        skill_chance = 94
    elif level_skill <= 8:
        skill_chance = 93
    elif level_skill <= 9:
        skill_chance = 92
    else:
        skill_chance = 91
    return skill_chance


class_ = random.choice(['paladin', 'necromancer', 'wizard', 'warrior', 'priest', 'warlock', 'assassin', 'default'])
Class_rpg = {'Class': class_,
             'Name': None,
             'Level': random.randint(26, 50),
             'Status': {
                 'con': data['skills'][class_]['modifier']['con'] + 5 + choice_mods(),
                 'prec': data['skills'][class_]['modifier']['prec'] + 5 + choice_mods(),
                 'agi': data['skills'][class_]['modifier']['agi'] + 5 + choice_mods(),
                 'atk': data['skills'][class_]['modifier']['atk'] + 5 + choice_mods(),
                 'luk': data['skills'][class_]['modifier']['luk'] + 0 + choice_mods(),
             },
             'XP': 10000,
             'img': None,
             'itens': list()}
