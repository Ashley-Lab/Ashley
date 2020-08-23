import discord

from asyncio import sleep, TimeoutError
from resources.utility import embed_creator
from random import randint, choice
from config import data

classes = data['skills']
equipments = data['equips']
levels = [5, 10, 15, 20, 25]


class Entity(object):
    def __init__(self, db, is_player):
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
        self.armor = 0
        self.img = self.db['img']
        self.ln = self.db['lower_net']

        if self.is_player:

            self.rate = [classes[self.db['class']]['rate']['life'], classes[self.db['class']]['rate']['mana']]
            if self.db['level'] > 25:
                self.rate[0] += classes[self.db['next_class']]['rate']['life']
                self.rate[1] += classes[self.db['next_class']]['rate']['mana']

            for k in self.status.keys():
                if k in ["pdh", "hp", "mp"]:
                    continue
                self.status[k] += classes[self.db['class']]['modifier'][k]
                if self.db['level'] > 25:
                    self.status[k] += classes[self.db['next_class']]['modifier'][k]

            for c in self.db['equipped_items']:
                self.armor += equipments[c[1]][c[0]]['armor']
                for name in self.status.keys():
                    self.status[name] += equipments[c[1]][c[0]]['modifier'][name]

            self.ik = []
            for c in range(5):
                if self.lvl >= levels[c]:
                    self.atacks[classes[self.db['next_class']][str(c)]['name']] = classes[self.db['next_class']][str(c)]
                    self.ik.append(self.db['next_class'])
                else:
                    self.atacks[classes[self.db['class']][str(c)]['name']] = classes[self.db['class']][str(c)]
                    self.ik.append(self.db['class'])

            self.status['hp'] = self.status['con'] * self.rate[0]
            self.status['mp'] = self.status['con'] * self.rate[1]
            self.level_skill = self.status["luk"] // 2 if self.status["luk"] // 2 < 10 else 9

        else:

            for k in self.status.keys():
                if k in ["pdh", "hp", "mp"]:
                    continue
                if self.db['enemy'] > 25:
                    self.status[k] += randint(2, 4)

            self.atacks = self.db['atacks']
            self.level_skill = self.db['level'] // 10 + randint(1, 5)

            if self.db['enemy'] > 25:
                self.rate = [(12 + self.db['level'] // 10), (12 + self.db['level'] // 10)]
            else:
                self.rate = [(6 + self.db['level'] // 10), (6 + self.db['level'] // 10)]

            self.status['hp'] = self.status['con'] * self.rate[0]
            self.status['mp'] = self.status['con'] * self.rate[1]

    async def turn(self, enemy_info, bot, ctx):
        stun = False
        self.atack = None
        atacks = eval(str(self.atacks.keys()).replace('dict_keys(', '').replace(')', ''))
        try:
            effects = eval(str(self.effects.keys()).replace('dict_keys(', '').replace(')', ''))
        except KeyError:
            effects = None

        for c in ['stun', 'gelo']:
            try:
                if c in effects and self.effects[c]['turns'] > 0:
                    stun = True
            except KeyError:
                pass

        for c in [['fraquesa', 'fisico'], ['silencio', 'magico']]:
            try:
                if c[0] in effects and self.effects[c[0]]['turns'] > 0:
                    for c2 in atacks:
                        if self.atacks[c2]['type'] == c[1]:
                            atacks.remove(c2)
            except KeyError:
                pass

        if stun is False:
            if self.is_player:
                emojis = [bot.config['skills'][self.ik[0]]['0']['icon'], bot.config['skills'][self.ik[1]]['1']['icon'],
                          bot.config['skills'][self.ik[2]]['2']['icon'], bot.config['skills'][self.ik[3]]['3']['icon'],
                          bot.config['skills'][self.ik[4]]['4']['icon']]
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
                    c2, ls = atacks[c], self.level_skill
                    damage = int(self.status['atk'] + self.status['atk'] * 0.50)
                    dado = self.atacks[c2]['damage'][self.level_skill]
                    description += f"{emojis[c]} **{c2.upper()}** ``Lv:`` **{ls + 1 if ls + 1 < 11 else 10}**\n" \
                                   f"``Dano:`` **{dado} + {damage} de ATK**\n" \
                                   f"``Mana:`` **{self.atacks[c2]['mana'][self.level_skill]}**\n" \
                                   f"``Efeito(s):`` " \
                                   f"**{str(self.atacks[c2]['effs'][self.level_skill].keys())}**" \
                                   f"\n\n".replace('dict_keys([', '').replace('])', '').replace('\'', '')
                regen = int(((self.status['con'] * self.rate[1]) / 100) * 50)
                description += f'<:pass:692967573649752194> **{"Pass turn".upper()}**\n' \
                               f'``Mana Recovery:`` **+{regen} de Mana** + **HP Regen**'
                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=0x000000
                )
                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                msg = await ctx.send(embed=embed)
                await sleep(0.5)
                for c in range(0, len(atacks)):
                    await msg.add_reaction(emojis[c])
                await msg.add_reaction('<:pass:692967573649752194>')
                while not bot.is_closed():
                    try:
                        reaction = await bot.wait_for('reaction_add', timeout=60.0)
                        while reaction[1].id != ctx.author.id:
                            reaction = await bot.wait_for('reaction_add', timeout=60.0)
                    except TimeoutError:
                        return "COMANDO-CANCELADO"
                    emo = "<:pass:692967573649752194>"
                    emoji_ = str(emo).replace('<:', '').replace(emo[emo.rfind(':'):], '')
                    try:
                        if reaction[0].emoji.name == emoji_:
                            regen = int(((self.status['con'] * self.rate[1]) / 100) * 50)
                            if (self.status['mp'] + regen) <= (self.status['con'] * self.rate[1]):
                                self.status['mp'] += regen
                                hp = int(((self.status['con'] * self.rate[1]) / 100) * 10)
                                if (self.status['hp'] + hp) <= (self.status['con'] * self.rate[0]):
                                    self.status['hp'] += hp
                                else:
                                    self.status['hp'] = (self.status['con'] * self.rate[0])
                            else:
                                self.status['mp'] = (self.status['con'] * self.rate[1])
                            self.atack = None
                            break
                    except AttributeError:
                        pass
                    for c in emojis:
                        emoji = str(c).replace('<:', '').replace(c[c.rfind(':'):], '')
                        try:
                            if reaction[0].emoji.name == emoji:
                                test_atack = emojis.index(f'<:{reaction[0].emoji.name}:{reaction[0].emoji.id}>')
                                _atack = atacks[test_atack]
                                remove = self.atacks[_atack]['mana'][self.level_skill]
                                if self.status['mp'] >= remove:
                                    self.status['mp'] -= remove
                                    self.atack = atacks[test_atack]
                                    break
                                else:
                                    embed = discord.Embed(
                                        description=f"``{ctx.author.name.upper()} VOCÊ NÃO TEM MANA O SUFICIENTE!\n"
                                                    f"ENTÃO ESCOLHA OUTRA SKILL OU PASSE A VEZ...``\n"
                                                    f"**Obs:** Passar a vez regenera a mana!",
                                        color=0x000000
                                    )
                                    embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                                    await ctx.send(embed=embed)
                        except TypeError:
                            break
                        except AttributeError:
                            pass
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

            try:
                self.atack = self.atacks[self.atack]
            except KeyError:
                pass
            except TypeError:
                pass

        else:
            description = f'{self.name} esta stunado'
            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player
            img_ = "https://uploads1.yugioh.com/card_images/2110/detail/2004.jpg?1385103024"
            embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img, self.ln)
            await ctx.send(embed=embed_)

        try:
            if self.atack['effs'] is not None:
                if self.is_player:
                    if self.atack['effs'][self.level_skill]['cura']['type'] == "cura":
                        percent = self.atack['effs'][self.level_skill]['cura']['damage']
                        regen = int(((self.status['con'] * self.rate[0]) / 100) * percent)
                        if (self.status['hp'] + regen) <= (self.status['con'] * self.rate[0]):
                            self.status['hp'] += regen
                        else:
                            self.status['hp'] = (self.status['con'] * self.rate[0])
                        desc = f'**{self.name.upper()}** ``recuperou`` **{regen}%** ``de HP``'
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
                        desc = f'**{self.name.upper()}** ``recuperou`` **{regen}%** ``de HP``'
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
                        self.status['hp'] -= (self.effects[c]['damage'] - self.armor // 2)
                        if self.status['hp'] < 0:
                            self.status['hp'] = 0
                        description = f"**{self.name.upper()}** ``sofreu`` **{self.effects[c]['damage']}** ``de dano " \
                                      f"por efeito``"
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player
                        img_ = "https://media1.giphy.com/media/md78DFkpIIzzW/source.gif"
                        embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)
                    elif 'manadrain' in self.effects[c]['type']:
                        self.status['mp'] -= (self.effects[c]['damage'] - self.armor // 2)
                        if self.status['mp'] < 0:
                            self.status['mp'] = 0
                        description = f"**{self.name.upper()}** ``teve`` **{self.effects[c]['damage']}** ``de mana " \
                                      f"drenada por efeito``"
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player
                        img_ = "https://media1.giphy.com/media/pDLxcNa1r3QA0/source.gif"
                        embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)
                except KeyError:
                    pass
                if self.effects[c]['turns'] > 0:
                    self.effects[c]['turns'] -= 1

        return self.atack

    async def damage(self, skill, lvlskill, enemy_atack, ctx, name):
        if skill is not None:
            if skill['effs'] is not None:
                if not self.is_player:
                    key = [k for k, v in skill['effs'][lvlskill].items()]
                else:
                    key = [k for k, v in skill['effs'].items()]
                for c in key:
                    try:
                        if not self.is_player:
                            chance = randint(1, 100)
                            chance += self.status['luk']
                            if chance >= 95:
                                self.effects['turns'] += skill['effs'][lvlskill][c]['turns']
                                self.chance = True
                            else:
                                self.chance = False
                        else:
                            chance = randint(1, 100)
                            if chance >= 95:
                                self.effects['turns'] += skill['effs'][c]['turns']
                                self.chance = True
                            else:
                                self.chance = False
                    except KeyError:
                        if not self.is_player:
                            chance = randint(1, 100)
                            chance += self.status['luk']
                            if chance >= 95:
                                self.effects[c] = skill['effs'][lvlskill][c]
                                self.chance = True
                            else:
                                self.chance = False
                        else:
                            chance = randint(1, 100)
                            if chance >= 95:
                                self.effects[c] = skill['effs'][c]
                                self.chance = True
                            else:
                                self.chance = False
                    if self.chance:
                        if c.upper() != "SEM EFEITO":
                            description = f'**{self.name.upper()}** ``recebeu o efeito de`` **{c.upper()}**'
                            hp_max = self.status['con'] * self.rate[0]
                            monster = not self.is_player
                            embed_ = embed_creator(description, skill['img'], monster, hp_max,
                                                   self.status['hp'], self.img, self.ln)
                            await ctx.send(embed=embed_)
                    else:
                        if c.upper() != "SEM EFEITO":
                            description = f'**{self.name.upper()}** ``não recebeu o efeito de`` **{c.upper()}**'
                            hp_max = self.status['con'] * self.rate[0]
                            monster = not self.is_player
                            img_ = "https://uploads1.yugioh.com/card_images/2383/detail/110.jpg?1385098437"
                            embed_ = embed_creator(description, img_, monster, hp_max,
                                                   self.status['hp'], self.img, self.ln)
                            await ctx.send(embed=embed_)
            if not self.is_player:
                damage = skill['damage'][lvlskill]
            else:
                damage = skill['damage']
            dice1 = int(damage[:damage.find('d')])
            dice2 = int(damage[damage.find('d') + 1:])
            bk = 0
            for c in range(0, dice1):
                bk += randint(1, dice2)
            damage = enemy_atack + bk
            self.status['hp'] -= (damage - self.armor)
            if self.status['hp'] < 0:
                self.status['hp'] = 0
            description = f'**{self.name.upper()}** ``recebeu`` **{damage}** ``de dano``'
            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player
            embed_ = embed_creator(description, skill['img'], monster, hp_max, self.status['hp'], self.img, self.ln)
            await ctx.send(embed=embed_)
        else:
            description = f'**{name.upper()}** ``não pode atacar!``'
            hp_max = self.status['con'] * self.rate[0]
            monster = not self.is_player
            img_ = "https://uploads1.yugioh.com/card_images/2110/detail/2004.jpg?1385103024"
            embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img, self.ln)
            await ctx.send(embed=embed_)
