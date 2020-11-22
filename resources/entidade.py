import discord

from asyncio import sleep, TimeoutError
from resources.utility import embed_creator
from random import randint, choice
from config import data

_class = data['skills']
levels = [5, 10, 15, 20, 25]


class Entity(object):
    def __init__(self, db, is_player, pvp=False, raid=False):
        self.db = db
        self.name = self.db['name']
        self.status = self.db['status']
        self.xp = self.db['xp']
        self.lvl = self.db['level']
        self.effects = {}
        self.atacks = {}
        self.atack = None
        self.chance = False
        self.is_player = is_player
        self.pdef = self.db['pdef']
        self.mdef = self.db['mdef']
        self.img = self.db['img']
        self.ln = self.db['lower_net']
        self.pvp = pvp
        self.raid = raid
        self.ls = 0
        self.potion = 0

        if self.is_player:
            for c in range(5):
                if self.lvl >= levels[c]:
                    self.atacks[_class[self.db['next_class']][str(c)]['name']] = _class[self.db['next_class']][str(c)]
                else:
                    self.atacks[_class[self.db['class']][str(c)]['name']] = _class[self.db['class']][str(c)]

            self.rate = [_class[self.db['class']]['rate']['life'], _class[self.db['class']]['rate']['mana']]
            if self.db['level'] > 25:
                self.rate[0] += _class[self.db['next_class']]['rate']['life']
                self.rate[1] += _class[self.db['next_class']]['rate']['mana']

            self.status['hp'] = self.status['con'] * self.rate[0]
            self.status['mp'] = self.status['con'] * self.rate[1]
            self.level_skill = self.db['skills']

            if self.db['level'] > 25:
                self.cc = [_class[self.db['next_class']]['cc'], self.db['next_class']]
            else:
                self.cc = [_class[self.db['class']]['cc'], self.db['class']]

            self.p_class = self.db['next_class'] if self.db['level'] > 25 else self.db['class']

        else:

            if self.db['enemy']['level'] > 25:
                self.rate = [(12 + self.db['level'] // 10), (12 + self.db['level'] // 10)]
            else:
                self.rate = [(6 + self.db['level'] // 10), (6 + self.db['level'] // 10)]

            self.atacks = self.db['atacks']
            self.status['hp'] = self.status['con'] * self.rate[0]
            self.status['mp'] = self.status['con'] * self.rate[1]
            self.level_skill = 10
            self.cc = [self.db['cc'], "monster"]

    async def turn(self, enemy_info, bot, ctx, user=None, raid_num=0):
        user = ctx.author if user is None else user
        stun = False
        ice = False
        self.atack = None
        atacks = eval(str(self.atacks.keys()).replace('dict_keys(', '').replace(')', ''))
        try:
            effects = eval(str(self.effects.keys()).replace('dict_keys(', '').replace(')', ''))
        except KeyError:
            effects = None

        for c in ['stun', 'gelo']:
            try:
                if c in effects and self.effects[c]['turns'] > 0:
                    if c == "stun":
                        stun = True
                    if c == "gelo":
                        ice = True

            except KeyError:
                pass

        for c in [['fraquesa', 'fisico'], ['silencio', 'magico']]:
            if c[0] in effects:
                if self.effects[c[0]]['turns'] > 0:
                    for c2 in atacks:
                        if self.atacks[c2]['type'] == c[1]:
                            atacks.remove(c2)

        if stun is False and ice is False:
            if self.is_player:
                emojis = list()
                title = 'YOUR HP:  [{}/{}]  |  YOUR MP:  [{}/{}]\n--==>> OPPONENT: {}<<==--\n' \
                        '--==>> HP: [{}/{}] | LVL: {} <<==--'.format(self.status['hp'] if self.status['hp'] > 0 else 0,
                                                                     (self.status['con'] * self.rate[0]),
                                                                     self.status['mp'] if self.status['mp'] > 0 else 0,
                                                                     (self.status['con'] * self.rate[1]),
                                                                     enemy_info[2].upper(),
                                                                     enemy_info[0]['hp'] if enemy_info[0][
                                                                                                'hp'] > 0 else 0,
                                                                     enemy_info[0]['con'] * enemy_info[1][0],
                                                                     enemy_info[3])
                description = ''
                for c in range(0, len(atacks)):
                    lvs = self.level_skill[c]
                    self.ls = lvs if 0 <= lvs <= 9 else 9
                    c2, ls = atacks[c], self.ls
                    damage = int(self.status['atk'] * 2 / 100 * ((30 + (c * 5)) + (c * 10)))
                    dado = self.atacks[c2]['damage'][self.ls]
                    d1 = int(dado[:dado.find('d')])
                    d2 = int(dado[dado.find('d') + 1:])
                    dd = f"{f'{d2}-{d2 * d1}' if d2 != d2 * d1 else d2}"
                    if lvs >= 11:
                        dd = f'{d2 + int((lvs - 10) * 10)}-{d2 * d1}'
                    icon = self.atacks[c2]['icon']
                    skill_type = self.atacks[c2]['type']
                    emojis.append(self.atacks[c2]['icon'])

                    try:
                        effect_skill = str(self.atacks[c2]['effs'][self.ls].keys())
                    except KeyError:
                        effect_skill = "sem efeito"
                    except TypeError:
                        effect_skill = "sem efeito"

                    rm = int(((self.status['con'] * self.rate[1]) / 100) * 35)
                    ru = int(((self.status['con'] * self.rate[1]) / 100) * 50)
                    eff_mana = effect_skill.replace('dict_keys([', '').replace('])', '').replace('\'', '')
                    a_mana = self.atacks[c2]['mana'][self.ls] + self.lvl
                    a_mana = self.atacks[c2]['mana'][self.ls] + (self.lvl * 2) if self.lvl > 25 else a_mana
                    _mana = a_mana if eff_mana != "cura" else rm
                    _mana = ru if self.atacks[c2]['type'] == "especial" else _mana

                    description += f"{icon} **{c2.upper()}** ``+{lvs}``\n" \
                                   f"``Dano:`` {f'**{dd} + {damage}**' if ls > 0 else f'**{damage}**'}\n" \
                                   f"``Tipo:`` **{skill_type.upper()}**\n" \
                                   f"``Mana:`` **{_mana}**\n" \
                                   f"``Efeito(s):`` **{effect_skill}**" \
                                   f"\n\n".replace('dict_keys([', '').replace('])', '').replace('\'', '')

                regen = int(((self.status['con'] * self.rate[1]) / 100) * 50)
                description += f'<:MP:774699585620672534> **{"Pass turn MP".upper()}**\n' \
                               f'``MP Recovery:`` **+{regen} de Mana**\n\n' \
                               f'<:HP:774699585070825503> **{"Pass turn HP".upper()}**\n' \
                               f'``HP Recovery:`` **25-35% de HP**\n\n' \
                               f'<:fechar:749090949413732352> **Finalizar batalha**'
                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=0x000000
                )
                embed.set_thumbnail(url="{}".format(user.avatar_url))
                msg = await ctx.send(embed=embed)
                await sleep(0.5)
                for c in range(0, len(atacks)):
                    await msg.add_reaction(emojis[c])
                await msg.add_reaction('<:MP:774699585620672534>')
                await msg.add_reaction('<:HP:774699585070825503>')
                await msg.add_reaction('<:fechar:749090949413732352>')
                while not bot.is_closed():
                    try:
                        reaction = await bot.wait_for('reaction_add', timeout=60.0)
                        while reaction[1].id != user.id:
                            reaction = await bot.wait_for('reaction_add', timeout=60.0)
                    except TimeoutError:
                        return "COMANDO-CANCELADO"
                    emohp = "<:HP:774699585070825503>"
                    emomp = "<:MP:774699585620672534>"
                    emob = "<:fechar:749090949413732352>"
                    emoji_hp = str(emohp).replace('<:', '').replace(emohp[emohp.rfind(':'):], '')
                    emoji_mp = str(emomp).replace('<:', '').replace(emomp[emomp.rfind(':'):], '')
                    emoji_fb = str(emob).replace('<:', '').replace(emob[emob.rfind(':'):], '')
                    try:
                        if reaction[0].emoji.name == emoji_mp:
                            # regeneração de MP
                            regen = int(((self.status['con'] * self.rate[1]) / 100) * 50)
                            if (self.status['mp'] + regen) <= (self.status['con'] * self.rate[1]):
                                self.status['mp'] += regen
                            else:
                                self.status['mp'] = (self.status['con'] * self.rate[1])

                            self.atack = "PASS-TURN-MP"
                            break

                        potion_limit = 3 if not self.raid else 3 + (raid_num * 2)
                        if reaction[0].emoji.name == emoji_hp and self.potion < potion_limit:
                            # regeneração de HP
                            if self.p_class in ['priest', 'assassin', 'default']:
                                hp_regen = int(((self.status['con'] * self.rate[0]) / 100) * 35)

                            elif self.p_class in ['necromancer', 'wizard', 'warlock']:
                                hp_regen = int(((self.status['con'] * self.rate[0]) / 100) * 30)

                            else:
                                hp_regen = int(((self.status['con'] * self.rate[0]) / 100) * 25)

                            if (self.status['hp'] + hp_regen) <= (self.status['con'] * self.rate[0]):
                                self.status['hp'] += hp_regen
                            else:
                                self.status['hp'] = (self.status['con'] * self.rate[0])

                            self.atack = "PASS-TURN-HP"
                            self.potion += 1
                            break

                        if reaction[0].emoji.name == emoji_fb:
                            return "BATALHA-CANCELADA"

                    except AttributeError:
                        pass

                    potion_msg = False
                    for c in emojis:
                        emoji = str(c).replace('<:', '').replace(c[c.rfind(':'):], '')
                        try:
                            _reaction = reaction[0].emoji.name
                        except AttributeError:
                            _reaction = reaction[0].emoji
                        if _reaction == emoji or _reaction == emoji_hp:

                            if _reaction == emoji:
                                test_atack = emojis.index(f'<:{reaction[0].emoji.name}:{reaction[0].emoji.id}>')
                                _atack = atacks[test_atack]
                                lvs = self.level_skill[self.atacks[_atack]['skill'] - 1]
                                self.ls = lvs if 0 <= lvs <= 9 else 9
                                a_mana_1 = self.atacks[_atack]['mana'][self.ls] + self.lvl
                                a_mana_2 = self.atacks[_atack]['mana'][self.ls] + (self.lvl * 2)
                                remove = a_mana_2 if self.lvl > 25 else a_mana_1
                                try:
                                    effects_skill = [k for k, v in self.atacks[_atack]['effs'][self.ls].items()]
                                except TypeError:
                                    effects_skill = ['nenhum']
                                heal = False
                                for eff in effects_skill:
                                    if eff == "cura":
                                        heal = True
                                if heal:
                                    remove = int(((self.status['con'] * self.rate[1]) / 100) * 35)
                                if self.atacks[_atack]['type'] == "especial":
                                    remove = int(((self.status['con'] * self.rate[1]) / 100) * 50)
                            else:
                                remove = 10000
                                test_atack = None

                            potion_limit = 3 if not self.raid else 3 + (raid_num * 2)
                            if self.potion >= potion_limit and reaction[0].emoji.name == emoji_hp:
                                if self.raid:
                                    msg = f"``MATE OUTRO MONSTRO PARA AUMENTAR O SEU LIMITE, ESCOLHA UMA SKILL OU " \
                                          f"PASSE A VEZ...``\n**Obs:** Passar a vez regenera a mana ou vida!"
                                else:
                                    msg = f"``ENTÃO ESCOLHA UMA SKILL OU PASSE A VEZ...``\n" \
                                          f"**Obs:** Passar a vez regenera a mana ou vida!"
                                embed = discord.Embed(
                                    description=f"``{user.name.upper()} VOCÊ JA ATINGIU O LIMITE DE POÇÃO DE VIDA!``\n"
                                                f"{msg}", color=0x000000)
                                embed.set_thumbnail(url=f"{user.avatar_url}")
                                if not potion_msg:
                                    await ctx.send(embed=embed)
                                    potion_msg = True

                            elif self.status['mp'] >= remove:
                                self.status['mp'] -= remove
                                self.atack = atacks[test_atack]
                                break

                            else:
                                embed = discord.Embed(
                                    description=f"``{user.name.upper()} VOCÊ NÃO TEM MANA O SUFICIENTE!``\n"
                                                f"``ENTÃO ESCOLHA OUTRA SKILL OU PASSE A VEZ...``\n"
                                                f"**Obs:** Passar a vez regenera a mana ou vida!",
                                    color=0x000000
                                )
                                embed.set_thumbnail(url=f"{user.avatar_url}")
                                await ctx.send(embed=embed)

                    if self.atack is not None:
                        break
            else:
                self.atack = choice(atacks)
                embed = discord.Embed(
                    description=f"**{self.name.upper()}** ``ESCOLHEU O ATAQUE:`` **{self.atack.upper()}**",
                    color=0xf15a02
                )
                embed.set_thumbnail(url=f"{self.img}")
                await ctx.send(embed=embed)

            if self.atack is not None and self.atack not in ["PASS-TURN-MP", "PASS-TURN-HP"]:
                self.atack = self.atacks[self.atack]

        else:
            description = f'**{self.name.upper()}** ``esta`` **{"STUNADO" if stun else "CONGELADO"}**'
            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player
            img_ = "https://uploads1.yugioh.com/card_images/2110/detail/2004.jpg?1385103024"
            embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img, self.ln)
            await ctx.send(embed=embed_)

        try:
            if self.atack['effs'] is not None:
                if self.is_player:
                    lvs = self.level_skill[self.atack['skill'] - 1]
                    self.ls = lvs if 0 <= lvs <= 9 else 9
                    if self.atack['effs'][self.ls]['cura']['type'] == "cura":
                        percent = self.atack['effs'][self.ls]['cura']['damage']
                        regen = int(((self.status['con'] * self.rate[0]) / 100) * percent)
                        if (self.status['hp'] + regen) <= (self.status['con'] * self.rate[0]):
                            self.status['hp'] += regen
                        else:
                            self.status['hp'] = (self.status['con'] * self.rate[0])
                        desc = f'**{self.name.upper()}** ``recuperou`` **{regen}** ``de HP``'
                        hp = self.status['con'] * self.rate[0]
                        p = not self.is_player
                        await ctx.send(embed=embed_creator(desc, self.atack['img'], p, hp,
                                                           self.status['hp'], self.img, self.ln))
                        self.atack = None
                else:
                    if self.atack['effs']['cura']['type'] == "cura":
                        percent = self.atack['effs']['cura']['damage']
                        regen = int(((self.status['con'] * self.rate[0]) / 100) * percent)
                        if (self.status['hp'] + regen) <= (self.status['con'] * self.rate[0]):
                            self.status['hp'] += regen
                        else:
                            self.status['hp'] = (self.status['con'] * self.rate[0])
                        desc = f'**{self.name.upper()}** ``recuperou`` **{regen}** ``de HP``'
                        hp = self.status['con'] * self.rate[0]
                        p = not self.is_player
                        await ctx.send(embed=embed_creator(desc, self.atack['img'], p, hp,
                                                           self.status['hp'], self.img, self.ln))
                        self.atack = None
        except KeyError:
            pass
        except TypeError:
            pass

        if effects is not None:
            for c in effects:
                try:
                    if 'damage' in self.effects[c]['type']:
                        damage = self.effects[c]['damage']
                        damage = damage if damage > 0 else 1
                        self.status['hp'] -= damage
                        if self.status['hp'] < 0:
                            self.status['hp'] = 0
                        description = f"**{self.name.upper()}** ``sofreu`` **{damage}** ``de dano " \
                                      f"por efeito de`` **{c.upper()}!**"
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player
                        img_ = "https://media1.giphy.com/media/md78DFkpIIzzW/source.gif"
                        embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)
                    elif 'manadrain' in self.effects[c]['type']:
                        damage = self.effects[c]['damage']
                        damage = damage if damage > 0 else 1
                        damage = int(((self.status['con'] * self.rate[1]) / 100) * damage)
                        self.status['mp'] -= damage
                        if self.status['mp'] < 0:
                            self.status['mp'] = 0
                        description = f"**{self.name.upper()}** ``teve`` **{damage}** ``de mana " \
                                      f"drenada por efeito de`` **{c.upper()}!**"
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player
                        img_ = "https://media1.giphy.com/media/pDLxcNa1r3QA0/source.gif"
                        embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)
                    if self.effects[c]['turns'] > 0 and c == "cegueira":
                        description = f"**{self.name.upper()}** ``esta sobe o efeito de`` " \
                                      f"**{c.upper()}!**"
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player
                        img_ = "https://vignette.wikia.nocookie.net/yugioh/images/9/95/MesmericControl-TF04-JP-VG.jpg"
                        embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)
                except KeyError:
                    pass

                try:
                    if self.effects[c]['turns'] > 0:
                        self.effects[c]['turns'] -= 1

                    if self.effects[c]['turns'] < 1:
                        del self.effects[c]
                except KeyError:
                    pass

        return self.atack

    async def damage(self, skill, lvlskill, enemy_atack, ctx, name, enemy_cc, enemy_img, enemy_luk):

        # chance de critital 100%
        lethal = False

        if skill is None:
            description = f'**{name.upper()}** ``não pode atacar!``'
            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player if self.pvp else self.is_player
            img_ = "https://uploads1.yugioh.com/card_images/2110/detail/2004.jpg?1385103024"
            embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], enemy_img, self.ln)
            return await ctx.send(embed=embed_)

        if skill == "PASS-TURN-MP":
            description = f'**{name.upper()}** ``passou o turno, usando a poção de MANA!``'
            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player if self.pvp else self.is_player
            img_ = "https://vignette.wikia.nocookie.net/yugioh/images/6/61/OfferingstotheDoomed-TF04-JP-VG.png"
            embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], enemy_img, self.ln)
            return await ctx.send(embed=embed_)

        if skill == "PASS-TURN-HP":
            description = f'**{name.upper()}** ``passou o turno, usando a poção de VIDA!``'
            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player if self.pvp else self.is_player
            img_ = "https://vignette.wikia.nocookie.net/yugioh/images/6/61/OfferingstotheDoomed-TF04-JP-VG.png"
            embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], enemy_img, self.ln)
            return await ctx.send(embed=embed_)

        if not self.is_player or self.pvp:
            skill_number = int(skill['skill'])
            lvs = lvlskill[skill_number - 1]
        else:
            lvs = lvlskill

        self.ls = lvs if 0 <= lvs <= 9 else 9

        if skill['effs'] is not None:
            if not self.is_player:
                key = [k for k, v in skill['effs'][self.ls].items()]
            else:
                if self.pvp:
                    key = [k for k, v in skill['effs'][self.ls].items()]
                else:
                    key = [k for k, v in skill['effs'].items()]
            for c in key:

                rate_chance = 97  # a chance da skill funcionar
                chance = randint(1, 100)
                chance += enemy_luk + int(lvs / 2)
                rate_chance -= int(enemy_luk / 2) if enemy_luk > 0 else 0

                if chance >= rate_chance:
                    self.chance = True
                else:
                    self.chance = False

                if self.chance:

                    if c in self.effects.keys() and self.effects[c]['turns'] > 0:
                        description = f'**{self.name.upper()}** ``ainda está sob o efeito de`` **{c.upper()}**'
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player if self.pvp else self.is_player
                        img_ = "https://vignette.wikia.nocookie.net/yugioh/images/c/c6/RingofDefense-OW.png"
                        embed_ = embed_creator(description, img_, monster, hp_max,
                                               self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)

                    else:

                        if not self.is_player:
                            self.effects[c] = skill['effs'][self.ls][c]
                            max_turn = skill['effs'][self.ls][c]['turns']
                            self.effects[c]['turns'] = randint(1, max_turn) if max_turn > 1 else max_turn
                        else:
                            if self.pvp:
                                self.effects[c] = skill['effs'][self.ls][c]
                                max_turn = skill['effs'][self.ls][c]['turns']
                                self.effects[c]['turns'] = randint(1, max_turn) if max_turn > 1 else max_turn
                            else:
                                self.effects[c] = skill['effs'][c]
                                max_turn = skill['effs'][c]['turns']
                                self.effects[c]['turns'] = randint(1, max_turn) if max_turn > 1 else max_turn

                        if self.effects[c]['turns'] < 1 or self.effects[c]['turns'] > 9:
                            self.effects[c]['turns'] = randint(1, 2)

                        turns = self.effects[c]['turns']

                        description = f'**{self.name.upper()}** ``recebeu o efeito de`` **{c.upper()}** ``por`` ' \
                                      f'**{turns}** ``turno{"s" if turns > 1 else ""}``'
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player if self.pvp else self.is_player
                        embed_ = embed_creator(description, skill['img'], monster, hp_max,
                                               self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)

                else:
                    description = f'**{self.name.upper()}** ``não recebeu o efeito de`` **{c.upper()}**'
                    hp_max = self.status['con'] * self.rate[0]
                    monster = not self.is_player if self.pvp else self.is_player
                    img_ = "https://uploads1.yugioh.com/card_images/2383/detail/110.jpg?1385098437"
                    embed_ = embed_creator(description, img_, monster, hp_max,
                                           self.status['hp'], self.img, self.ln)
                    await ctx.send(embed=embed_)

        if not self.is_player:
            damage = skill['damage'][self.ls]
        else:
            if self.pvp:
                damage = skill['damage'][self.ls]
            else:
                damage = skill['damage']
        d1 = int(damage[:damage.find('d')])
        d2 = int(damage[damage.find('d') + 1:])

        dd = (d2, d2 * d1) if d2 != d2 * d1 else (d2, d2)
        if lvs >= 11:
            dd = (d2 + int((lvs - 10) * 10), d2 * d1)

        if dd[0] != dd[1]:
            bk = randint(dd[0], dd[1])
        else:
            bk = dd[0]

        if not self.is_player or self.pvp:
            damage = int(enemy_atack / 100 * ((30 + (skill['skill'] * 5)) + (skill['skill'] * 10))) + bk
        else:
            damage = enemy_atack + bk

        critical = False
        critical_chance = randint(1, 20)
        critical_damage = enemy_cc[0]
        value_critical = 20

        if enemy_cc[1] in ['necromancer', 'wizard', 'warlock']:
            value_critical = 19

        if enemy_cc[1] in ['assassin', 'priest']:
            value_critical = 18

        if not self.is_player or self.pvp:
            value_critical -= int(enemy_luk / 5)

        try:
            if self.effects["cegueira"]['turns'] > 0:
                lethal = True
        except KeyError:
            lethal = False

        if critical_chance >= value_critical or lethal:
            critical = True

        if critical:
            damage = int(damage + (damage / 100 * critical_damage))

            file = discord.File("images/elements/critical.gif", filename="critical.gif")
            embed = discord.Embed(title="CRITICAL", color=0x38105e)
            embed.set_image(url="attachment://critical.gif")
            await ctx.send(file=file, embed=embed)

        defense = self.pdef if skill['type'] == "fisico" else self.mdef
        if skill['type'] == "especial":
            defense = choice([self.pdef, self.mdef])

        armor_now = defense if defense > 0 else 1
        percent = abs(int(armor_now / (damage / 100)))
        if percent < 45:
            dn = abs(int(damage - defense))
        else:
            dn_chance = randint(1, 100)
            dn = abs(int(damage - defense) if dn_chance < 5 else int(damage / 100 * randint(46, 65)))

        if dn < 0:
            description = f'**{self.name.upper()}** ``obsorveu todo o dano e recebeu`` **0** ``de dano``'
            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player if self.pvp else self.is_player
            embed_ = embed_creator(description, skill['img'], monster, hp_max, self.status['hp'], self.img, self.ln)
            await ctx.send(embed=embed_)
        else:
            self.status['hp'] -= dn
            if self.status['hp'] < 0:
                self.status['hp'] = 0

            if defense > 0:
                description = f'**{self.name.upper()}** ``receberia`` **{damage}** ``de dano, mas absorveu parte ' \
                              f'dele, logo recebeu`` **{dn}**'
            else:
                description = f'**{self.name.upper()}** ``recebeu`` **{damage}** ``de dano``'

            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player if self.pvp else self.is_player
            embed_ = embed_creator(description, skill['img'], monster, hp_max, self.status['hp'], self.img, self.ln)
            await ctx.send(embed=embed_)
