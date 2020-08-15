import discord

from asyncio import sleep, TimeoutError
from resources.utility import embed_creator
from random import randint, choice
from config import data

# DATABASE SKILL / EQUIP
classes = data['skills']
itens = data['equips']
# NEW SKILLS
niveis = [5, 10, 15, 20, 25]


class Entity(object):
    def __init__(self, db, is_player):
        self.db = db
        self.name = self.db['Name']
        self.status = self.db['Status']
        self.xp = self.db['XP']
        self.lvl = self.db['Level']
        self.effects = {}
        self.atacks = {}
        self.atack = None
        self.chance = False
        self.is_player = is_player
        self.armor = 0
        self.img = self.db['img']
        self.ln = self.db['lower_net']

        if self.is_player:
            self._ = self.db['Class']
            self.rate = [classes[self.db['Class']]['rate']['life'], classes[self.db['Class']]['rate']['mana']]

            if self._ != "default":
                for k in self.status.keys():
                    self.status[k] += data['skills'][self._]['modifier'][k]

            for c in self.db['equipped_items']:
                self.armor += itens[c[1]][c[0]]['armor']
                for name in self.status.keys():
                    self.status[name] += itens[c[1]][c[0]]['modifier'][name]

            self.ik = []

            for c in range(5):
                if self.lvl >= niveis[c]:
                    self.atacks[classes[self.db['next_class']][str(c)]['name']] = classes[self.db['next_class']][str(c)]
                    self.ik.append(self.db['next_class'])
                else:
                    self.atacks[classes[self.db['Class']][str(c)]['name']] = classes[self.db['Class']][str(c)]
                    self.ik.append(self.db['Class'])

            for c in self.status.keys():
                if c in ["pdh", "hp", "mp"]:
                    continue
                self.status[c] += classes[self.db['Class']]['modifier'][c]

            self.status['hp'] = self.status['con'] * self.rate[0]
            self.status['mp'] = self.status['con'] * self.rate[1]
            self.level_skill = self.db['Level'] // 10 + randint(1 + (self.status["luk"] // 4), 5)
        else:
            self.atacks = self.db['Atacks']
            self.level_skill = self.db['Level'] // 10 + randint(1, 5)
            self.rate = [(10 + self.db['Level'] // 10), (10 + self.db['Level'] // 10)]
            self.status['hp'] = self.status['con'] * self.rate[0]
            self.status['mp'] = self.status['con'] * self.rate[1]

    async def turn(self, enemy_life, bot, ctx):
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
                title = 'YOUR HP:  [{}/{}]  ||  YOUR MP:  [{}/{}]\n----====>>> ENEMY HP:  [{}] <<<====----' \
                        ''.format(self.status['hp'] if self.status['hp'] > 0 else 0,
                                  (self.status['con'] * self.rate[0]),
                                  self.status['mp'] if self.status['mp'] > 0 else 0,
                                  (self.status['con'] * self.rate[1]),
                                  enemy_life if enemy_life > 0 else 0)
                description = ''
                for c in range(0, len(atacks)):
                    c2 = atacks[c]
                    description += f"{emojis[c]} **{c2.upper()}** ``Lv:`` **{self.level_skill}**\n" \
                                   f"``Dano:`` **{self.atacks[c2]['damage'][self.level_skill]}**\n" \
                                   f"``Mana:`` **{self.atacks[c2]['mana'][self.level_skill]}%**\n" \
                                   f"``Efeito(s):`` " \
                                   f"**{str(self.atacks[c2]['effs'][self.level_skill].keys())}**" \
                                   f"\n\n".replace('dict_keys([', '').replace('])', '').replace('\'', '')
                description += f'<:pass:692967573649752194> **{"Pass turn".upper()}**\n' \
                               f'``Mana Recovery:`` **15% da Mana Total**'
                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=0x000000
                )
                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                msg = await ctx.send(embed=embed)
                for c in range(0, len(atacks)):
                    await msg.add_reaction(emojis[c])
                await msg.add_reaction('<:pass:692967573649752194>')
                while not bot.is_closed():
                    try:
                        reaction = await bot.wait_for('reaction_add', timeout=30.0)
                        while reaction[1].id != ctx.author.id:
                            reaction = await bot.wait_for('reaction_add', timeout=30.0)
                    except TimeoutError:
                        return "COMANDO-CANCELADO"
                    emo = "<:pass:692967573649752194>"
                    emoji_ = str(emo).replace('<:', '').replace(emo[emo.rfind(':'):], '')
                    try:
                        if reaction[0].emoji.name == emoji_:
                            regen = int(((self.status['con'] * self.rate[1]) / 100) * 15)
                            if (self.status['mp'] + regen) <= (self.status['con'] * self.rate[1]):
                                self.status['mp'] += regen
                            else:
                                self.status['mp'] = (self.status['con'] * self.rate[1])
                            break
                    except AttributeError:
                        pass
                    for c in emojis:
                        emoji = str(c).replace('<:', '').replace(c[c.rfind(':'):], '')
                        try:
                            if reaction[0].emoji.name == emoji:
                                self.atack = emojis.index(f'<:{reaction[0].emoji.name}:{reaction[0].emoji.id}>')
                                self.atack = atacks[self.atack]
                                percent = self.atacks[self.atack]['mana'][self.level_skill]
                                remove = int(((self.status['con'] * self.rate[1]) / 100) * percent)
                                if self.status['mp'] > remove:
                                    self.status['mp'] -= remove
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
                                    self.atack = None
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

        await sleep(1)

        if effects is not None:
            for c in effects:
                try:
                    if 'damage' in self.effects[c]['type']:
                        self.status['hp'] -= self.effects[c]['damage']
                        if self.status['hp'] < 0:
                            self.status['hp'] = 0
                        description = f"**{self.name.upper()}** ``sofreu`` **{self.effects[c]['damage']}** ``de dano " \
                                      f"por efeito``"
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player
                        img_ = "https://media1.giphy.com/media/md78DFkpIIzzW/source.gif"
                        embed_ = embed_creator(description, img_, monster, hp_max,
                                               self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)
                    elif 'manadrain' in self.effects[c]['type']:
                        self.status['mp'] -= self.effects[c]['damage']
                        if self.status['mp'] < 0:
                            self.status['mp'] = 0
                        description = f"**{self.name.upper()}** ``teve`` **{self.effects[c]['damage']}** ``de mana " \
                                      f"drenada por efeito``"
                        hp_max = self.status['con'] * self.rate[0]
                        monster = not self.is_player
                        img_ = "https://media1.giphy.com/media/pDLxcNa1r3QA0/source.gif"
                        embed_ = embed_creator(description, img_, monster,
                                               hp_max, self.status['hp'], self.img, self.ln)
                        await ctx.send(embed=embed_)
                except KeyError:
                    pass
                if self.effects[c]['turns'] > 0:
                    self.effects[c]['turns'] -= 1
        return self.atack

    async def damage(self, skill, enemy_atack, ctx, name):
        if skill is not None:
            if skill['effs'] is not None:
                if not self.is_player:
                    key = [k for k, v in skill['effs'][self.level_skill].items()]
                else:
                    key = [k for k, v in skill['effs'].items()]
                for c in key:
                    try:
                        if not self.is_player:
                            chance = randint(1, 100)
                            chance += self.status['luk']
                            if chance >= 90:
                                self.effects['turns'] += skill['effs'][self.level_skill][c]['turns']
                                self.chance = True
                            else:
                                self.chance = False
                        else:
                            chance = randint(1, 100)
                            if chance >= 50:
                                self.effects['turns'] += skill['effs'][c]['turns']
                                self.chance = True
                            else:
                                self.chance = False
                    except KeyError:
                        if not self.is_player:
                            chance = randint(1, 100)
                            chance += self.status['luk']
                            if chance >= 90:
                                self.effects[c] = skill['effs'][self.level_skill][c]
                                self.chance = True
                            else:
                                self.chance = False
                        else:
                            chance = randint(1, 100)
                            if chance >= 50:
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
                damage = skill['damage'][self.level_skill]
            else:
                damage = skill['damage']
            dice1 = int(damage[:damage.find('d')])
            dice2 = int(damage[damage.find('d') + 1:])
            damage = 0
            for c in range(0, dice1):
                damage += randint(1, dice2)
            damage += enemy_atack
            self.status['hp'] -= damage
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
