import discord

import time as date
from asyncio import sleep
from discord.ext import commands
from random import randint, choice
from resources.entidade import Entity
from resources.check import check_it
from resources.db import Database
from resources.img_edit import calc_xp
from datetime import datetime

evasion = {}
player = {}
monster = {}
xp_off = {}
git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.m = self.bot.config['battle']['monsters']
        self.w_s = self.bot.config['attribute']['chance_weapon']
        self.db_monster = {}
        self.db_player = {}

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='battle', aliases=['batalha', 'batalhar'])
    async def battle(self, ctx):
        """Comando usado pra batalhar no rpg da ashley
        Use ash battle"""
        global player, monster, xp_off, evasion
        xp_off[ctx.author.id] = False
        evasion[ctx.author.id] = [[0, False], [0, False]]

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if data['config']['battle']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE JÁ ESTÁ BATALHANDO!``')
            return await ctx.send(embed=embed)

        if not data['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
            return await ctx.send(embed=embed)

        ct = 50
        if data['rpg']['active']:
            date_old = data['rpg']['activated_at']
            date_now = datetime.today()
            days = abs((date_old - date_now).days)
            if days <= 10:
                ct = 5

        try:
            if data['inventory']['coins'] < ct:
                embed = discord.Embed(
                    color=self.bot.color,
                    description=f'<:negate:721581573396496464>│``VOCE PRECISA DE + DE {ct} FICHAS PARA BATALHAR!``\n'
                                f'**OBS:** ``USE O COMANDO`` **ASH SHOP** ``PARA COMPRAR FICHAS!``')
                return await ctx.send(embed=embed)
        except KeyError:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE NÃO TEM FICHA!``')
            return await ctx.send(embed=embed)

        update['inventory']['coins'] -= ct
        update['config']['battle'] = True
        await self.bot.db.update_data(data, update, 'users')

        # configuração do player
        set_value = ["shoulder", "breastplate", "gloves", "leggings", "boots"]
        self.db_player[ctx.author.id] = data['rpg']
        self.db_player[ctx.author.id]["img"] = ctx.author.avatar_url_as(format="png")
        self.db_player[ctx.author.id]['name'] = ctx.author.name
        self.db_player[ctx.author.id]["pdef"] = 0
        self.db_player[ctx.author.id]["mdef"] = 0
        set_e = list()

        # bonus status player
        eq = dict()
        for ky in self.bot.config["equips"].keys():
            for kk, vv in self.bot.config["equips"][ky].items():
                eq[kk] = vv

        for k in self.db_player[ctx.author.id]["status"].keys():
            try:
                temp = self.bot.config["skills"][self.db_player[ctx.author.id]['class']]['modifier'][k]
                self.db_player[ctx.author.id]["status"][k] += temp
                if self.db_player[ctx.author.id]['level'] > 25:
                    temp_2 = self.bot.config["skills"][self.db_player[ctx.author.id]['next_class']]['modifier'][k]
                    self.db_player[ctx.author.id]["status"][k] += temp_2
            except KeyError:
                pass

        for c in self.db_player[ctx.author.id]['equipped_items'].keys():
            if self.db_player[ctx.author.id]['equipped_items'][c] is None:
                continue

            if c in set_value:
                set_e.append(str(c))

            self.db_player[ctx.author.id]["pdef"] += eq[self.db_player[ctx.author.id]['equipped_items'][c]]['pdef']
            self.db_player[ctx.author.id]["mdef"] += eq[self.db_player[ctx.author.id]['equipped_items'][c]]['mdef']
            for name in self.db_player[ctx.author.id]["status"].keys():
                try:
                    temp_3 = eq[self.db_player[ctx.author.id]['equipped_items'][c]]['modifier'][name]
                    self.db_player[ctx.author.id]["status"][name] += temp_3
                except KeyError:
                    pass

        for kkk in self.bot.config["set_equips"].values():
            if kkk['set'] == set_e:
                for name in self.db_player[ctx.author.id]["status"].keys():
                    try:
                        self.db_player[ctx.author.id]["status"][name] += kkk['modifier'][name]
                    except KeyError:
                        pass

        # configuração do monstro
        lvl = data['rpg']['level']
        dif = 2 if lvl < 2 else 5 if 2 <= lvl <= 9 else 10 if 10 <= lvl <= 30 else 15
        max_ = lvl + dif if lvl + dif < 61 else 60
        min_ = lvl - 5 if lvl - 5 > 1 else 1
        min_ = min_ if min_ < 55 else 55
        if ctx.author.id in self.db_monster:
            del self.db_monster[ctx.author.id]

        _monster = choice([m for m in self.m if min_ < self.m[self.m.index(m)]['level'] < max_])
        self.db_monster[ctx.author.id] = _monster.copy()

        if "hp" in self.db_monster[ctx.author.id]['status']:
            del self.db_monster[ctx.author.id]['status']['hp']
        if "mp" in self.db_monster[ctx.author.id]['status']:
            del self.db_monster[ctx.author.id]['status']['mp']

        self.db_monster[ctx.author.id]['lower_net'] = True if data['rpg']['lower_net'] else False
        self.db_monster[ctx.author.id]['enemy'] = self.db_player[ctx.author.id]
        self.db_monster[ctx.author.id]["pdef"] = 0 + lvl
        self.db_monster[ctx.author.id]["mdef"] = 0 + lvl

        # bonus status monster
        for k in self.db_monster[ctx.author.id]["status"].keys():
            if self.db_player[ctx.author.id]['level'] > 25:
                self.db_monster[ctx.author.id]["status"][k] += randint(2, 4)

        for k in self.db_monster[ctx.author.id]["status"].keys():
            for sts in self.db_player[ctx.author.id]['equipped_items'].keys():
                if self.db_player[ctx.author.id]['equipped_items'][sts] is not None:
                    if k == "luk":
                        self.db_monster[ctx.author.id]["status"][k] += 1
                    if k in ["atk", "con"]:
                        self.db_monster[ctx.author.id]["status"][k] += randint(1, 2)

        # criando as entidades...
        player[ctx.author.id] = Entity(self.db_player[ctx.author.id], True)
        monster[ctx.author.id] = Entity(self.db_monster[ctx.author.id], False)

        # durante a batalha
        while not self.bot.is_closed():

            # -----------------------------------------------------------------------------
            if player[ctx.author.id].status['hp'] <= 0 or monster[ctx.author.id].status['hp'] <= 0:
                break

            skill = await player[ctx.author.id].turn([monster[ctx.author.id].status, monster[ctx.author.id].rate,
                                                      monster[ctx.author.id].name, monster[ctx.author.id].lvl],
                                                     self.bot, ctx)

            if skill == "BATALHA-CANCELADA":
                player[ctx.author.id].status['hp'] = 0
                xp_off[ctx.author.id] = True

            if player[ctx.author.id].status['hp'] <= 0 or monster[ctx.author.id].status['hp'] <= 0:
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

            atk = int(player[ctx.author.id].status['atk'] * 2)

            # player chance
            d20 = randint(1, 20)
            lvlp = int(player[ctx.author.id].lvl / 10)
            prec = int(player[ctx.author.id].status['prec'] / 2)
            chance_player = d20 + lvlp + prec

            # monster chance
            d16 = randint(1, 16)
            lvlm = int(monster[ctx.author.id].lvl / 10)
            agi = int(monster[ctx.author.id].status['agi'] / 3)
            chance_monster = d16 + lvlm + agi

            evasion[ctx.author.id][0][1] = False if chance_player > chance_monster else True
            if evasion[ctx.author.id][0][1] and evasion[ctx.author.id][0][0] > 1:
                chance_monster, evasion[ctx.author.id][0][1] = 0, False
            if not evasion[ctx.author.id][0][1]:
                evasion[ctx.author.id][0][0] = 0

            if chance_player > chance_monster:
                _eff = await monster[ctx.author.id].damage(skill, player[ctx.author.id].level_skill, atk, ctx,
                                                           player[ctx.author.id].name, player[ctx.author.id].cc,
                                                           player[ctx.author.id].img,
                                                           player[ctx.author.id].status['luk'],
                                                           player[ctx.author.id].effects)
                player[ctx.author.id].effects = _eff
            else:

                if evasion[ctx.author.id][0][1]:
                    evasion[ctx.author.id][0][0] += 1

                embed = discord.Embed(
                    description=f"``{monster[ctx.author.id].name.upper()} EVADIU``",
                    color=0x000000
                )
                if not data['rpg']['lower_net']:
                    embed.set_image(url="https://storage.googleapis.com/ygoprodeck.com/pics_artgame/47529357.jpg")
                embed.set_thumbnail(url=f"{self.db_monster[ctx.author.id]['img']}")
                await ctx.send(embed=embed)

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

            # -----------------------------------------------------------------------------
            if player[ctx.author.id].status['hp'] <= 0 or monster[ctx.author.id].status['hp'] <= 0:
                break

            skill = await monster[ctx.author.id].turn(monster[ctx.author.id].status['hp'], self.bot, ctx)

            if skill == "BATALHA-CANCELADA":
                player[ctx.author.id].status['hp'] = 0
                xp_off[ctx.author.id] = True

            if player[ctx.author.id].status['hp'] <= 0 or monster[ctx.author.id].status['hp'] <= 0:
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

            atk_bonus = monster[ctx.author.id].status['atk'] * 1 if player[ctx.author.id].lvl > 25 else \
                monster[ctx.author.id].status['atk'] * 0.25
            atk = int(monster[ctx.author.id].status['atk'] + atk_bonus)

            # monster chance
            d20 = randint(1, 20)
            lvlm = int(monster[ctx.author.id].lvl / 10)
            prec = int(monster[ctx.author.id].status['prec'] / 2)
            chance_monster = d20 + lvlm + prec

            # player chance
            d16 = randint(1, 16)
            lvlp = int(player[ctx.author.id].lvl / 10)
            agi = int(player[ctx.author.id].status['agi'] / 3)
            chance_player = d16 + lvlp + agi

            evasion[ctx.author.id][1][1] = False if chance_monster > chance_player else True
            if evasion[ctx.author.id][1][1] and evasion[ctx.author.id][1][0] > 1:
                chance_player, evasion[ctx.author.id][1][1] = 0, False
            if not evasion[ctx.author.id][1][1]:
                evasion[ctx.author.id][1][0] = 0

            if chance_monster > chance_player:
                _eff = await player[ctx.author.id].damage(skill, monster[ctx.author.id].level_skill, atk, ctx,
                                                          monster[ctx.author.id].name, monster[ctx.author.id].cc,
                                                          monster[ctx.author.id].img,
                                                          monster[ctx.author.id].status['luk'],
                                                          monster[ctx.author.id].effects)
                monster[ctx.author.id].effects = _eff
            else:

                if evasion[ctx.author.id][1][1]:
                    evasion[ctx.author.id][1][0] += 1

                embed = discord.Embed(
                    description=f"``{ctx.author.name.upper()} EVADIU``",
                    color=0x000000
                )
                if not data['rpg']['lower_net']:
                    embed.set_image(url="https://storage.googleapis.com/ygoprodeck.com/pics_artgame/47529357.jpg")
                embed.set_thumbnail(url=f"{self.db_player[ctx.author.id]['img']}")
                await ctx.send(embed=embed)

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

        # calculo de xp
        xp, lp = self.db_monster[ctx.author.id]['xp'], self.db_player[ctx.author.id]['level']
        lm = self.db_monster[ctx.author.id]['level']
        temp_4 = abs(0.15 * (self.db_player[ctx.author.id]['level'] - self.db_monster[ctx.author.id]['level']))
        perc = xp if lp - lm <= 0 else xp + temp_4
        data_xp = calc_xp(self.db_player[ctx.author.id]['xp'], self.db_player[ctx.author.id]['level'])

        if self.db_player[ctx.author.id]['xp'] < 32:
            xpm = data_xp[2]
            xpr = xpm

        else:
            if 1 < self.db_player[ctx.author.id]['level'] < 7:
                percent = [randint(50, 75), randint(40, 60), randint(30, 55), randint(25, 45), randint(20, 40)]
                xpm = data_xp[1] - data_xp[2]
                xpr = int(xpm / 100 * percent[self.db_player[ctx.author.id]['level'] - 2])

            else:
                xpm = data_xp[1] - data_xp[2]
                xpr = int(xpm / 100 * perc)

        if xpr < xpm / 100 * 1:
            xpr = int(xpm / 100 * 1)

        xp_reward = [int(xpr + xpr * 0.15), int(xpr), int(xpr * 0.15)]

        # chance de drop
        change = randint(1, 100)

        # depois da batalha
        if monster[ctx.author.id].status['hp'] > 0:
            if not xp_off[ctx.author.id]:
                await self.bot.data.add_xp(ctx, xp_reward[2])
            embed = discord.Embed(
                description=f"``{ctx.author.name.upper()} PERDEU!``",
                color=0x000000
            )
            img = "https://media1.tenor.com/images/09b085a6b0b33a9a9c8529a3d2ee1914/tenor.gif?itemid=5648908"
            if not data['rpg']['lower_net']:
                embed.set_image(url=img)
            embed.set_thumbnail(url=f"{self.db_player[ctx.author.id]['img']}")
            await ctx.send(embed=embed)
        else:
            # premiação
            if data['rpg']['vip']:
                await self.bot.data.add_xp(ctx, xp_reward[0])
            else:
                await self.bot.data.add_xp(ctx, xp_reward[1])
            answer_ = await self.bot.db.add_money(ctx, self.db_monster[ctx.author.id]['ethernya'], True)
            embed = discord.Embed(
                description=f"``{ctx.author.name.upper()} GANHOU!`` {answer_}",
                color=0x000000)
            img = "https://media1.tenor.com/images/a39aa52e78dfdc01934dd2b00c1b2a6e/tenor.gif?itemid=12772532"
            if not data['rpg']['lower_net']:
                embed.set_image(url=img)
            embed.set_thumbnail(url=f"{self.db_player[ctx.author.id]['img']}")
            await ctx.send(embed=embed)

            if change < 60:
                if data['rpg']['vip']:
                    reward = [choice(self.db_monster[ctx.author.id]['reward']) for _ in range(8)]
                else:
                    reward = [choice(self.db_monster[ctx.author.id]['reward']) for _ in range(4)]

                if self.db_player[ctx.author.id]['level'] > 25:
                    bonus = ['stone_crystal_white', 'stone_crystal_red', 'stone_crystal_green',
                             'stone_crystal_blue', 'stone_crystal_yellow']

                    if data['rpg']['vip']:
                        reward[0] = choice(bonus)
                        reward[1] = choice(bonus)
                        reward[2] = choice(bonus)
                        reward[3] = choice(bonus)

                    else:
                        reward[0] = choice(bonus)
                        reward[1] = choice(bonus)

                if change < 40:
                    if data['rpg']['vip']:
                        reward.append(choice(['Discharge_Crystal', 'Crystal_of_Energy', 'Acquittal_Crystal']))
                        reward.append(choice(['Discharge_Crystal', 'Crystal_of_Energy', 'Acquittal_Crystal']))
                    else:
                        reward.append(choice(['Discharge_Crystal', 'Crystal_of_Energy', 'Acquittal_Crystal']))

                if change < 15 and self.db_player[ctx.author.id]['level'] > 25:
                    date_ = date.localtime()
                    item_event = choice(["soul_crystal_of_love", "soul_crystal_of_love", "soul_crystal_of_love",
                                         "soul_crystal_of_hope", "soul_crystal_of_hope", "soul_crystal_of_hope",
                                         "soul_crystal_of_hate", "soul_crystal_of_hate", "soul_crystal_of_hate",
                                         "fused_diamond", "fused_diamond", "fused_ruby", "fused_ruby",
                                         "fused_sapphire", "fused_sapphire", "fused_emerald", "fused_emerald",
                                         "unsealed_stone", "melted_artifact"])

                    icon, name = self.bot.items[item_event][0], self.bot.items[item_event][1]
                    awards = choice(['images/elements/medallion.gif', 'images/elements/trophy.gif'])
                    msg = f"``VOCÊ GANHOU`` {icon} ``{name.upper()}`` ✨ **DO EVENTO DE HALLOWEEN** ✨"
                    file = discord.File(awards, filename="reward.gif")
                    embed = discord.Embed(title=msg, color=self.bot.color)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_image(url="attachment://reward.gif")

                    # config do evento atual.
                    if date_[0] == 2020 and date_[1] == 10:
                        reward.append(item_event)
                        await ctx.send(file=file, embed=embed)

                response = await self.bot.db.add_reward(ctx, reward)
                await ctx.send('<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS DO RPG** ✨ '
                               '{}'.format(response))

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if change < 10 and player[ctx.author.id].status['hp'] > 0 and self.db_player[ctx.author.id]['level'] > 25:

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

        elif change < 25 and player[ctx.author.id].status['hp'] > 0:

            equips_list = list()
            for ky in self.bot.config['equips'].keys():
                for k, v in self.bot.config['equips'][ky].items():
                    equips_list.append((k, v))

            sb = choice(['summon_box_sr', 'summon_box_sr', 'summon_box_sr', 'summon_box_sr', 'summon_box_sr',
                         'summon_box_ur', 'summon_box_ur', 'summon_box_ur', 'summon_box_secret'])

            try:
                update['rpg']['items'][sb] += 1
            except KeyError:
                update['rpg']['items'][sb] = 1

            rew = None
            for i in equips_list:
                if i[0] == sb:
                    rew = i[1]

            if rew is not None:
                await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU UM`` ✨ **CONSUMABLE** ✨\n'
                               f'{rew["icon"]} `1 {rew["name"]}` **{rew["rarity"]}**')

        update['config']['battle'] = False
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(Battle(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mBATTLE\033[1;32m foi carregado com sucesso!\33[m')
