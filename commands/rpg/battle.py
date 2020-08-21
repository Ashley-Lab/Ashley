import discord

from asyncio import sleep
from discord.ext import commands
from random import randint, choice
from resources.entidade import Entity
from resources.check import check_it
from resources.db import Database
from resources.img_edit import calc_xp


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.m = self.bot.config['battle']['monsters']

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

        update['inventory']['coins'] -= 10
        update['config']['battle'] = True
        await self.bot.db.update_data(data, update, 'users')

        try:
            if data['inventory']['coins'] < 10:
                embed = discord.Embed(
                    color=self.bot.color,
                    description='<:negate:721581573396496464>│``VOCE PRECISA DE PELO MENOS 10 FICHAS!``')
                return await ctx.send(embed=embed)
        except KeyError:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE NÃO TEM FICHA!``')
            return await ctx.send(embed=embed)

        if not data['rpg']['status']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
            return await ctx.send(embed=embed)

        # configuração do player
        db_player = dict(data['rpg'])
        db_player['Name'] = ctx.author.name
        db_player["img"] = ctx.author.avatar_url_as(format="png")
        player = Entity(db_player, True)

        # configuração do monstro
        lvl = data['rpg']['Level']
        dif = 1 if lvl == 1 else 3 if 1 < lvl < 5 else 5 if 5 < lvl < 40 else 10
        min_, max_ = lvl - dif if lvl - dif > 0 else 0, lvl + dif
        db_monster = choice([m for m in self.m if min_ < self.m[self.m.index(m)]['Level'] < max_])
        db_monster['lower_net'] = True if data['rpg']['lower_net'] else False
        db_monster['enemy'] = data['rpg']['Level']
        monster = Entity(db_monster, False)

        # durante a batalha
        while not self.bot.is_closed():

            # -----------------------------------------------------------------------------
            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break

            atk = await player.turn([monster.status, monster.rate, monster.name, monster.lvl], self.bot, ctx)

            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break
            # -----------------------------------------------------------------------------

            if atk == "COMANDO-CANCELADO":
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['battle'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito`` '
                                      '**COMANDO CANCELADO**')

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

            if randint(0, 20) + player.status['prec'] > randint(0, 16) + monster.status['agi']:
                await monster.damage(atk, player.status['atk'], ctx, player.name)
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

            atk = await monster.turn(monster.status['hp'], self.bot, ctx)

            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break
            # -----------------------------------------------------------------------------

            if atk == "COMANDO-CANCELADO":
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['battle'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito`` '
                                      '**COMANDO CANCELADO**')

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

            if randint(0, 20) + monster.status['prec'] > randint(0, 16) + player.status['agi']:
                await player.damage(atk, monster.status['atk'], ctx, monster.name)
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
        xp, lp, lm = db_monster['XP'], db_player['Level'], db_monster['Level']
        perc = xp if lp - lm <= 0 else xp + abs(0.25 * (db_player['Level'] - db_monster['Level']))
        data_xp = calc_xp(db_player['XP'], db_player['Level'])

        if db_player['XP'] < 32:
            xpm = data_xp[2]
            xpr = xpm
        else:
            if 1 < db_player['Level'] < 7:
                percent = [randint(50, 75), randint(40, 60), randint(30, 55), randint(25, 45), randint(20, 40)]
                xpm = data_xp[1] - data_xp[2]
                xpr = int(xpm / 100 * percent[db_player['Level'] - 2])
            else:
                xpm = data_xp[1] - data_xp[2]
                xpr = int(xpm / 100 * perc)
        if xpr < xpm / 100 * 1:
            xpr = int(xpm / 100 * 1)

        xp_reward = [int(xpr + xpr * 0.5), int(xpr), int(xpr / 2)]
        print(f"Player: {db_player['Name']} | Percent: {perc} | XPR/XPM: {xpr}/{xpm} | Reward: {xp_reward}")

        # depois da batalha
        if monster.status['hp'] > 0:
            if data['rpg']['vip']:
                await self.bot.data.add_xp(ctx, xp_reward[1])
            else:
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
            change = randint(1, 100)
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
        update['config']['battle'] = False
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(Battle(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mBATTLE\033[1;32m foi carregado com sucesso!\33[m')
