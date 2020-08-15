import discord

from asyncio import sleep
from discord.ext import commands
from random import randint, choice
from resources.entidade import Entity
from resources.check import check_it
from resources.db import Database


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

        db_player = dict(data['rpg'])
        db_player['Name'] = ctx.author.name
        db_player["img"] = ctx.author.avatar_url_as(format="png")

        if db_player['lower_net']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:confirmed:721581574461587496>│``MODO SEM IMAGENS ATIVADO``')
            await ctx.send(embed=embed)

        min_ = data['rpg']['Level'] - 9 if data['rpg']['Level'] - 9 > 0 else 0
        max_ = data['rpg']['Level'] + 9
        db_monster = choice([m for m in self.m if min_ < self.m[self.m.index(m)]['Level'] < max_])
        db_monster['lower_net'] = True if data['rpg']['lower_net'] else False
        if data['rpg']['vip']:
            db_monster['XP'] += db_monster['XP'] // 2
        player = Entity(db_player, True)
        monster = Entity(db_monster, False)

        # durante a batalha
        while not self.bot.is_closed():
            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break

            atk = await player.turn(monster.status['hp'], self.bot, ctx)

            if atk == "COMANDO-CANCELADO":
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['battle'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito`` '
                                      '**COMANDO CANCELADO**')

            await sleep(1)
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

            if player.status['hp'] <= 0 or monster.status['hp'] <= 0:
                break

            atk = await monster.turn(monster.status['hp'], self.bot, ctx)

            if atk == "COMANDO-CANCELADO":
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['battle'] = False
                await self.bot.db.update_data(data, update, 'users')
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito`` '
                                      '**COMANDO CANCELADO**')

            await sleep(1)
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
            await sleep(2)

        # depois da batalha
        if monster.status['hp'] > 0:
            await self.bot.data.add_xp(ctx, db_monster['XP'] // 4)
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
            await self.bot.data.add_xp(ctx, db_monster['XP'])
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
                    reward = list(db_monster['reward'])
                else:
                    reward = [choice(db_monster['reward']) for _ in range(3)]
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
