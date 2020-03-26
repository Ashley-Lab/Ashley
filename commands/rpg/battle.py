from asyncio import sleep
from discord.ext import commands
from random import randint, choice
from resources.entidade import Entity
from resources.check import check_it
from resources.db import Database
from resources.in_test import Class_rpg, choice_equips


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monsters = self.bot.config['battle']['monsters']

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='battle', aliases=['batalha'])
    async def battle(self, ctx):
        Class_rpg['Name'] = ctx.author.name
        list_items = list(choice_equips(self.bot).values())
        for c in range(5):
            Class_rpg['itens'].append(list_items[c])
        db_player = Class_rpg
        db_monster = choice(self.monsters)
        player = Entity(db_player, True)
        monster = Entity(db_monster, False)
        turns = choice([0, 1])
        while player.status['hp'] > 0 and monster.status['hp'] > 0:
            if turns == 0:
                atk = await player.turn(monster.status['hp'], self.bot, ctx)
                await sleep(1)
                if randint(0, 20) + player.status['prec'] > randint(0, 16) + monster.status['agi']:
                    await monster.damage(atk, player.status['atk'], ctx, player.name)
                else:
                    await ctx.send(f"<:oc_status:519896814225457152>│``{monster.name.upper()} EVADIU``")
                atk = await monster.turn(monster.status['hp'], self.bot, ctx)
                await sleep(1)
                if randint(0, 20) + monster.status['prec'] > randint(0, 16) + player.status['agi']:
                    await player.damage(atk, monster.status['atk'], ctx, monster.name)
                else:
                    await ctx.send("<:confirmado:519896822072999937>│``VOCÊ EVADIU``")
                await sleep(2)
            else:
                atk = await monster.turn(monster.status['hp'], self.bot, ctx)
                await sleep(1)
                if randint(0, 20) + monster.status['prec'] > randint(0, 16) + player.status['agi']:
                    await player.damage(atk, monster.status['atk'], ctx, monster.name)
                else:
                    await ctx.send("<:confirmado:519896822072999937>│``VOCÊ EVADIU``")
                atk = await player.turn(monster.status['hp'], self.bot, ctx)
                await sleep(1)
                if randint(0, 20) + player.status['prec'] > randint(0, 16) + monster.status['agi']:
                    await monster.damage(atk, player.status['atk'], ctx, player.name)
                else:
                    await ctx.send(f"<:oc_status:519896814225457152>│``{monster.name.upper()} EVADIU``")
                await sleep(2)
        if monster.status['hp'] > 0:
            await ctx.send('<:oc_status:519896814225457152>│``VOCÊ PERDEU!``')
        else:
            await ctx.send('<:confirmado:519896822072999937>│``VOCÊ GANHOU!``')


def setup(bot):
    bot.add_cog(Battle(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mBATTLE\033[1;32m foi carregado com sucesso!\33[m')
