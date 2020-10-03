import re
import json
# import asyncio  // colocar para testes
import textwrap
import unicodedata

from io import BytesIO
from config import data  # tirar para testes...
from aiohttp_requests import requests
from random import choice
from PIL import Image, ImageDraw, ImageFont, ImageOps

avatar_marry = None
letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
           't', 'u', 'v', 'w', 'x', 'y', 'z')


regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def validate_url(url):
    return bool(regex.fullmatch(url))


with open("data/pets.json", encoding="utf-8") as pets:
    pets = json.load(pets)

with open("data/equips.json", encoding="utf-8") as _equips:
    _equips = json.load(_equips)


def calc_xp(xp, lvl):
    xp_now, xp_lvl_now, xp_lvl_back = xp, data['xp'][str(lvl)], data['xp'][str(lvl - 1 if lvl > 1 else 1)]
    try:
        percent = int(int((xp_now - xp_lvl_back) * 100 / (xp_lvl_now - xp_lvl_back)) / 2)
    except ZeroDivisionError:
        percent = 0
    return percent, xp_lvl_now, xp_lvl_back


def remove_acentos_e_caracteres_especiais(word):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', word)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z \\\]', '', palavra_sem_acento)


async def get_avatar(avatar_url, x, y):
    if validate_url(str(avatar_url)):
        link = str(avatar_url)
    else:
        link = "https://festsonho.com.br/images/sem_foto.png"
    url_avatar = await requests.get(link)
    avatar = Image.open(BytesIO(await url_avatar.read())).convert('RGBA')
    avatar = avatar.resize((x, y))
    big_avatar = (avatar.size[0] * 3, avatar.size[1] * 3)
    mascara = Image.new('L', big_avatar, 0)
    trim = ImageDraw.Draw(mascara)
    trim.ellipse((0, 0) + big_avatar, fill=255)
    mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
    avatar.putalpha(mascara)
    exit_avatar = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
    exit_avatar.putalpha(mascara)
    avatar = exit_avatar
    return avatar


def gift(key, time):
    # load image
    image = Image.open("images/dashboards/giftart.png").convert('RGBA')
    show = ImageDraw.Draw(image)

    # load fonts
    font_key = ImageFont.truetype("fonts/gift.otf", 18)
    font_time = ImageFont.truetype("fonts/bot.otf", 24)

    # retangulos dos textos
    rectangle_1 = [5, 46, 394, 83]
    rectangle_2 = [88, 191, 312, 156]
    x1, y1, x2, y2 = rectangle_1
    x3, y3, x4, y4 = rectangle_2

    # bordas dos retangulos
    show.rectangle([x1, y1, x2, y2])
    show.rectangle([x3, y3, x4, y4])

    # alinhamento do retangulo 1
    w, h = show.textsize(key, font=font_key)
    x = (x2 - x1 - w) / 2 + x1 + 3
    y = (y2 - y1 - h) / 2 + y1 + 3
    show.text(xy=(x + 1, y + 1), text=key, fill=(0, 0, 0), font=font_key)
    show.text(xy=(x, y), text=key, fill=(255, 255, 255), font=font_key)

    # alinhamento do retangulo 2
    w, h = show.textsize(time, font=font_time)
    x = (x4 - x3 - w) / 2 + x3
    y = (y4 - y3 - h) / 2 + y3 + 1
    show.text(xy=(x + 1, y + 1), text=time, fill=(255, 255, 255), font=font_time)
    show.text(xy=(x, y), text=time, fill=(68, 29, 114), font=font_time)

    image.save('giftcard.png')


