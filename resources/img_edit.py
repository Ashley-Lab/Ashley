import re
import json
import textwrap
import requests
import unicodedata

from io import BytesIO
from random import choice
from PIL import Image, ImageDraw, ImageFont, ImageOps

letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
           't', 'u', 'v', 'w', 'x', 'y', 'z')
avatar_marry = None

with open("data/pets.json", encoding="utf-8") as pets:
    pets = json.load(pets)


def calc_xp(xp, lvl):
    experience_now = xp
    lvl_now = lvl
    experience = experience_now
    lvl_guess = lvl_now + 1
    while True:
        lvl_next = int(experience ** 0.2)
        if lvl_now < lvl_next:
            lvl_now = lvl_next
            if lvl_now == lvl_guess:
                xp_ = experience
                break
        experience += 1
    percent = int(experience_now * 100 / xp_)
    return int(percent / 2), xp_


def remove_acentos_e_caracteres_especiais(word):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', word)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z \\\]', '', palavra_sem_acento)


def get_avatar(avatar_url, x, y):
    url_avatar = requests.get(avatar_url)
    avatar = Image.open(BytesIO(url_avatar.content)).convert('RGBA')
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
    show.text(xy=(x + 2, y + 2), text=key, fill=(0, 0, 0), font=font_key)
    show.text(xy=(x, y), text=key, fill=(255, 255, 255), font=font_key)

    # alinhamento do retangulo 2
    w, h = show.textsize(time, font=font_time)
    x = (x4 - x3 - w) / 2 + x3
    y = (y4 - y3 - h) / 2 + y3 + 1
    show.text(xy=(x + 2, y + 2), text=time, fill=(0, 0, 0), font=font_time)
    show.text(xy=(x, y), text=time, fill=(255, 255, 255), font=font_time)

    image.save('giftcard.png')


def profile(data_):
    # load dashboard image
    global avatar_marry
    image = Image.open("images/dashboards/profile.png").convert('RGBA')
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
    avatar_user = get_avatar(data_['avatar_member'], 119, 119)
    if data_['avatar_married'] is not None:
        avatar_marry = get_avatar(data_['avatar_married'], 122, 122)

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

        'relics/anel': [(108, 293)],
        'relics/balança': [(161, 293)],
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
        if k[k.find("/"):] in data_['artifacts']:
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
                width = size * 1.2
            elif len(data_[k]) <= 100:
                size = 24
                width = size * 1.4
            elif len(data_[k]) <= 150:
                size = 22
                width = size * 1.6
            else:
                size = 20
                width = size * 1.8

            font_text_about = ImageFont.truetype("fonts/times.ttf", size)
            msg = textwrap.wrap(data_[k], width=width)
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
            x_, y_ = text_align(rectangles[k], data_[k][1], font_text_vip)
            show.text(xy=(x_ + 1, y_ + 1), text=data_[k][1].upper(), fill=(255, 255, 255), font=font_text_vip)
            show.text(xy=(x_, y_), text=data_[k][1].upper(), fill=(68, 29, 114), font=font_text_vip)
        else:
            font_s = font_number if k in font_ else font_text
            if k == "xp":
                data_[k] += " / " + str(percent[1])
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
