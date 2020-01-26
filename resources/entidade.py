import discord
import asyncio

from discord.ext import commands
from random import randint, choice
from config import data

manatax = 5
lifetax = 7
classes = data['battle']['classes']
niveis = data['battle']['niveis']
itens = data['battle']['itens']


class Entity(object):
    def __init__(self, db, is_player):
        self.name = db['Name']
        self.status = db['Status']
        self.xp = db['XP']
        self.effects = {}
        self.atacks = {}
        self.is_player = is_player
        self.armadura = 0
        # levelatacks = [5, 10, 15, 20]
        levelatacks = [2, 3, 4, 5]
        if self.is_player is True:
            self.atacks[classes[db['Class']]['atacks']['primeiro']['name']] = classes[db['Class']]['atacks']['primeiro']
            for c in range(0, 4):
                if self.xp > niveis[(levelatacks[c] - 1)]:
                    self.atacks[classes[db['Class']]['atacks'][str(c)]['name']] = classes[db['Class']]['atacks'][str(c)]
        else:
            self.atacks = db['Atacks']
        self.status['hp'] = self.status['con'] * lifetax
        self.status['mp'] = self.status['con'] * manatax
        if self.is_player:
            for c in db['itens']:
                self.armadura += itens[c]['armadura']
                key = self.status.keys()
                for c2 in key:
                    try:
                        self.status[c2] += itens[c]['modificadores'][c2]
                    except KeyError:
                        pass
        key = self.status.keys()
        for c in key:
            try:
                self.status[c] += classes[db['Class']]['modificadores'][c]
            except KeyError:
                pass

    async def turn(self, enemy_life, bot, ctx):
        stun = False
        atack = None
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

        for c in [['fraquesa', 'fisico'], ['silencio', 'especial']]:
            try:
                if c[0] in effects and self.effects[c[0]]['turns'] > 0:
                    for c2 in atacks:
                        if self.atacks[c2]['type'] == c[1]:
                            atacks.remove(c2)
            except KeyError:
                pass

        if stun is False:
            if self.is_player is True:
                emojis = ['🌕', '🌖', '🌗', '🌘', '🌑']
                title = 'HP: {}\nHP Inimigo:{}'.format(self.status['hp'], enemy_life)
                description = ''
                for c in range(0, len(atacks)):
                    c2 = atacks[c]
                    description += f"{emojis[c]} **{c2.upper()}**: Dano **{self.atacks[c2]['damage']}** " \
                                   f"Mana **{self.atacks[c2]['mana']}**\n" \
                                   f"Efeitos **{str(self.atacks[c2]['effs'].keys())}**\n".replace('dict_keys([',
                                                                                                  '').replace('])', '')
                description += '😶 Pass turn'
                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=bot.color
                )
                msg = await ctx.send(embed=embed)
                for c in range(0, len(atacks)):
                    await msg.add_reaction(emojis[c])
                await msg.add_reaction('😶')
                while True:
                    reaction = await bot.wait_for('reaction_add')
                    while reaction[1].id != ctx.author.id:
                        reaction = await bot.wait_for('reaction_add')
                    if reaction[0].emoji in emojis:
                        atack = emojis.index(reaction[0].emoji)
                        atack = atacks[atack]
                        break
                    else:
                        break
            else:
                atack = choice(atacks)
            try:
                atack = self.atacks[atack]
            except KeyError:
                pass
        else:
            await ctx.send(f'{self.name} esta stunado')

        if effects is not None:
            for c in effects:
                try:
                    if 'damage' in self.effects[c]['type']:
                        self.status['hp'] -= self.effects[c]['damage']
                        await ctx.send(f"{self.name} sofreu {self.effects[c]['damage']} de dano por efeito")
                    elif 'manadrain' in effects[c]['type']:
                        self.status['mp'] -= self.effects[c]['damage']
                        await ctx.send(f"{self.name} teve {self.effects[c]['damage']} de mana drenada por efeito")
                except KeyError:
                    pass
                if self.effects[c]['turns'] > 0:
                    self.effects[c]['turns'] -= 1
        return atack

    async def damage(self, skill, enemy_atack, ctx):
        if skill is not None:
            if skill['effs'] is not None:
                key = skill['effs'].keys()
                for c in key:
                    try:
                        self.effects[c]['turns'] += skill['effs'][c]['turns']
                    except KeyError:
                        self.effects[c] = skill['effs'][c]
                    await ctx.send(f'{self.name} recebeu o efeito de {c}')
            damage = skill['damage']
            dice1 = int(damage[:damage.find('d')])
            dice2 = int(damage[damage.find('d') + 1:])
            damage = 0
            for c in range(0, dice1):
                damage += randint(0, dice2)
            damage += enemy_atack
            self.status['hp'] -= damage
            await ctx.send(f'{self.name} recebeu {damage} de dano')
        else:
            await ctx.send(f'{self.name} não pode atacar')
