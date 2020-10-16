import discord

from asyncio import sleep, TimeoutError
from discord.ext import commands
from random import randint
from resources.entidade import Entity
from resources.check import check_it
from resources.db import Database

player_1 = {}
player_2 = {}


class PVP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def config_player(self, user, data, lower_net):
        # configuração do player
        set_value = ["shoulder", "breastplate", "gloves", "leggings", "boots"]
        db_player = data['rpg']
        db_player["img"] = user.avatar_url_as(format="png")
        db_player['name'] = user.name
        db_player["armor"] = 0
        db_player["lower_net"] = lower_net
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

            db_player["armor"] += eq[db_player['equipped_items'][c]]['armor']
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

        return db_player

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='pvp')
    async def pvp(self, ctx, member: discord.Member = None):
        """Comando usado pra ir PVP no rpg da ashley
        Use ash pvp"""
        if member is None:
            return await ctx.send("<:alert:739251822920728708>│``Você precisa mencionar alguem!``")
        if member.id == ctx.author.id:
            return await ctx.send("<:alert:739251822920728708>│``Você não pode ir PVP consigo mesmo!``")

        def check(m):
            return m.author.id == member.id and m.content.upper() in ['SIM', 'NÃO', 'S', 'N', 'NAO', 'CLARO']

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = await self.bot.db.get_data("user_id", member.id, "users")

        if data_user['config']['playing']:
            return await ctx.send("<:alert:739251822920728708>│``Você está jogando, aguarde para quando"
                                  " vocÊ estiver livre!``")

        if not data_user['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
            return await ctx.send(embed=embed)

        if data_user['config']['battle']:
            msg = '<:negate:721581573396496464>│``VOCE ESTÁ BATALHANDO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if data_user['rpg']['level'] < 26:
            msg = '<:negate:721581573396496464>│``VOCE PRECISA ESTA NO NIVEL 26 OU MAIOR PARA TROCAR EQUIPAMENTOS!\n' \
                  'OLHE O SEU NIVEL NO COMANDO:`` **ASH SKILL**'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)

        if data_member['config']['playing']:
            return await ctx.send("<:alert:739251822920728708>│``O usuario está jogando, aguarde para quando"
                                  " ele estiver livre!``")

        if not data_member['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``O USUARIO DEVE USAR O COMANDO`` **ASH RPG** ``ANTES!``')
            return await ctx.send(embed=embed)

        if data_member['config']['battle']:
            msg = '<:negate:721581573396496464>│``O USUARIO ESTÁ BATALHANDO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if data_member['rpg']['level'] < 26:
            msg = '<:negate:721581573396496464>│``O USUARIO PRECISA ESTA NO NIVEL 26 OU MAIOR PARA TROCAR ' \
                  'EQUIPAMENTOS!\nPEÇA PARA ELE OLHAR O NIVEL NO COMANDO:`` **ASH SKILL**'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        await ctx.send(f'<a:ash:525105075446743041>│{member.mention}, ``VOCÊ RECEBEU UM DESAFIO PARA IR PVP '
                       f'COM`` {ctx.author.mention} ``DIGITE`` **SIM** ``OU`` **NÃO** ``PARA ACEITAR OU REGEITAR!``')
        try:
            answer = await self.bot.wait_for('message', check=check, timeout=30.0)
        except TimeoutError:
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, ele(a) demorou muito pra responder:`` '
                                  '**COMANDO CANCELADO**')

        if answer.content.upper() not in ['SIM', 'S', 'CLARO']:
            return await ctx.send(f'<:negate:721581573396496464>│{ctx.author.mention} ``SEU PEDIDO FOI REJEITADO...``')

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_user, update_member = data_user, data_member
        update_user['config']['battle'] = True
        await self.bot.db.update_data(data_user, update_user, 'users')
        update_member['config']['battle'] = True
        await self.bot.db.update_data(data_member, update_member, 'users')

        if data_user['rpg']['lower_net'] and data_member['rpg']['lower_net']:
            lower_net = True
        else:
            lower_net = False

        player_1_data = self.config_player(ctx.author, data_user, lower_net)
        player_2_data = self.config_player(member, data_member, lower_net)

        # criando as entidades...
        player_1[ctx.author.id] = Entity(player_1_data, True, True)
        player_2[member.id] = Entity(player_2_data, True, True)

        # durante a batalha
        while not self.bot.is_closed():

            # -----------------------------------------------------------------------------
            if player_1[ctx.author.id].status['hp'] <= 0 or player_2[member.id].status['hp'] <= 0:
                break

            skill = await player_1[ctx.author.id].turn([player_2[member.id].status, player_2[member.id].rate,
                                                        player_2[member.id].name, player_2[member.id].lvl],
                                                       self.bot, ctx, ctx.author)

            if skill == "BATALHA-CANCELADA":
                player_1[ctx.author.id].status['hp'] = 0

            if player_1[ctx.author.id].status['hp'] <= 0 or player_2[member.id].status['hp'] <= 0:
                break
            # -----------------------------------------------------------------------------

            if skill == "COMANDO-CANCELADO":
                player_1[ctx.author.id].status['hp'] = 0
                await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito`` **COMANDO CANCELADO**')

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------
            lvlp1 = player_1[ctx.author.id].lvl
            lvlp2 = player_2[member.id].lvl
            atk = int(player_1[ctx.author.id].status['atk'] * 2)
            p1_chance = randint(1, 20 + lvlp1) + player_1[ctx.author.id].status['prec']
            p2_chance = randint(1, 16 + lvlp2) + player_2[member.id].status['agi']
            if p1_chance > p2_chance:
                await player_2[member.id].damage(skill, player_1[ctx.author.id].level_skill, atk, ctx,
                                                 player_1[ctx.author.id].name)
            else:
                embed = discord.Embed(
                    description=f"``{player_2[member.id].name.upper()} EVADIU``",
                    color=0x000000
                )
                if not lower_net:
                    embed.set_image(url="https://storage.googleapis.com/ygoprodeck.com/pics_artgame/47529357.jpg")
                embed.set_thumbnail(url=f"{player_2_data['img']}")
                await ctx.send(embed=embed)

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

            # -----------------------------------------------------------------------------
            if player_1[ctx.author.id].status['hp'] <= 0 or player_2[member.id].status['hp'] <= 0:
                break

            skill = await player_2[member.id].turn([player_1[ctx.author.id].status, player_1[ctx.author.id].rate,
                                                    player_1[ctx.author.id].name, player_1[ctx.author.id].lvl],
                                                   self.bot, ctx, member)

            if skill == "BATALHA-CANCELADA":
                player_2[member.id].status['hp'] = 0

            if player_1[ctx.author.id].status['hp'] <= 0 or player_2[member.id].status['hp'] <= 0:
                break
            # -----------------------------------------------------------------------------

            if skill == "COMANDO-CANCELADO":
                player_2[member.id].status['hp'] = 0
                await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito`` **COMANDO CANCELADO**')

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------
            lvlp2 = player_2[member.id].lvl
            lvlp1 = player_1[ctx.author.id].lvl
            atk = int(player_2[member.id].status['atk'] * 2)
            p2_chance = randint(1, 20 + lvlp2) + player_2[member.id].status['prec']
            p1_chance = randint(1, 16 + lvlp1) + player_1[ctx.author.id].status['agi']
            if p2_chance > p1_chance:
                await player_1[ctx.author.id].damage(skill, player_2[member.id].level_skill, atk, ctx,
                                                     player_2[member.id].name)
            else:
                embed = discord.Embed(
                    description=f"``{ctx.author.name.upper()} EVADIU``",
                    color=0x000000
                )
                if not lower_net:
                    embed.set_image(url="https://storage.googleapis.com/ygoprodeck.com/pics_artgame/47529357.jpg")
                embed.set_thumbnail(url=f"{player_1_data['img']}")
                await ctx.send(embed=embed)

            # --------======== TEMPO DE ESPERA ========--------
            await sleep(0.5)
            # --------======== ............... ========--------

        if player_1[ctx.author.id].status['hp'] <= 0:
            await ctx.send(f"<:confirmed:721581574461587496>│🎊 **PARABENS** 🎉 {member.mention} ``VOCE GANHOU!``")
        if player_2[member.id].status['hp'] <= 0:
            await ctx.send(f"<:confirmed:721581574461587496>│🎊 **PARABENS** 🎉 {ctx.author.mention} ``VOCE GANHOU!``")

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_user, update_member = data_user, data_member
        update_user['config']['battle'] = False
        await self.bot.db.update_data(data_user, update_user, 'users')
        update_member['config']['battle'] = False
        await self.bot.db.update_data(data_member, update_member, 'users')


def setup(bot):
    bot.add_cog(PVP(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPVP\033[1;32m foi carregado com sucesso!\33[m')
