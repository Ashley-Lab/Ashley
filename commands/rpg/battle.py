from asyncio import sleep
from discord.ext import commands
from random import randint, choice
from resources.entidade import Entity
from resources.check import check_it
from resources.db import Database


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monsters = self.bot.config['battle']['monsters']

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='battle', aliases=['batalha'])
    async def battle(self, ctx):
        db_player = {'Class': 'maga',
                     'Name': ctx.author.name,
                     'Status': {
                         'con': int(30),
                         'prec': int(30),
                         'agi': int(30),
                         'atk': int(30)
                     },
                     'XP': int(8000),
                     'itens': ['armadura de gurdur']}
        db_monster = choice(self.monsters)
        player = Entity(db_player, True)
        monster = Entity(db_monster, False)
        turns = choice([0, 1])
        while player.status['hp'] > 0 and monster.status['hp'] > 0:
            if turns == 0:
                atk = await player.turn(monster.status['hp'], self.bot, ctx)
                if randint(0, 20) + player.status['prec'] > randint(0, 16) + monster.status['agi']:
                    await monster.damage(atk, player.status['atk'], ctx)
                atk = await monster.turn(monster.status['hp'], self.bot, ctx)
                if randint(0, 20) + monster.status['prec'] > randint(0, 16) + player.status['agi']:
                    await player.damage(atk, monster.status['atk'], ctx)
                await sleep(5)
            else:
                atk = await monster.turn(monster.status['hp'], self.bot, ctx)
                if randint(0, 20) + monster.status['prec'] > randint(0, 16) + player.status['agi']:
                    await player.damage(atk, monster.status['atk'], ctx)
                atk = await player.turn(monster.status['hp'], self.bot, ctx)
                if randint(0, 20) + player.status['prec'] > randint(0, 16) + monster.status['agi']:
                    await monster.damage(atk, player.status['atk'], ctx)
                await sleep(5)
        if monster.status['hp'] > 0:
            await ctx.send('you lose')
        else:
            await ctx.send('you win')


def setup(bot):
    bot.add_cog(Battle(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mBATTLE\033[1;32m foi carregado com sucesso!\33[m')
