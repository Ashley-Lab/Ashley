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
raid_rank = {}
p_raid = {}
m_raid = {}
money = {}
xp_tot = {}
xp_off = {}
git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class Raid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.m = self.bot.config['battle']['monsters']
        self.w_s = self.bot.config['attribute']['chance_weapon']

    def choice_monster(self, data, db_player, id_author):
        # configuração do monstro
        lvl = raid_rank[id_author]
        _min, _max = 25 + lvl if lvl < 31 else 59, 30 + lvl if lvl < 31 else 60
        db_monster = choice([m for m in self.m if _min < self.m[self.m.index(m)]['level'] < _max])
        db_monster['lower_net'] = True if data['rpg']['lower_net'] else False
        db_monster['enemy'] = db_player
        db_monster["pdef"] = raid_rank[id_author] * 25
        db_monster["mdef"] = raid_rank[id_author] * 25

        if "hp" in db_monster['status']:
            del db_monster['status']['hp']
        if "mp" in db_monster['status']:
            del db_monster['status']['mp']

        # bonus status monster
        for k in db_monster["status"].keys():
            if db_player['level'] > 25:
                db_monster["status"][k] += randint(2, 4)

        for k in db_monster["status"].keys():
            for sts in db_player['equipped_items'].keys():
                if db_player['equipped_items'][sts] is not None:
                    if k == "luk":
                        db_monster["status"][k] += randint(1, 2)
                    if k in ["atk", "con"]:
                        db_monster["status"][k] += randint(1, 2)
        return db_monster

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='raid', aliases=['onda', 'orda'])
    async def raid(self, ctx):
        """Comando usado pra batalhar no rpg da ashley
        Use ash raid"""
        global raid_rank, m_raid, p_raid, money, xp_tot, xp_off, evasion
        xp_off[ctx.author.id] = False
        evasion[ctx.author.id] = [[0, False], [0, False]]

        raid_rank[ctx.author.id] = 0
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

        if data['rpg']['level'] < 26:
            msg = '<:negate:721581573396496464>│``VOCE PRECISA ESTA NO NIVEL 26 OU MAIOR PARA IR UMA RAID!\n' \
                  'OLHE O SEU NIVEL NO COMANDO:`` **ASH SKILL**'
            embed = discord.Embed(color=self.bot.color, description=msg)
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
        db_player = data['rpg']
        db_player["img"] = ctx.author.avatar_url_as(format="png")
        db_player['name'] = ctx.author.name
        db_player["pdef"] = 0
        db_player["mdef"] = 0
        set_e = list()

        # bonus status player
        eq = dict()
        for ky in self.bot.config["equips"].keys():
            for kk, vv in self.bot.config["equips"][ky].items():
                eq[kk] = vv

        for k in db_player["status"].keys():
            try:
                db_player["status"][k] += self.bot.config["skills"][db_player['class']]['modifier'][k]
                if db_player['level'] > 25:
                    db_player["status"][k] += self.bot.config["skills"][db_player['next_class']]['modifier'][k]
            except KeyError:
                pass

        for c in db_player['equipped_items'].keys():
            if db_player['equipped_items'][c] is None:
                continue

            if c in set_value:
                set_e.append(str(c))

            db_player["pdef"] += eq[db_player['equipped_items'][c]]['pdef']
            db_player["mdef"] += eq[db_player['equipped_items'][c]]['mdef']
            for name in db_player["status"].keys():
                try:
                    db_player["status"][name] += eq[db_player['equipped_items'][c]]['modifier'][name]
                except KeyError:
                    pass

        for kkk in self.bot.config["set_equips"].values():
            if kkk['set'] == set_e:
                for name in db_player["status"].keys():
                    try:
                        db_player["status"][name] += kkk['modifier'][name]
                    except KeyError:
                        pass

        # criando as entidade do jogador...
        p_raid[ctx.author.id] = Entity(db_player, True, raid=True)

        # ======================================================================================================
        # ----------------------------------- SYSTEM RAID MONSTERS / BOSS --------------------------------------
        # ======================================================================================================

        db_monster = self.choice_monster(data, db_player, ctx.author.id)
        # criando as entidade do monstro...
        m_raid[ctx.author.id] = Entity(db_monster, False, raid=True)
        m_raid[ctx.author.id].status['hp'] += raid_rank[ctx.author.id] * 100
        money[ctx.author.id] = db_monster['ethernya']
        xp_tot[ctx.author.id] = [(db_monster['xp'], db_monster['level'])]

        # durante a batalha
        while not self.bot.is_closed():

            # -----------------------------------------------------------------------------
            if p_raid[ctx.author.id].status['hp'] <= 0:
                break
            if m_raid[ctx.author.id].status['hp'] <= 0:
                raid_rank[ctx.author.id] += 1
                db_monster = self.choice_monster(data, db_player, ctx.author.id)
                msg = f"Voce derrotou o {raid_rank[ctx.author.id]}° monstro, proximo..."
                embed = discord.Embed(color=self.bot.color, title=msg)
                embed.set_image(url=db_monster['img'])
                await ctx.send(embed=embed)
                # criando as entidade do monstro...
                m_raid[ctx.author.id] = Entity(db_monster, False, raid=True)
                m_raid[ctx.author.id].status['hp'] += raid_rank[ctx.author.id] * 100
                money[ctx.author.id] += db_monster['ethernya']
                xp_tot[ctx.author.id].append((db_monster['xp'], db_monster['level']))

            skill = await p_raid[ctx.author.id].turn([m_raid[ctx.author.id].status, m_raid[ctx.author.id].rate,
                                                      m_raid[ctx.author.id].name, m_raid[ctx.author.id].lvl],
                                                     self.bot, ctx, raid_num=raid_rank[ctx.author.id])

            if skill == "BATALHA-CANCELADA":
                p_raid[ctx.author.id].status['hp'] = 0
                xp_off[ctx.author.id] = True

            if p_raid[ctx.author.id].status['hp'] <= 0:
                break
            if m_raid[ctx.author.id].status['hp'] <= 0:
                raid_rank[ctx.author.id] += 1
                db_monster = self.choice_monster(data, db_player, ctx.author.id)
                msg = f"Voce derrotou o {raid_rank[ctx.author.id]}° monstro, proximo..."
                embed = discord.Embed(color=self.bot.color, title=msg)
                embed.set_image(url=db_monster['img'])
                await ctx.send(embed=embed)
                # criando as entidade do monstro...
                m_raid[ctx.author.id] = Entity(db_monster, False, raid=True)
                m_raid[ctx.author.id].status['hp'] += raid_rank[ctx.author.id] * 100
                money[ctx.author.id] += db_monster['ethernya']
                xp_tot[ctx.author.id].append((db_monster['xp'], db_monster['level']))
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

            atk = int(p_raid[ctx.author.id].status['atk'] * 2)

            # player chance
            d20 = randint(1, 20)
            lvlp = int(p_raid[ctx.author.id].lvl / 10)
            prec = int(p_raid[ctx.author.id].status['prec'] / 2)
            chance_player = d20 + lvlp + prec

            # monster chance
            d16 = randint(1, 16)
            lvlm = int(m_raid[ctx.author.id].lvl / 10)
            agi = int(m_raid[ctx.author.id].status['agi'] / 3)
            chance_monster = d16 + lvlm + agi

            evasion[ctx.author.id][0][1] = False if chance_player > chance_monster else True
            if evasion[ctx.author.id][0][1] and evasion[ctx.author.id][0][0] > 1:
                chance_monster, evasion[ctx.author.id][0][1] = 0, False
            if not evasion[ctx.author.id][0][1]:
                evasion[ctx.author.id][0][0] = 0

            if chance_player > chance_monster:
                _eff = await m_raid[ctx.author.id].damage(skill, p_raid[ctx.author.id].level_skill, atk, ctx,
                                                          p_raid[ctx.author.id].name, p_raid[ctx.author.id].cc,
                                                          p_raid[ctx.author.id].img,
                                                          p_raid[ctx.author.id].status['luk'],
                                                          p_raid[ctx.author.id].effects)
                p_raid[ctx.author.id].effects = _eff
            else:

                if evasion[ctx.author.id][0][1]:
                    evasion[ctx.author.id][0][0] += 1

                embed = discord.Embed(
                    description=f"``{m_raid[ctx.author.id].name.upper()} EVADIU``",
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
            if p_raid[ctx.author.id].status['hp'] <= 0:
                break
            if m_raid[ctx.author.id].status['hp'] <= 0:
                raid_rank[ctx.author.id] += 1
                db_monster = self.choice_monster(data, db_player, ctx.author.id)
                msg = f"Voce derrotou o {raid_rank[ctx.author.id]}° monstro, proximo..."
                embed = discord.Embed(color=self.bot.color, title=msg)
                embed.set_image(url=db_monster['img'])
                await ctx.send(embed=embed)
                # criando as entidade do monstro...
                m_raid[ctx.author.id] = Entity(db_monster, False, raid=True)
                m_raid[ctx.author.id].status['hp'] += raid_rank[ctx.author.id] * 100
                money[ctx.author.id] += db_monster['ethernya']
                xp_tot[ctx.author.id].append((db_monster['xp'], db_monster['level']))

            skill = await m_raid[ctx.author.id].turn(m_raid[ctx.author.id].status['hp'], self.bot, ctx)

            if skill == "BATALHA-CANCELADA":
                p_raid[ctx.author.id].status['hp'] = 0
                xp_off[ctx.author.id] = True

            if p_raid[ctx.author.id].status['hp'] <= 0:
                break
            if m_raid[ctx.author.id].status['hp'] <= 0:
                raid_rank[ctx.author.id] += 1
                db_monster = self.choice_monster(data, db_player, ctx.author.id)
                msg = f"Voce derrotou o {raid_rank[ctx.author.id]}° monstro, proximo..."
                embed = discord.Embed(color=self.bot.color, title=msg)
                embed.set_image(url=db_monster['img'])
                await ctx.send(embed=embed)
                # criando as entidade do monstro...
                m_raid[ctx.author.id] = Entity(db_monster, False, raid=True)
                m_raid[ctx.author.id].status['hp'] += raid_rank[ctx.author.id] * 100
                money[ctx.author.id] += db_monster['ethernya']
                xp_tot[ctx.author.id].append((db_monster['xp'], db_monster['level']))
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

            bonus_raid = int(5 * raid_rank[ctx.author.id])
            raid_info = m_raid[ctx.author.id].cc
            raid_info[0] = bonus_raid

            atk_bonus = m_raid[ctx.author.id].status['atk'] * 1 if p_raid[ctx.author.id].lvl > 25 else \
                m_raid[ctx.author.id].status['atk'] * 0.25
            atk = int(m_raid[ctx.author.id].status['atk'] + atk_bonus)

            # monster chance
            d20 = randint(1, 20)
            lvlm = int(m_raid[ctx.author.id].lvl / 10)
            prec = int(m_raid[ctx.author.id].status['prec'] / 2)
            chance_monster = d20 + lvlm + prec

            # player chance
            d16 = randint(1, 16)
            lvlp = int(p_raid[ctx.author.id].lvl / 10)
            agi = int(p_raid[ctx.author.id].status['agi'] / 3)
            chance_player = d16 + lvlp + agi

            evasion[ctx.author.id][1][1] = False if chance_monster > chance_player else True
            if evasion[ctx.author.id][1][1] and evasion[ctx.author.id][1][0] > 1:
                chance_player, evasion[ctx.author.id][1][1] = 0, False
            if not evasion[ctx.author.id][1][1]:
                evasion[ctx.author.id][1][0] = 0

            if chance_monster > chance_player:
                _eff = await p_raid[ctx.author.id].damage(skill, m_raid[ctx.author.id].level_skill, atk, ctx,
                                                          m_raid[ctx.author.id].name, raid_info,
                                                          m_raid[ctx.author.id].img,
                                                          m_raid[ctx.author.id].status['luk'],
                                                          m_raid[ctx.author.id].effects)
                m_raid[ctx.author.id].effects = _eff
            else:

                if evasion[ctx.author.id][1][1]:
                    evasion[ctx.author.id][1][0] += 1

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
        perc = 0

        for xp_now in xp_tot[ctx.author.id]:
            test = xp_now[1] - 5 < db_player['level'] < xp_now[1] + 5
            xpn = xp_now[0] if test else 1
            xp, lp, lm = xpn, db_player['level'], xp_now[1]
            bonus = abs(0.5 * (db_player['level'] - xp_now[1]))
            perc += xp if lp - lm <= 0 else xp + bonus if test else xp

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

        xp_reward = [int(xpr + xpr * 0.5), int(xpr), int(xpr * 0.5)]

        # chance de drop
        change = randint(1, 100) + raid_rank[ctx.author.id]

        # depois da raid
        if raid_rank[ctx.author.id] <= 0:
            if not xp_off[ctx.author.id]:
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
            answer_ = await self.bot.db.add_money(ctx, money[ctx.author.id], True)
            msg = f"``{ctx.author.name.upper()} GANHOU!`` {answer_}"
            embed = discord.Embed(description=msg, color=0x000000)
            img = "https://media1.tenor.com/images/a39aa52e78dfdc01934dd2b00c1b2a6e/tenor.gif?itemid=12772532"
            if not data['rpg']['lower_net']:
                embed.set_image(url=img)
            embed.set_thumbnail(url=f"{db_player['img']}")
            await ctx.send(embed=embed)

            if change < 75:
                if data['rpg']['vip']:
                    reward = [choice(db_monster['reward']) for _ in range(8)]
                else:
                    reward = [choice(db_monster['reward']) for _ in range(4)]

                raid_reward = ["soul_crystal_of_love", "soul_crystal_of_love", "soul_crystal_of_love",
                               "soul_crystal_of_hope", "soul_crystal_of_hope", "soul_crystal_of_hope",
                               "soul_crystal_of_hate", "soul_crystal_of_hate", "soul_crystal_of_hate",
                               "fused_diamond", "fused_diamond", "fused_ruby", "fused_ruby",
                               "fused_sapphire", "fused_sapphire", "fused_emerald", "fused_emerald",
                               "unsealed_stone", "melted_artifact"]

                msg = "\n"

                if raid_rank[ctx.author.id] >= 5:
                    reward.append(choice(raid_reward))
                    msg += "🎊 **PARABENS** 🎉│``Ganhou`` **+1** ``item especial por matar`` **5** ``monstros``\n"

                if raid_rank[ctx.author.id] >= 10:
                    reward.append(choice(raid_reward))
                    msg += "🎊 **PARABENS** 🎉│``Ganhou`` **+1** ``item especial por matar`` **10** ``monstros``\n"

                if raid_rank[ctx.author.id] >= 15:
                    reward.append(choice(raid_reward))
                    msg += "🎊 **PARABENS** 🎉│``Ganhou`` **+1** ``item especial por matar`` **15** ``monstros``\n"

                if raid_rank[ctx.author.id] >= 20:
                    reward.append(choice(raid_reward))
                    msg += "🎊 **PARABENS** 🎉│``Ganhou`` **+1** ``item especial por matar`` **20** ``monstros``\n"

                if raid_rank[ctx.author.id] >= 25:
                    reward.append(choice(raid_reward))
                    msg += "🎊 **PARABENS** 🎉│``Ganhou`` **+1** ``item especial por matar`` **25** ``monstros``\n"

                if raid_rank[ctx.author.id] >= 30:
                    reward.append(choice(raid_reward))
                    msg += "🎊 **PARABENS** 🎉│``Ganhou`` **+1** ``item especial por matar`` **30** ``monstros``\n"

                if db_player['level'] > 25:
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

                if change < 50:
                    if data['rpg']['vip']:
                        reward.append(choice(['Discharge_Crystal', 'Crystal_of_Energy', 'Acquittal_Crystal']))
                        reward.append(choice(['Discharge_Crystal', 'Crystal_of_Energy', 'Acquittal_Crystal']))
                    else:
                        reward.append(choice(['Discharge_Crystal', 'Crystal_of_Energy', 'Acquittal_Crystal']))

                response = await self.bot.db.add_reward(ctx, reward)
                await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ITENS DO RPG** ✨ '
                               f'{response}\n{msg}')

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if change < 10 and raid_rank[ctx.author.id] > 0 and db_player['level'] > 25:

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

        if raid_rank[ctx.author.id] > 0:
            if raid_rank[ctx.author.id] > update['user']['raid']:
                update['user']['raid'] = raid_rank[ctx.author.id]
                await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCÊ CONSEGUIU MATAR:`` "
                               f"**{raid_rank[ctx.author.id]}** ``MONSTROS!``\n **ESSE É SEU NOVO RECORD!** "
                               f"``APROVEITE E OLHE O COMANDO:`` **ASH TOP RAID**")
            else:
                await ctx.send(f"<:confirmed:721581574461587496>│``VOCÊ CONSEGUIU MATAR:`` "
                               f"**{raid_rank[ctx.author.id]}** ``MONSTROS!``")

        if raid_rank[ctx.author.id] >= 10:
            try:
                update['inventory']['boss_key'] += 1
            except KeyError:
                update['inventory']['boss_key'] = 1
            await ctx.send(f"<:confirmed:721581574461587496>│🎊 **PARABENS** 🎉 ``Por matar`` **10+** ``monstros,"
                           f" voce dropou`` ✨ <:bosskey:766048658470600714> ✨ ``1`` **Boss Key** "
                           f"``adicionando ao seu inventario o item com sucesso...``")

        update['config']['battle'] = False
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(Raid(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mRAID\033[1;32m foi carregado com sucesso!\33[m')
