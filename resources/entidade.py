import discord
import asyncio

from asyncio import sleep
from discord.ext import commands
from resources.utility import embed_creator
from random import randint, choice
from config import data

manatax = 5
lifetax = 7
classes = data['skills']
niveis = [10, 20, 30, 40, 50]
itens = data['equips']


class Entity(object):
    def __init__(self, db, is_player):
        self.name = db['Name']
        self.status = db['Status']
        self.xp = db['XP']
        self.effects = {}
        self.atacks = {}
        self.atack = None
        self.is_player = is_player
        self.armor = 0
        self.img = db['img']
        # levelatacks = [5, 10, 15, 20]
        levelatacks = [2, 3, 4, 5]
        if self.is_player:
            self.atacks[classes[db['Class']]['0']['name']] = classes[db['Class']]['0']
            for c in range(1, 5):
                if self.xp > niveis[(levelatacks[c - 1] - 1)]:
                    self.atacks[classes[db['Class']][str(c)]['name']] = classes[db['Class']][str(c)]
        else:
            self.atacks = db['Atacks']
        self.status['hp'] = self.status['con'] * lifetax
        self.status['mp'] = self.status['con'] * manatax
        if self.is_player:
            self._ = db['Class']
            for c in db['itens']:
                self.armor += itens[c[1]][c[0]]['armor']
                key = self.status.keys()
                for c2 in key:
                    try:
                        self.status[c2] += itens[c[1]][c[0]]['modifier'][c2]
                    except KeyError:
                        pass
        key = self.status.keys()
        for c in key:
            try:
                self.status[c] += classes[db['Class']]['modifier'][c]
            except KeyError:
                pass

    async def turn(self, enemy_life, bot, ctx):
        stun = False
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
            if self.is_player is True:
                emojis = [bot.config['skills'][self._]['0']['icon'], bot.config['skills'][self._]['1']['icon'],
                          bot.config['skills'][self._]['2']['icon'], bot.config['skills'][self._]['3']['icon'],
                          bot.config['skills'][self._]['4']['icon']]
                title = 'YOUR HP:  [{}]  ||  YOUR MP:  [{}]\nENEMY HP:  [{}]' \
                        ''.format(self.status['hp'] if self.status['hp'] > 0 else 0,
                                  self.status['mp'] if self.status['mp'] > 0 else 0,
                                  enemy_life if enemy_life > 0 else 0)
                description = ''
                for c in range(0, len(atacks)):
                    c2 = atacks[c]
                    description += f"{emojis[c]} **{c2.upper()}** ``Lv:`` **{self.atacks[c2]['level']}**\n" \
                                   f"``Dano:`` **{self.atacks[c2]['damage'][self.atacks[c2]['level'] - 1]}**\n" \
                                   f"``Mana:`` **{self.atacks[c2]['mana'][self.atacks[c2]['level'] - 1]}**\n" \
                                   f"``Efeito(s):`` " \
                                   f"**{str(self.atacks[c2]['effs'][self.atacks[c2]['level'] - 1].keys())}**" \
                                   f"\n\n".replace('dict_keys([', '').replace('])', '').replace('\'', '')
                description += '⏭️ **Pass turn**'.upper()
                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=0x000000
                )
                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                msg = await ctx.send(embed=embed)
                for c in range(0, len(atacks)):
                    await msg.add_reaction(emojis[c])
                await msg.add_reaction('⏭️')
                while True:
                    reaction = await bot.wait_for('reaction_add')
                    while reaction[1].id != ctx.author.id:
                        reaction = await bot.wait_for('reaction_add')
                    for c in emojis:
                        emoji = str(c).replace('<:', '').replace(c[c.rfind(':'):], '')
                        try:
                            if reaction[0].emoji.name == emoji:
                                self.atack = emojis.index(f'<:{reaction[0].emoji.name}:{reaction[0].emoji.id}>')
                                self.atack = atacks[self.atack]
                                break
                        except AttributeError:
                            break
                        except TypeError:
                            break
                    if self.atack is not None:
                        break
            else:
                self.atack = choice(atacks)
            try:
                self.atack = self.atacks[self.atack]
            except KeyError:
                pass
            except TypeError:
                pass
        else:
            description = f'{self.name} esta stunado'
            hp_max = self.status['con'] * lifetax
            monster = not self.is_player
            img_ = self.atack['img']
            embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img)
            await ctx.send(embed=embed_)

        await sleep(1)

        if effects is not None:
            for c in effects:
                try:
                    if 'damage' in self.effects[c]['type']:
                        self.status['hp'] -= self.effects[c]['damage']
                        description = f"**{self.name.upper()}** ``sofreu`` **{self.effects[c]['damage']}** ``de dano " \
                                      f"por efeito``"
                        hp_max = self.status['con'] * lifetax
                        monster = not self.is_player
                        img_ = self.atack['img']
                        embed_ = embed_creator(description, img_, monster, hp_max,
                                               self.status['hp'], self.img)
                        await ctx.send(embed=embed_)
                    elif 'manadrain' in self.effects[c]['type']:
                        self.status['mp'] -= self.effects[c]['damage']
                        description = f"**{self.name.upper()}** ``teve`` **{self.effects[c]['damage']}** ``de mana " \
                                      f"drenada por efeito``"
                        hp_max = self.status['con'] * lifetax
                        monster = not self.is_player
                        img_ = self.atack['img']
                        embed_ = embed_creator(description, img_, monster,
                                               hp_max, self.status['hp'], self.img)
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
                    key = skill['effs'][skill['level']].keys()
                else:
                    key = skill['effs'].keys()
                for c in key:
                    try:
                        if not self.is_player:
                            self.effects['turns'] += skill['effs'][skill['level']][c]['turns']
                        else:
                            self.effects['turns'] += skill['effs'][c]['turns']
                    except KeyError:
                        if not self.is_player:
                            self.effects[c] = skill['effs'][skill['level']][c]
                        else:
                            self.effects[c] = skill['effs'][c]
                    description = f'**{self.name.upper()}** ``recebeu o efeito de`` **{c.upper()}**'
                    hp_max = self.status['con'] * lifetax
                    monster = not self.is_player
                    embed_ = embed_creator(description, skill['img'], monster, hp_max,
                                           self.status['hp'], self.img)
                    await ctx.send(embed=embed_)
            if not self.is_player:
                damage = skill['damage'][skill['level']]
            else:
                damage = skill['damage']
            dice1 = int(damage[:damage.find('d')])
            dice2 = int(damage[damage.find('d') + 1:])
            damage = 0
            for c in range(0, dice1):
                damage += randint(0, dice2)
            damage += enemy_atack
            self.status['hp'] -= damage
            description = f'**{self.name.upper()}** ``recebeu`` **{damage}** ``de dano``'
            hp_max = self.status['con'] * lifetax
            monster = not self.is_player
            embed_ = embed_creator(description, skill['img'], monster, hp_max, self.status['hp'], self.img)
            await ctx.send(embed=embed_)

        else:
            description = f'**{name.upper()}** ``não pode atacar!``'
            hp_max = self.status['con'] * lifetax
            monster = not self.is_player
            img_ = "https://uploads1.yugioh.com/card_images/2110/detail/2004.jpg?1385103024"
            embed_ = embed_creator(description, img_, monster, hp_max, self.status['hp'], self.img)
            await ctx.send(embed=embed_)
