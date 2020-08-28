import discord

from asyncio import sleep
from discord.ext import commands
from random import randint, choice
from resources.entidade import Entity
from resources.check import check_it
from resources.db import Database
from resources.img_edit import calc_xp

git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.m = self.bot.config['battle']['monsters']

        self.w_s = {
            "assassin_1": 50,
            "assassin_2": 25,
            "assassin_3": 20,
            "assassin_4": 5,
            "assassin_5": 1,

            "necromancer_1": 50,
            "necromancer_2": 25,
            "necromancer_3": 20,
            "necromancer_4": 5,
            "necromancer_5": 1,

            "paladin_1": 50,
            "paladin_2": 25,
            "paladin_3": 20,
            "paladin_4": 5,
            "paladin_5": 1,

            "priest_1": 50,
            "priest_2": 25,
            "priest_3": 20,
            "priest_4": 5,
            "priest_5": 1,

            "warlock_1": 50,
            "warlock_2": 25,
            "warlock_3": 20,
            "warlock_4": 5,
            "warlock_5": 1,

            "warrior_1": 50,
            "warrior_2": 25,
            "warrior_3": 20,
            "warrior_4": 5,
            "warrior_5": 1,

            "wizard_1": 50,
            "wizard_2": 25,
            "wizard_3": 20,
            "wizard_4": 5,
            "wizard_5": 1,

            "01": 35,
            "02": 35,
            "03": 35
        }

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='battle', aliases=['batalha', 'batalhar'])
    async def battle(self, ctx):
        """Comando usado pra batalhar no rpg da ashley
        Use ash battle"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if data['config']['battle']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE JÁ ESTÁ BATALHANDO!``')
            return await ctx.send(embed=embed)

        try:
            if data['inventory']['coins'] < 50:
                embed = discord.Embed(
                    color=self.bot.color,
                    description='<:negate:721581573396496464>│``VOCE PRECISA DE + DE 50 FICHAS PARA BATALHAR!``\n'
                                '**OBS:** ``USE O COMANDO`` **ASH SHOP** ``PARA COMPRAR FICHAS!``')
                return await ctx.send(embed=embed)
        except KeyError:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE NÃO TEM FICHA!``')
            return await ctx.send(embed=embed)

        update['inventory']['coins'] -= 50
        update['config']['battle'] = True
        await self.bot.db.update_data(data, update, 'users')

        if not data['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
            return await ctx.send(embed=embed)

        # configuração do player
        db_player = dict(data['rpg'])
        db_player['name'] = ctx.author.name
        db_player["img"] = ctx.author.avatar_url_as(format="png")
        player = Entity(db_player, True)

        # configuração do monstro
        lvl = data['rpg']['level']
        dif = 1 if lvl == 1 else 3 if 1 < lvl < 9 else 5 if 9 < lvl < 40 else 10
        min_, max_ = lvl - dif if lvl - dif > 0 else 0, lvl + dif
        db_monster = choice([m for m in self.m if min_ < self.m[self.m.index(m)]['level'] < max_])
        db_monster['lower_net'] = True if data['rpg']['lower_net'] else False
        db_monster['enemy'] = data['rpg']
        monster = Entity(db_monster, False)

        # durante a batalha
        while not self.bot.is_closed():

            # -----------------------------------------------------------------------------
            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break

            skill = await player.turn([monster.status, monster.rate, monster.name, monster.lvl], self.bot, ctx)

            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break
            # -----------------------------------------------------------------------------

            if skill == "COMANDO-CANCELADO":
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['battle'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito`` '
                                      '**COMANDO CANCELADO**')

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------
            lvlp, lvlm, atk = player.lvl, monster.lvl, int(player.status['atk'] * 2)
            if randint(1, 20 + lvlp) + player.status['prec'] > randint(1, 16 + lvlm) + monster.status['agi']:
                await monster.damage(skill, player.level_skill, atk, ctx, player.name)
            else:
                embed = discord.Embed(
                    description=f"``{monster.name.upper()} EVADIU``",
                    color=0x000000
                )
                if not data['rpg']['lower_net']:
                    embed.set_image(url="https://storage.googleapis.com/ygoprodeck.com/pics_artgame/47529357.jpg")
                embed.set_thumbnail(url=f"{db_monster['img']}")
                await ctx.send(embed=embed)

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

            # -----------------------------------------------------------------------------
            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break

            skill = await monster.turn(monster.status['hp'], self.bot, ctx)

            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break
            # -----------------------------------------------------------------------------

            if skill == "COMANDO-CANCELADO":
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['battle'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito`` '
                                      '**COMANDO CANCELADO**')

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

            atk_bonus = monster.status['atk'] * 1 if player.lvl > 25 else monster.status['atk'] * 0.25
            lvlp, lvlm, atk = player.lvl, monster.lvl, int(monster.status['atk'] + atk_bonus)
            if randint(1, 20 + lvlm) + monster.status['prec'] > randint(1, 16 + lvlp) + player.status['agi']:
                await player.damage(skill, monster.level_skill, atk, ctx, monster.name)
            else:
                embed = discord.Embed(
                    description=f"``{ctx.author.name.upper()} EVADIU``",
                    color=0x000000
                )
                if not data['rpg']['lower_net']:
                    embed.set_image(url="https://storage.googleapis.com/ygoprodeck.com/pics_artgame/47529357.jpg")
                embed.set_thumbnail(url=f"{db_player['img']}")
                await ctx.send(embed=embed)

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

        # calculo de xp
        xp, lp, lm = db_monster['xp'], db_player['level'], db_monster['level']
        perc = xp if lp - lm <= 0 else xp + abs(0.25 * (db_player['level'] - db_monster['level']))
        data_xp = calc_xp(db_player['xp'], db_player['level'])

        if db_player['xp'] < 32:
            xpm = data_xp[2]
            xpr = xpm
        else:
            if 1 < db_player['level'] < 7:
                percent = [randint(50, 75), randint(40, 60), randint(30, 55), randint(25, 45), randint(20, 40)]
                xpm = data_xp[1] - data_xp[2]
                xpr = int(xpm / 100 * percent[db_player['level'] - 2])
            else:
                xpm = data_xp[1] - data_xp[2]
                xpr = int(xpm / 100 * perc)
        if xpr < xpm / 100 * 1:
            xpr = int(xpm / 100 * 1)

        xp_reward = [int(xpr + xpr * 0.25), int(xpr), int(xpr * 0.25)]

        # chance de drop
        change = randint(1, 100)

        # depois da batalha
        if monster.status['hp'] > 0:
            await self.bot.data.add_xp(ctx, xp_reward[2])
            embed = discord.Embed(
                description=f"``{ctx.author.name.upper()} PERDEU!``",
                color=0x000000
            )
            img = "https://media1.tenor.com/images/09b085a6b0b33a9a9c8529a3d2ee1914/tenor.gif?itemid=5648908"
            if not data['rpg']['lower_net']:
                embed.set_image(url=img)
            embed.set_thumbnail(url=f"{db_player['img']}")
            await ctx.send(embed=embed)
        else:
            # premiação
            if data['rpg']['vip']:
                await self.bot.data.add_xp(ctx, xp_reward[0])
            else:
                await self.bot.data.add_xp(ctx, xp_reward[1])
            answer_ = await self.bot.db.add_money(ctx, db_monster['ethernya'], True)
            embed = discord.Embed(
                description=f"``{ctx.author.name.upper()} GANHOU!`` {answer_}",
                color=0x000000)
            img = "https://media1.tenor.com/images/a39aa52e78dfdc01934dd2b00c1b2a6e/tenor.gif?itemid=12772532"
            if not data['rpg']['lower_net']:
                embed.set_image(url=img)
            embed.set_thumbnail(url=f"{db_player['img']}")
            await ctx.send(embed=embed)

            if change < 25:
                if data['rpg']['vip']:
                    reward = [choice(db_monster['reward']) for _ in range(8)]
                else:
                    reward = [choice(db_monster['reward']) for _ in range(4)]
                if change == 1:
                    reward.append(choice(['Discharge_Crystal', 'Crystal_of_Energy', 'Acquittal_Crystal']))
                response = await self.bot.db.add_reward(ctx, reward)
                await ctx.send('<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS DO RPG** ✨ '
                               '{}'.format(response))

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if change < 10 and player.status['hp'] > 0 and db_player['level'] > 25:

            equips_list = list()
            for ky in self.bot.config['equips'].keys():
                for k, v in self.bot.config['equips'][ky].items():
                    equips_list.append((k, v))

            list_items = []
            for i_, amount in self.w_s.items():
                list_items += [i_] * amount
            armor_or_shield = choice(list_items)

            try:
                update['rpg']['items'][armor_or_shield] += 1
            except KeyError:
                update['rpg']['items'][armor_or_shield] = 1

            rew = None
            for i in equips_list:
                if i[0] == armor_or_shield:
                    rew = i[1]

            if rew is not None:
                img = choice(git)
                embed = discord.Embed(color=self.bot.color)
                embed.set_image(url=img)
                await ctx.send(embed=embed)
                await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ESPADA/ESCUDO** ✨\n'
                               f'{rew["icon"]} `1 {rew["name"]}` **{rew["rarity"]}**')

        update['config']['battle'] = False
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(Battle(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mBATTLE\033[1;32m foi carregado com sucesso!\33[m')