async def profile(data_):
    # load dashboard image
    global avatar_marry
    image = Image.open("images/dashboards/profile.png").convert('RGBA')
    if len(data_['artifacts'].keys()) == 24:
        like = choice(['profile_obelisk', 'profile_ra', 'profile_slifer'])
        image = Image.open(f"images/dashboards/{like}.png").convert('RGBA')
    show = ImageDraw.Draw(image)

    # load fonts
    font_number = ImageFont.truetype("fonts/times.ttf", 24)
    font_text = ImageFont.truetype("fonts/bot.otf", 24)

    # take pet
    if data_['pet'] is not None:
        pet = pets[data_['pet']]
        if pet['colour'][0] is True:
            pet_c = choice(pet['colour'][2])
            indice = pet['colour'][2].index(pet_c)
            mask = choice(letters[:pet['mask'][indice]])
            link_ = f"images/pet/{data_['pet']}/{pet_c}/mask_{mask}.png"
        else:
            mask = choice(letters[:pet['mask'][0]])
            link_ = f"images/pet/{data_['pet']}/mask_{mask}.png"
    else:
        link_ = None

    # take avatar member
    avatar_user = await get_avatar(data_['avatar_member'], 119, 119)
    if data_['avatar_married'] is not None:
        avatar_marry = await get_avatar(data_['avatar_married'], 122, 122)

    # take artifacts img
    artifacts = {
        'armors/aquario': [(30, 532)],
        'armors/aries': [(81, 532)],
        'armors/cancer': [(133, 532)],
        'armors/capricornio': [(185, 532)],
        'armors/escorpiao': [(30, 462)],
        'armors/gemeos': [(81, 462)],
        'armors/leao': [(133, 462)],
        'armors/peixes': [(185, 462)],
        'armors/sargitario': [(30, 390)],
        'armors/libra': [(81, 390)],
        'armors/touro': [(133, 390)],
        'armors/virgem': [(185, 390)],

        'exodia/braço_direito': [(49, 45)],
        'exodia/braço_esquerdo': [(162, 45)],
        'exodia/perna_direita': [(75, 120)],
        'exodia/perna_esquerda': [(135, 120)],
        'exodia/the_one': [(106, 45)],

        'relics/anel': [(161, 293)],
        'relics/balança': [(108, 293)],
        'relics/chave': [(53, 293)],
        'relics/colar': [(185, 222)],
        'relics/enigma': [(133, 222)],
        'relics/olho': [(81, 222)],
        'relics/vara': [(30, 222)]
    }

    for key in artifacts.keys():
        img = Image.open(f"images/artifacts/{key}.png").convert('RGBA')
        img = img.resize((39, 57))
        artifacts[key].append(img)

    # add img to main img
    image.paste(avatar_user, (278, 7), avatar_user)
    if data_['avatar_married'] is not None:
        image.paste(avatar_marry, (665, 439), avatar_marry)

    # add percent to bar xp
    percent = calc_xp(int(data_["xp"]), int(data_["level"]))
    percent_img = Image.open("images/elements/1porcent.png").convert('RGBA')
    w_percent, h_percent = percent_img.size
    ini_x, ini_y = 540, 8
    for n in range(percent[0]):
        image.paste(percent_img, (ini_x, ini_y), percent_img)
        ini_x += w_percent

    for k in artifacts.keys():
        if k[k.find("/") + 1:] in data_['artifacts'].keys():
            image.paste(artifacts[k][1], (artifacts[k][0][0], artifacts[k][0][1]), artifacts[k][1])

    # rectangles' texts
    rectangles = {
        "xp": [540, 8, 940, 29],
        "level": [942, 2, 996, 34],
        "vip": [590, 33, 941, 51],
        "rec": [645, 66, 755, 87],
        "coin": [832, 67, 940, 88],
        "commands": [422, 92, 565, 162],
        "entitlement": [281, 209, 564, 312],
        "name": [583, 107, 972, 141],
        "about": [583, 142, 972, 319],
        "wallet": [766, 327, 972, 348],
        "pet": [857, 425, 971, 574],
    }

    # Text Align
    def text_align(box, text, font_t):
        nonlocal show
        x1, y1, x2, y2 = box
        w, h = show.textsize(text.upper(), font=font_t)
        x = (x2 - x1 - w) // 2 + x1
        y = (y2 - y1 - h) // 2 + y1
        return x, y

    # font number select
    font_ = ['rec', 'coin', 'wallet', 'xp']

    # take vip img
    vip_xy = [[(280, 135), "images/elements/vip_member.png"], [(326, 135), "images/elements/vip_guild.png"],
              [(372, 135), "images/elements/vip_rpg.png"]]

    # add text to img
    for k in rectangles.keys():
        if k == "pet":
            if link_ is not None:
                pet = Image.open(link_).convert('RGBA')
                width_, height_ = pet.size
                pet = pet.resize(((width_ * 40 // 100), (height_ * 40 // 100)))
                x1_p, y1_p, x2_p, y2_p = rectangles[k]
                w_p, h_p = pet.size
                x_p = (x2_p - x1_p - w_p) // 2 + x1_p
                y_p = (y2_p - y1_p - h_p) // 2 + y1_p
                image.paste(pet, (x_p + 35, y_p + 5), pet)
        elif k == "about":
            if len(data_[k]) <= 50:
                size = 26
                if len(data_[k].split()) <= 5:
                    size = 21
                width = size * 1.2
            elif len(data_[k]) <= 100:
                size = 24
                if len(data_[k].split()) <= 5:
                    size = 19
                width = size * 1.4
            elif len(data_[k]) <= 150:
                size = 22
                if len(data_[k].split()) <= 5:
                    size = 17
                width = size * 1.6
            else:
                size = 20
                if len(data_[k].split()) <= 5:
                    size = 15
                width = size * 1.8

            font_text_about = ImageFont.truetype("fonts/times.ttf", size)
            msg = textwrap.wrap(data_[k], width=int(width))
            x_s1, y_s1, x_s2, y_s2 = rectangles[k]
            current_h = (y_s2 - y_s1) / 2 + width
            for line in msg:
                w_s, h_s = show.textsize(line, font=font_text_about)
                x_s = (x_s2 - x_s1 - w_s) / 2 + x_s1
                y_s = (y_s2 - y_s1 - current_h) / 2 + y_s1
                show.text((x_s + 1, y_s + 1), line, align='center', font=font_text_about, fill=(255, 255, 255))
                show.text((x_s, y_s), line, align='center', font=font_text_about, fill=(68, 29, 114))
                current_h -= h_s + size
        elif k == "vip":
            _ = 0
            for vip in data_[k][0]:
                if vip:
                    vip = Image.open(vip_xy[_][1]).convert('RGBA')
                    image.paste(vip, (vip_xy[_][0][0], vip_xy[_][0][1]), vip)
                _ += 1
            font_text_vip = ImageFont.truetype("fonts/bot.otf", 20)
            if not data_[k][0][0]:
                data_[k][1] = "VOCE NAO TEM VIP ATIVO"
            x_, y_ = text_align(rectangles[k], data_[k][1], font_text_vip)
            show.text(xy=(x_ + 1, y_ + 1), text=data_[k][1].upper(), fill=(255, 255, 255), font=font_text_vip)
            show.text(xy=(x_, y_), text=data_[k][1].upper(), fill=(68, 29, 114), font=font_text_vip)
        else:
            font_s = font_number if k in font_ else font_text
            if k == "xp":
                if data_[k] < 32:
                    new_xp = f"{data_[k]} / {percent[2]}      {percent[0] * 2} / 100%"
                else:
                    new_xp = f"{data_[k] - percent[2]} / {percent[1] - percent[2]}      {percent[0] * 2} / 100%"
                data_[k] = new_xp
            x_, y_ = text_align(rectangles[k], data_[k], font_s)
            if font_s == font_text:
                if k == "entitlement":
                    font_s = font_text = ImageFont.truetype("fonts/bot.otf", 30)
                if k == "commands":
                    font_s = font_text = ImageFont.truetype("fonts/bot.otf", 28)
                show.text(xy=(x_ + 1, y_ + 1), text=data_[k].upper(), fill=(0, 0, 0), font=font_s)
                show.text(xy=(x_, y_), text=data_[k].upper(), fill=(255, 255, 255), font=font_s)
            else:
                if k != "wallet":
                    y_ = y_ - 2
                show.text(xy=(x_ + 1, y_ + 1), text=data_[k].upper(), fill=(255, 255, 255), font=font_s)
                show.text(xy=(x_, y_), text=data_[k].upper(), fill=(68, 29, 114), font=font_s)

    # save image
    image.save('profile.png')


async def skill_points(database):
    # load dashboard image
    image = Image.open("images/dashboards/skill_point.png").convert('RGBA')
    show = ImageDraw.Draw(image)

    # Text Align
    def text_align(box, text, font_t):
        nonlocal show
        x1, y1, x2, y2 = box
        w, h = show.textsize(text.upper(), font=font_t)
        x = (x2 - x1 - w) // 2 + x1
        y = (y2 - y1 - h) // 2 + y1
        return x, y

    # rectangles' texts
    rectangles = {
        "xp": [292, 15, 693, 37],
        "level": [693, 11, 747, 42],
        "class": [160, 103, 325, 141],
        "name": [153, 147, 668, 186],

        "atk": [340, 85, 405, 137],
        "dex": [428, 85, 493, 137],
        "acc": [520, 85, 585, 137],
        "con": [615, 85, 680, 137],
        "luk": [709, 85, 774, 137],

        "pdh": [33, 506, 120, 585]}

    # locate of skills
    skills = {
        "01-d1": [212, 235, 260, 283],
        "02-c1": [282, 235, 330, 283],
        "03-c1": [353, 235, 401, 283],
        "04-c1": [424, 235, 472, 283],
        "05-c1": [495, 235, 543, 283],
        "06-c1": [566, 235, 614, 283],

        "11-d2": [212, 306, 260, 354],
        "12-d2": [282, 306, 330, 354],
        "13-c2": [353, 306, 401, 354],
        "14-c2": [424, 306, 472, 354],
        "15-c2": [495, 306, 543, 354],
        "16-c2": [566, 306, 614, 354],

        "21-d3": [212, 377, 260, 425],
        "22-d3": [282, 377, 330, 425],
        "23-d3": [353, 377, 401, 425],
        "24-c3": [424, 377, 472, 425],
        "25-c3": [495, 377, 543, 425],
        "26-c3": [566, 377, 614, 425],

        "31-d4": [212, 447, 260, 495],
        "32-d4": [282, 447, 330, 495],
        "33-d4": [353, 447, 401, 495],
        "34-d4": [424, 447, 472, 495],
        "35-c4": [495, 447, 543, 495],
        "36-c4": [566, 447, 614, 495],

        "41-d5": [212, 519, 260, 567],
        "42-d5": [282, 519, 330, 567],
        "43-d5": [353, 519, 401, 567],
        "44-d5": [424, 519, 472, 567],
        "45-d5": [495, 519, 543, 567],
        "46-c5": [566, 519, 614, 567]
    }

    # add img to main img
    avatar_user = await get_avatar(database['avatar_member'], 132, 132)
    image.paste(avatar_user, (10, 13), avatar_user)

    # add img vip
    if database['vip']:
        vip = Image.open("images/elements/vip_rpg.png").convert('RGBA')
        image.paste(vip, (214, 57), vip)

    # add percent to bar xp
    percent = calc_xp(int(database['xp']), int(database['level']))  # XP / LEVEL
    percent_img = Image.open("images/elements/1porcent.png").convert('RGBA')
    w_percent, h_percent = percent_img.size
    ini_x, ini_y = 293, 16
    for n in range(percent[0]):
        image.paste(percent_img, (ini_x, ini_y), percent_img)
        ini_x += w_percent

    # add skill to img
    for k in skills.keys():
        c = database['class'] if k[3] == "c" else "default"
        skill = Image.open(f"images/skills/{c}/{k[4]}.jpg").convert('RGBA')
        skill = skill.resize((48, 48))
        image.paste(skill, (skills[k][0] + 1, skills[k][1] + 1), skill)

    # add text to img
    for k in rectangles.keys():
        if k == "xp":
            font_number = ImageFont.truetype("fonts/times.ttf", 24)
            if database[k] < 32:
                new_xp = f"{database[k]} / {percent[2]}      {percent[0] * 2} / 100%"
            else:
                new_xp = f"{database[k] - percent[2]} / {percent[1] - percent[2]}      {percent[0] * 2} / 100%"
            database[k] = new_xp
            x_, y_ = text_align(rectangles[k], database[k], font_number)
            show.text(xy=(x_ + 1, y_ - 2), text=database[k].upper(), fill=(0, 0, 0), font=font_number)
            show.text(xy=(x_, y_ - 3), text=database[k].upper(), fill=(255, 255, 255), font=font_number)
        elif k == "level":
            font_number = ImageFont.truetype("fonts/times.ttf", 28)
            x_, y_ = text_align(rectangles[k], database[k], font_number)
            show.text(xy=(x_ + 1, y_ - 2), text=database[k].upper(), fill=(0, 0, 0), font=font_number)
            show.text(xy=(x_, y_ - 3), text=database[k].upper(), fill=(255, 255, 255), font=font_number)
        elif k in ['atk', 'dex', 'acc', 'con', 'luk']:
            font_number = ImageFont.truetype("fonts/times.ttf", 50)
            x_, y_ = text_align(rectangles[k], database[k], font_number)
            show.text(xy=(x_ + 1, y_ - 5), text=database[k].upper(), fill=(0, 0, 0), font=font_number)
            show.text(xy=(x_, y_ - 6), text=database[k].upper(), fill=(255, 255, 255), font=font_number)
        elif k == "pdh":
            font_number = ImageFont.truetype("fonts/times.ttf", 60)
            x_, y_ = text_align(rectangles[k], database[k], font_number)
            show.text(xy=(x_ + 1, y_ - 8), text=database[k].upper(), fill=(0, 0, 0), font=font_number)
            show.text(xy=(x_, y_ - 7), text=database[k].upper(), fill=(255, 255, 255), font=font_number)
        elif k == "name":
            font_text = ImageFont.truetype("fonts/bot.otf", 34)
            x_, y_ = text_align(rectangles[k], database[k], font_text)
            show.text(xy=(x_ + 1, y_ + 1), text=database[k].upper(), fill=(0, 0, 0), font=font_text)
            show.text(xy=(x_, y_), text=database[k].upper(), fill=(255, 255, 255), font=font_text)
        else:
            if database[k] == "necromancer":
                font_text = ImageFont.truetype("fonts/bot.otf", 23)
            else:
                font_text = ImageFont.truetype("fonts/bot.otf", 28)
            x_, y_ = text_align(rectangles[k], database[k], font_text)
            show.text(xy=(x_ + 1, y_ + 1), text=database[k].upper(), fill=(0, 0, 0), font=font_text)
            show.text(xy=(x_, y_), text=database[k].upper(), fill=(255, 255, 255), font=font_text)

    image.save("skill_points.png")


def equips(data_s):
    # load dashboard image
    image = Image.open(f"images/dashboards/equip_{data_s['class']}.png").convert('RGBA')
    show = ImageDraw.Draw(image)

    # Text Align
    def text_align(box, text, font_t):
        nonlocal show
        x1, y1, x2, y2 = box
        w, h = show.textsize(text.upper(), font=font_t)
        x = (x2 - x1 - w) // 2 + x1
        y = (y2 - y1 - h) // 2 + y1
        return x, y

    mapped = {

        "base": {
            "atk": (420, 108, 484, 160),
            "dex": (420, 207, 484, 260),
            "acc": (420, 307, 486, 361),
            "con": (420, 408, 486, 462),
            "luk": (420, 509, 486, 562)
        },

        "class": {
            "atk": (568, 109, 631, 160),
            "dex": (568, 207, 632, 260),
            "acc": (565, 307, 631, 361),
            "con": (565, 408, 631, 462),
            "luk": (565, 508, 631, 561)
        },

        "equip": {
            "atk": (716, 108, 779, 160),
            "dex": (716, 207, 780, 260),
            "acc": (716, 307, 782, 361),
            "con": (716, 408, 782, 461),
            "luk": (716, 509, 782, 561)
        },

        "name": (24, 18, 373, 67),

        "equipped": {
            "shoulder": (38, 92, 95, 147),
            "breastplate": (38, 183, 95, 238),
            "gloves": (38, 274, 95, 329),
            "leggings": (38, 365, 95, 420),
            "boots": (38, 456, 95, 511),
            "consumable": (170, 456, 227, 511),
            "sword": (302, 92, 359, 147),
            "shield": (302, 183, 359, 238),
            "necklace": (302, 274, 359, 239),
            "earring": (302, 365, 359, 420),
            "ring": (302, 456, 359, 511)
        }
    }

    for key in mapped.keys():
        if key in ['base', 'class', 'equip']:
            for k in mapped[key].keys():
                if k in ['atk', 'dex', 'acc', 'con', 'luk']:
                    font = ImageFont.truetype("fonts/times.ttf", 50)
                    x_, y_ = text_align(mapped[key][k], data_s[f"status_{key}"][k], font)
                    show.text(xy=(x_ + 1, y_ - 5), text=data_s[f"status_{key}"][k].upper(), fill=(0, 0, 0), font=font)
                    show.text(xy=(x_, y_ - 6), text=data_s[f"status_{key}"][k].upper(), fill=(255, 255, 255), font=font)
        if key == "name":
            font_text = ImageFont.truetype("fonts/bot.otf", 34)
            x_, y_ = text_align(mapped[key], data_s[key], font_text)
            show.text(xy=(x_ + 1, y_ + 1), text=data_s[key].upper(), fill=(0, 0, 0), font=font_text)
            show.text(xy=(x_, y_), text=data_s[key].upper(), fill=(255, 255, 255), font=font_text)

    eq = dict()
    for ky in _equips.keys():
        for k, v in _equips[ky].items():
            eq[k] = v

    # add equips to img
    for k in mapped["equipped"].keys():
        if data_s['equipped'][k] is not None:
            armor = ['shoulder', 'breastplate', 'gloves', 'leggings', 'boots']
            jewel = ['necklace', 'earring', 'ring']
            if k in armor or k == "shield":
                e_type = "armor"
            elif k in jewel:
                e_type = "jewel"
            elif k == "sword":
                e_type = "weapon"
            else:
                e_type = "consumable"
            if k in armor:
                f_t = f"{eq[data_s['equipped'][k]]['rarity']}/{data_s['equipped'][k]}"
            elif k == "sword" or k in jewel or k == "consumable":
                f_t = f"{data_s['equipped'][k]}"
            else:
                f_t = f"shield/{data_s['equipped'][k]}"
            equipped = Image.open(f"images/equips/{e_type}/{f_t}.jpg").convert('RGBA')
            equipped = equipped.resize((56, 56))
            image.paste(equipped, (mapped["equipped"][k][0] + 1, mapped["equipped"][k][1]), equipped)

    image.save("equips.png")


async def welcome(data_welcome):
    # load dashboard image
    image = Image.open(f"images/dashboards/{data_welcome['type']}.png").convert('RGBA')
    show = ImageDraw.Draw(image)

    # add img to main img
    avatar_user = await get_avatar(data_welcome['avatar'], 258, 258)
    image.paste(avatar_user, (383, 46), avatar_user)

    # Text Align
    def text_align(box, text, font_t):
        nonlocal show
        x1, y1, x2, y2 = box
        w, h = show.textsize(text.upper(), font=font_t)
        x = (x2 - x1 - w) // 2 + x1
        y = (y2 - y1 - h) // 2 + y1
        return x, y

    # rectangles' texts
    rectangles = {
        "name": [0, 367, 1023, 442],
        "text": [0, 443, 1023, 499],
    }

    # add text to img
    for k in rectangles.keys():
        if k == "name":
            color = (211, 36, 7) if data_welcome['type'] == "welcome" else (79, 0, 38)
            back_color = (255, 255, 255) if data_welcome['type'] == "welcome" else (255, 255, 255)
            font = ImageFont.truetype("fonts/bot.otf", 50)
            x_, y_ = text_align(rectangles[k], data_welcome[k], font)
            show.text(xy=(x_ + 1, y_ + 13), text=data_welcome[k].upper(), fill=back_color, font=font)
            show.text(xy=(x_, y_ + 12), text=data_welcome[k].upper(), fill=color, font=font)

        if k == "text" and data_welcome['type'] == "welcome":
            font = ImageFont.truetype("fonts/times.ttf", 24)
            x_, y_ = text_align(rectangles[k], data_welcome[k], font)
            show.text(xy=(x_, y_), text=data_welcome[k].upper(), fill=(255, 255, 255), font=font)

    image.save(f"{data_welcome['type']}.png")
