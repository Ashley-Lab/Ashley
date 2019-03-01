import json
import discord
import resources.rpg_list

from aiohttp import ClientSession
from json import loads
from random import randint, choice
from discord.ext import commands
from time import localtime
from resources.check import check_it
# from resources.translation import t_
# from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

vida = 0x0B3B0B
hora = localtime()
P = choice(resources.rpg_list.PREMIOS)


class BattleRpg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.command()
    async def reset(self, ctx):
        if ctx.guild.id == 370680094533877763:
            await ctx.channel.send('Digite o ID do membro:')

            def check(m):
                return m.author == ctx.author and m.content.isdigit()

            id_membro = await self.bot.wait_for('message', check=check)
            record = self.bot.db.get_data("user_id", int(id_membro.content), "users")
            updates = record
            updates['batalhando'] = 0
            updates['provincia'] = 'nenhuma'
            try:
                self.bot.db.update_data(record, updates)
                await ctx.channel.send('RESETADO COM SUCESSO!')
            except:
                await ctx.channel.send('ID não encontrado!')

    @commands.command(name='combat', aliases=['battle'])
    async def combat(self, ctx):

        global monster, ataque_mob, resposta, chance_acerto

        if ctx.guild is not None:
            if ctx.guild.id == _auth['default_guild'] and ctx.channel.id in resources.rpg_list.PROVINCIAS:
                record = self.bot.db.get_data("user_id", ctx.author.id, "users")
                if record is not None and ctx.author.id == record["user_id"]:
                    async with ClientSession() as session:
                        async with session.get(resources.rpg_list.API_USER.format(ctx.author.id)) as resp:
                            data = await resp.read()
                            Data = loads(data)

                    # DADOS GERAIS
                    CANAL = self.bot.get_channel(431139654973128704)
                    cor = 0x4ff30a
                    tratamento = 0
                    ataques = 0

                    # ------------------------- START MONSTER ------------------------- #

                    # DEFININDO A RADIDADE DO MOB
                    mob = randint(0, 5)

                    # SELECIONANDO O MONSTRO
                    if ctx.channel.id == resources.rpg_list.PROVINCIAS[0]:
                        monster = resources.rpg_list.monster_1[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_1[mob]
                        resposta = resources.rpg_list.respostas_1
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[1]:
                        monster = resources.rpg_list.monster_2[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_2[mob]
                        resposta = resources.rpg_list.respostas_2
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[2]:
                        monster = resources.rpg_list.monster_3[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_3[mob]
                        resposta = resources.rpg_list.respostas_3
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[3]:
                        monster = resources.rpg_list.monster_4[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_4[mob]
                        resposta = resources.rpg_list.respostas_4
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[4]:
                        monster = resources.rpg_list.monster_5[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_5[mob]
                        resposta = resources.rpg_list.respostas_5
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[5]:
                        monster = resources.rpg_list.monster_6[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_6[mob]
                        resposta = resources.rpg_list.respostas_6
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[6]:
                        monster = resources.rpg_list.monster_7[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_7[mob]
                        resposta = resources.rpg_list.respostas_7
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[7]:
                        monster = resources.rpg_list.monster_8[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_8[mob]
                        resposta = resources.rpg_list.respostas_8
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[8]:
                        monster = resources.rpg_list.monster_9[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_9[mob]
                        resposta = resources.rpg_list.respostas_9
                    elif ctx.channel.id == resources.rpg_list.PROVINCIAS[9]:
                        monster = resources.rpg_list.monster_10[mob]
                        ataque_mob = resources.rpg_list.ataque_mob_10[mob]
                        resposta = resources.rpg_list.respostas_10

                    # STATUS MONSTER
                    img_monster = monster[0]
                    nome_do_mob = monster[1]
                    life_monster = monster[2]
                    item_monster = monster[3]
                    quantidade_item_mobs = 1
                    accuracy_monster = monster[4]
                    evasion_mob = monster[5]
                    força_monster = monster[6]
                    gold = monster[7]
                    recompença = monster[8]
                    bonus = monster[9]
                    defense_monster = monster[10]
                    critical_monster = monster[11]
                    level_monster = 'level atual: ' + str(monster[12])
                    defesa_critica_monster = monster[13]
                    loot_monster = monster[14]
                    hability_monster = monster[15]
                    azar_loot = monster[16]
                    experience = monster[17]
                    lucky_monster = monster[18]

                    # MONSTER CHAMPION
                    chance_champion = randint(1, 100)
                    if chance_champion >= 90:
                        champion = True
                    else:
                        champion = False
                    if champion:
                        # STATUS MONSTER CHAMPION
                        cor = 0x0a0a0a
                        nome_do_mob = 'CHAMPION - ' + monster[1]
                        life_monster = monster[2] + 1500
                        quantidade_item_mobs = 3
                        accuracy_monster = monster[4] + 15
                        evasion_mob = monster[5] + 10
                        força_monster = monster[6] + 30
                        gold = monster[7] + 6000
                        recompença = monster[8] + 6
                        bonus = True
                        defense_monster = monster[10] + 30
                        critical_monster = monster[11] + 15
                        level_monster = 'level atual: ' + str(monster[12] + 10)
                        defesa_critica_monster = monster[13] + 15
                        loot_monster = monster[14].append('Acquittal_Crystal')
                        azar_loot = monster[16] + 15
                        experience = monster[17] * 3
                        lucky_monster = monster[18] * 2

                    # BAD EFFECTS MONSTER
                    stun_monster = 0
                    poison_monster = 0

                    # ------------------------- START PLAYER ------------------------- #

                    # STATUS PLAYER
                    level_jogador = 'level atual: ' + str(record['level'])
                    vida_total_jogador = 1000 + (50 * record['level'])
                    força_jogador = 20 
                    defense_jogador = 20
                    accuracy_jogador = 15
                    evasion_jogador = 15
                    critical_jogador = 5.0
                    defesa_critica_jogador = 10.0
                    lucky = 12

                    # BAD EFFECTS
                    poison_jogador = 0
                    stun_jogador = 0

                    # TRATAMENTO
                    if ctx.author.id == 300592580381376513:
                        força_jogador += 100
                        tratamento = 2
                    elif 'Gloria_do_General' in Data['items']:
                        força_jogador += 40
                        tratamento = 3
                    elif 'Valor_do_Capitão' in Data['items']:
                        força_jogador += 30
                        tratamento = 1
                    elif 'Honra_do_Tenente' in Data['items']:
                        força_jogador += 20
                        tratamento = 4

                    # CHECK ARMOR
                    if 'Armadura_de_Ouro' in Data['items']:
                        ataques = 1
                        evasion_jogador += 5
                        accuracy_jogador += 5
                        vida_total_jogador += 500
                        defense_jogador += 25
                        defesa_critica_jogador += 5.0
                        Recovery = 0

                    # CHECK SWORD
                    if 'Zanpakutou' in Data['items']:
                        ataques = 2
                        força_jogador += 100
                        critical_jogador += 5.0
                        Ultimate = 0

                    # CHECK SET
                    if 'Zanpakutou' in Data['items'] and 'Armadura_de_Ouro' in Data['items']:
                        ataques = 3
                        força_jogador += 10
                        vida_total_jogador += 200
                        defense_jogador += 20
                        critical_jogador += 5.0
                        defesa_critica_jogador += 5.0

                    # ADD LIFE PLAYER
                    vida_jogador = vida_total_jogador
                    mob_vida = life_monster

                    if record['batalhando'] == 0:
                        if '{}'.format(item_monster) in Data['items']:		
                            await ctx.channel.send('rp!takeitem {} {} {}'.format(item_monster, quantidade_item_mobs, ctx.author.mention))
                            await ctx.channel.send('''```Markdown
#{}```'''.format(resposta[tratamento][0]))

                            await self.bot.data.add_battle(ctx)

                            embed = discord.Embed(
                                title='{}, O Monstro escolhido foi: {}'.format(ctx.author, nome_do_mob),
                                color=cor,
                                description='Ele tem level {} e tem {} de vida.'.format(
                                    level_monster, mob_vida)
                            )
                            embed.set_image(url=img_monster)
                            await ctx.channel.send(embed=embed)

                            while vida_jogador > 0 and mob_vida > 0:
                                if stun_jogador <= 0:
                                    efeito = ''

                                    # SISTEMA DE ULTIMATE DA ZANPAKUTOU
                                    if 'Zanpakutou' in Data['items']:
                                        chance_ultimate = randint(1, 100)
                                        if chance_ultimate >= 95:
                                            Ultimate += 1
                                            await ctx.channel.send('**{} SUA ZANPAKUTOU FOI ENERGIZADA COM UM ULTIMATE**'.format(ctx.author.mention))

                                    # SISTEMA DE ULTIMATE DA ARMADURA
                                    if 'Armadura_de_Ouro' in Data['items']:
                                        chance_ultimate = randint(1, 100)
                                        if chance_ultimate >= 90:
                                            Recovery += 1
                                            await ctx.channel.send('**{} SUA ARMADURA FOI ABENÇOADA COM UM RECOVERY**'.format(ctx.author.mention))

                                    # SISTEMA DE CRITICAL DO JOGADOR
                                    critico = False
                                    diferença = int(((defesa_critica_monster + defense_monster) - (critical_jogador + lucky + int(força_jogador / 5) + accuracy_jogador)))
                                    if diferença < 1:
                                        diferença = 2
                                    chance_de_critical = randint(1, diferença)
                                    if chance_de_critical >= 30:
                                        critico = True

                                    await ctx.channel.send('''```Markdown
#SUA VEZ, HUMANO!```''')
                                    if ataques == 0:
                                        jogador_ataque = discord.Embed(
                                            title='Escolha seu ataque:',
                                            color=cor,
                                            description='**1**:{}\n**2**:{}\n**3**:{}\n**4**:{}\n**5**:{}'.format(
                                                resources.rpg_list.ataque_jogador[ataques][0],
                                                resources.rpg_list.ataque_jogador[ataques][1],
                                                resources.rpg_list.ataque_jogador[ataques][2],
                                                resources.rpg_list.ataque_jogador[ataques][3],
                                                resources.rpg_list.ataque_jogador[ataques][4]))
                                        await ctx.channel.send(embed=jogador_ataque)
                                    elif ataques == 1:
                                        jogador_ataque = discord.Embed(
                                            title='Escolha seu ataque:',
                                            color=cor,
                                            description='**1**:{}\n**2**:{}\n**3**:{}\n**4**:{}\n**5**:{}\n**6**:{}'.format(
                                                resources.rpg_list.ataque_jogador[ataques][0],
                                                resources.rpg_list.ataque_jogador[ataques][1],
                                                resources.rpg_list.ataque_jogador[ataques][2],
                                                resources.rpg_list.ataque_jogador[ataques][3],
                                                resources.rpg_list.ataque_jogador[ataques][4],
                                                resources.rpg_list.ataque_jogador[ataques][5]))
                                        await ctx.channel.send(embed=jogador_ataque)
                                    elif ataques == 2:
                                        jogador_ataque = discord.Embed(
                                            title='Escolha seu ataque:',
                                            color=cor,
                                            description='**1**:{}\n**2**:{}\n**3**:{}\n**4**:{}\n**5**:{}\n**6**:{}'.format(
                                                resources.rpg_list.ataque_jogador[ataques][0],
                                                resources.rpg_list.ataque_jogador[ataques][1],
                                                resources.rpg_list.ataque_jogador[ataques][2],
                                                resources.rpg_list.ataque_jogador[ataques][3],
                                                resources.rpg_list.ataque_jogador[ataques][4],
                                                resources.rpg_list.ataque_jogador[ataques][5]))
                                        await ctx.channel.send(embed=jogador_ataque)
                                    else:
                                        jogador_ataque = discord.Embed(
                                            title='Escolha seu ataque:',
                                            color=cor,
                                            description='**1**:{}\n**2**:{}\n**3**:{}\n**4**:{}\n**5**:{}\n**6**:{}\n**7**:{}'.format(
                                                resources.rpg_list.ataque_jogador[ataques][0],
                                                resources.rpg_list.ataque_jogador[ataques][1],
                                                resources.rpg_list.ataque_jogador[ataques][2],
                                                resources.rpg_list.ataque_jogador[ataques][3],
                                                resources.rpg_list.ataque_jogador[ataques][4],
                                                resources.rpg_list.ataque_jogador[ataques][5],
                                                resources.rpg_list.ataque_jogador[ataques][6]))
                                        await ctx.channel.send(embed=jogador_ataque)

                                    def check(m):
                                        return m.author == ctx.author and m.content.isdigit()

                                    playat = await self.bot.wait_for('message', check=check)

                                    if ataques == 0:
                                        check_ataque = playat.content in ['1', '2', '3', '4', '5']
                                    elif ataques == 1:
                                        check_ataque = playat.content in ['1', '2', '3', '4', '5', '6']
                                    elif ataques == 2:
                                        check_ataque = playat.content in ['1', '2', '3', '4', '5', '6']
                                    else:
                                        check_ataque = playat.content in ['1', '2', '3', '4', '5', '6', '7']

                                    if check_ataque is False:
                                        while check_ataque is False:
                                            await ctx.channel.send('Essa não é uma opção valida tente denovo')

                                            playat = await self.bot.wait_for('message', check=check)

                                            if ataques == 0:
                                                check_ataque = playat.content in ['1', '2', '3', '4', '5']
                                            elif ataques == 1:
                                                check_ataque = playat.content in ['1', '2', '3', '4', '5', '6']
                                            elif ataques == 2:
                                                check_ataque = playat.content in ['1', '2', '3', '4', '5', '6']
                                            else:
                                                check_ataque = playat.content in ['1', '2', '3', '4', '5', '6', '7']
                                        playat = playat.content
                                    else:
                                        playat = playat.content
                                    playat = int(playat)
                                    nome_atk_jogador = playat - 1


                                    # CHANCE DE ACERTO DO JOGADOR
                                    accuracy_batalha_player = randint(accuracy_jogador, (accuracy_jogador * 2))
                                    evasion_monster = randint(int(evasion_mob / 2), evasion_mob)
                                    if stun_monster > 0:
                                        evasion_monster = 0

                                    if playat != 6:
                                        if accuracy_batalha_player > evasion_monster:
                                            if playat == 1:  # ATAQUE VARIANTE
                                                atk = randint(int(força_jogador/2), (força_jogador * 2))
                                                embed = discord.Embed(
                                                    title='{} usou {}.'.format(ctx.author,
                                                                               resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                    color=resources.rpg_list.corlista[1],
                                                    description='Você causou **{}** de dano.'.format(atk)
                                                )
                                                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                if critico is True:
                                                    atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(ctx.author,
                                                                                   resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[2],
                                                        description='Você causou **{}** de dano.'.format(atk)
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                await ctx.channel.send(embed=embed)
                                                mob_vida -= int(atk)
                                            if playat == 2:  # ATAQUE FIXO
                                                atk = 90 + força_jogador
                                                embed = discord.Embed(
                                                    title='{} usou {}.'.format(ctx.author,
                                                                               resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                    color=resources.rpg_list.corlista[1],
                                                    description='Você causou **{}** de dano.'.format(atk)
                                                )
                                                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                if critico is True:
                                                    atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(ctx.author,
                                                                                   resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[2],
                                                        description='Você causou **{}** de dano critico.'.format(atk)
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                await ctx.channel.send(embed=embed)
                                                mob_vida -= int(atk)
                                            if playat == 3:  # STUN
                                                if stun_monster <= 0:
                                                    chance_acerto = randint(1, lucky)
                                                    if 9 < chance_acerto < 13:
                                                        stun_monster = 1
                                                        efeito = str('e estunou por o/a {} **1** turno'.format(
                                                            nome_do_mob))
                                                    elif 12 < chance_acerto < 19:
                                                        stun_monster = 2
                                                        efeito = str('e estunou o/a {} por **2** turnos'.format(
                                                            nome_do_mob))
                                                    elif chance_acerto >= 19:
                                                        stun_monster = 3
                                                        efeito = ('e estunou o/a {} por **3** turnos'.format(
                                                            nome_do_mob))
                                                    chance_acerto = 0
                                                atk = randint(20, (20 + força_jogador))
                                                embed = discord.Embed(
                                                    title='{} usou {}.'.format(ctx.author,
                                                                               resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                    color=resources.rpg_list.corlista[1],
                                                    description='Você causou **{}** de dano {}'.format(atk, efeito)
                                                )
                                                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                if critico is True:
                                                    atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(ctx.author,
                                                                                   resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[2],
                                                        description='Você causou **{}** de dano critico {}'.format(atk, efeito)
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                await ctx.channel.send(embed=embed)
                                                mob_vida -= int(atk)
                                            if playat == 4:  # POISON
                                                if poison_monster <= 0:
                                                    chance_acerto = randint(1, lucky)
                                                    if 9 < chance_acerto < 13:
                                                        poison_monster = 1
                                                        efeito = str('e envenenou por o/a {} **1** turno'.format(
                                                            nome_do_mob))
                                                    elif 12 < chance_acerto < 20:
                                                        poison_monster = 2
                                                        efeito = str('e envenenou o/a {} por **2** turnos'.format(
                                                            nome_do_mob))
                                                    elif chance_acerto >= 20:
                                                        poison_monster = 3
                                                        efeito = ('e envenenou o/a {} por **3** turnos'.format(
                                                            nome_do_mob))
                                                    chance_acerto = 0
                                                atk = randint(25, (25 + força_jogador))
                                                embed = discord.Embed(
                                                    title='{} usou {}.'.format(ctx.author,
                                                                               resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                    color=resources.rpg_list.corlista[1],
                                                    description='Você causou **{}** de dano {}'.format(atk, efeito)
                                                )
                                                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                if critico is True:
                                                    atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(ctx.author,
                                                                                   resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[2],
                                                        description='Você causou **{}** de dano critico {}'.format(atk, efeito)
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                await ctx.channel.send(embed=embed)
                                                mob_vida -= int(atk)
                                            if playat == 5:  # ENERGIA CONCENTRADA
                                                atk = (randint(55, 95) + força_jogador) * randint(2, 5)
                                                if 150 < atk < 250:
                                                    stun_jogador = 1
                                                    efeito = str('e você foi estunado por **1** turno')
                                                elif 250 < atk < 350:
                                                    stun_jogador = 2
                                                    efeito = str('e você foi estunado por **2** turnos')
                                                elif 350 < atk < 450:
                                                    stun_jogador = 3
                                                    efeito = str('e você foi estunado por **3** turnos')
                                                elif 450 < atk < 850:
                                                    stun_jogador = 4
                                                    efeito = str('e você foi estunado por **4** turnos')
                                                elif 850 < atk < 1250:
                                                    stun_jogador = 5
                                                    efeito = str('e você foi estunado por **5** turnos')
                                                elif 1250 < atk < 1550:
                                                    stun_jogador = 6
                                                    efeito = str('e você foi estunado por **6** turnos')
                                                elif atk > 1550:
                                                    stun_jogador = 7
                                                    efeito = str('e você foi estunado por **7** turnos')
                                                embed = discord.Embed(
                                                    title='{} usou {}.'.format(ctx.author,
                                                                               resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                    color=resources.rpg_list.corlista[1],
                                                    description='Você causou **{}** de dano {}'.format(atk, efeito)
                                                )
                                                if critico is True:
                                                    atk += int(atk / 100 * 20)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(ctx.author,
                                                                                   resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[2],
                                                        description='Você causou **{}** de dano critico {}'.format(atk, efeito)
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                await ctx.channel.send(embed=embed)
                                                mob_vida -= int(atk)
                                            if playat == 7:  # EXTREME POWER
                                                if Ultimate >= 1:
                                                    atk = ((randint(55, 135) + força_jogador) * randint(3, 6))
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(ctx.author,
                                                                                   resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[1],
                                                        description='Você causou **{}** de dano!'.format(atk)
                                                    )
                                                    if critico is True:
                                                        atk += int(atk / 100 * 20)
                                                        embed = discord.Embed(
                                                            title='{} usou {}.'.format(ctx.author,
                                                                                       resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                            color=resources.rpg_list.corlista[2],
                                                            description='Você causou **{}** de dano critico!'.format(atk)
                                                        )
                                                        embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                        embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                    await ctx.channel.send(embed=embed)
                                                    Ultimate -= 1
                                                    mob_vida -= int(atk)
                                                else:
                                                    atk = (50 + força_jogador)
                                                    embed = discord.Embed(
                                                        title='{} não usou {}.'.format(ctx.author,
                                                                                       resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[1],
                                                        description='Pois nao tem o item necessário, mas você causou **{}** de dano.'.format(atk)
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                    if critico is True:
                                                        atk += int(atk / 100 * 40)
                                                        embed = discord.Embed(
                                                            title='{} não usou {}.'.format(ctx.author,
                                                                                           resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                            color=resources.rpg_list.corlista[2],
                                                            description='Pois nao tem o item necessário, mas você causou **{}** de dano critico.'.format(atk)
                                                        )
                                                        embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                        embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                    await ctx.channel.send(embed=embed)
                                                    mob_vida -= int(atk)
                                            if mob_vida < 0:
                                                mob_vida = 0
                                            if mob_vida < (life_monster * 30 / 100):
                                                vida = resources.rpg_list.cor_vida[0]
                                            elif mob_vida < (life_monster * 70 / 100):
                                                vida = resources.rpg_list.cor_vida[1]
                                            else:
                                                vida = resources.rpg_list.cor_vida[2]
                                            embed = discord.Embed(
                                                title='Vida do/a {}'.format(nome_do_mob),
                                                color=vida,
                                                description='{} ficou com {} de vida.'.format(
                                                    nome_do_mob, mob_vida)
                                            )
                                            embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                            embed.set_thumbnail(url=img_monster)
                                            await ctx.channel.send(embed=embed)
                                            if critico is False:
                                                await ctx.channel.send('''```Markdown
#{}```'''.format(resposta[tratamento][1]))
                                            else:
                                                await ctx.channel.send('''```Markdown
#{}```'''.format(resposta[tratamento][2]))
                                        else:
                                            embed = discord.Embed(
                                                title='{} errou o ataque.'.format(ctx.author),
                                                color=resources.rpg_list.corlista[10]
                                            )
                                            embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                            embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                            await ctx.channel.send(embed=embed)
                                    else:
                                        if playat == 6:  # RECUPERAÇÃO
                                            if Recovery >= 1:
                                                vida_cheia = False
                                                recuperação = randint(45, 200) + força_jogador
                                                if vida_jogador + recuperação > vida_total_jogador:
                                                    vida_jogador = vida_total_jogador
                                                    vida_cheia = True
                                                if critico is True:
                                                    recuperação += (recuperação / 100 * 20)
                                                    if vida_jogador + recuperação > vida_total_jogador:
                                                        vida_jogador = vida_total_jogador
                                                        vida_cheia = True
                                                if not vida_cheia:
                                                    embed = discord.Embed(
                                                        title='{} usou {}'.format(ctx.author,
                                                                                  resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[9],
                                                        description='Você recuperou **{}** pontos de vida.'.format(
                                                            recuperação)
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador),
                                                                    inline=False)
                                                    await ctx.channel.send(embed=embed)
                                                    vida_jogador += int(recuperação)
                                                else:
                                                    embed = discord.Embed(
                                                        title='{} usou {}'.format(ctx.author,
                                                                                  resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[9],
                                                        description='Você recuperou sua vida maxima!'
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador),
                                                                    inline=False)
                                                    await ctx.channel.send(embed=embed)
                                                Recovery -= 1
                                            else:
                                                atk = (50 + força_jogador)
                                                embed = discord.Embed(
                                                    title='{} não usou {}.'.format(ctx.author,
                                                                                   resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                    color=resources.rpg_list.corlista[1],
                                                    description='Pois nao tem o item necessário, mas você causou **{}** de dano.'.format(
                                                        atk)
                                                )
                                                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                if critico is True:
                                                    atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} não usou {}.'.format(ctx.author,
                                                                                       resources.rpg_list.ataque_jogador[ataques][nome_atk_jogador]),
                                                        color=resources.rpg_list.corlista[2],
                                                        description='Pois nao tem o item necessário, mas você causou **{}** de dano critico.'.format(
                                                            atk)
                                                    )
                                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                    embed.add_field(name='LEVEL:', value=str(level_jogador),
                                                                    inline=False)
                                                await ctx.channel.send(embed=embed)
                                                mob_vida -= int(atk)
                                else:
                                    embed = discord.Embed(
                                        title='{} esta estunado.'.format(ctx.author),
                                        color=resources.rpg_list.corlista[3],
                                        description='Isso vai durar mais **{}** turnos'.format(stun_jogador)
                                    )
                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                    embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                    await ctx.channel.send(embed=embed)
                                    stun_jogador -= 1
                                if poison_jogador > 0:
                                    poison = randint(int(força_monster / 3), (força_monster * randint(1, 2)))
                                    vida_jogador -= poison
                                    embed = discord.Embed(
                                        title='{} esta envenenado.'.format(ctx.author),
                                        color=resources.rpg_list.corlista[4],
                                        description='Você tomou {} de dano de veneno e ficou com **{}** de vida.'.format(poison, vida_jogador)
                                    )
                                    embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                    embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                    await ctx.channel.send(embed=embed)
                                    poison_jogador -= 1
                                #  ------------------  AQUI INICIA O TURNO DO MONSTRO  ------------------
                                if mob_vida > 0:
                                    if stun_monster <= 0:
                                        efeito = ''

                                        # SISTEMA DE CRITICAL DO MONSTER
                                        critico = False
                                        diferença = int(((defesa_critica_jogador + defense_jogador) - (critical_monster + int(força_monster / 3) + accuracy_monster)))
                                        if diferença < 1:
                                            diferença = 2
                                        chance_de_critical = randint(1, diferença)
                                        # await ctx.channel.send('monster, chance de **critical**: ``{}``'.format(chance_de_critical))
                                        if chance_de_critical >= 30:
                                            critico = True

                                        await ctx.channel.send('''```Markdown
#PREPARE-SE PARA MORRER!```''')
                                        playat = randint(1, 6)
                                        if mob_vida == life_monster:
                                            playat = randint(1, 5)
                                        nome_atk_mob = playat - 1

                                        # CHANCE DE ACERTO DO MONSTRO
                                        accuracy_battle_monster = randint(accuracy_monster, (accuracy_monster * 2))
                                        evasion_player = randint(int(evasion_jogador / 2), evasion_jogador)
                                        if stun_jogador > 0:
                                            evasion_player = 0

                                        if playat != 6:
                                            if accuracy_battle_monster > evasion_player:
                                                if playat == 1:  # Magia Negra
                                                    atk = (50 + força_monster)
                                                    if critico is True:
                                                        atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(nome_do_mob,
                                                                                   ataque_mob[nome_atk_mob]),
                                                        color=resources.rpg_list.corlista[0],
                                                        description='{} causou **{}** de dano.'.format(
                                                            nome_do_mob, atk))
                                                    embed.set_thumbnail(url=img_monster)
                                                    embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                                    await ctx.channel.send(embed=embed)
                                                    vida_jogador -= int(atk)
                                                if playat == 2:  # Perfurada com Stun
                                                    if stun_jogador <= 0:
                                                        chance_acerto = randint(1, (int(lucky_monster / 2) + 5))
                                                        if 9 < chance_acerto < 18:
                                                            stun_jogador = 1
                                                            efeito = str('e te estunou por **1** turno')
                                                        elif chance_acerto > 18:
                                                            stun_jogador = 2
                                                            efeito = str('e te estunou por **2** turnos')
                                                    chance_acerto = 0
                                                    atk = (randint(10, 30) + força_monster)
                                                    if critico is True:
                                                        atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(nome_do_mob,
                                                                                   ataque_mob[nome_atk_mob]),
                                                        color=resources.rpg_list.corlista[0],
                                                        description='{} causou **{}** de dano {}'.format(
                                                            nome_do_mob, atk, efeito)
                                                    )
                                                    embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                                    embed.set_thumbnail(url=img_monster)
                                                    await ctx.channel.send(embed=embed)
                                                    vida_jogador -= int(atk)
                                                if playat == 3:  # Poison
                                                    if poison_jogador <= 0:
                                                        chance_acerto = randint(1, (int(lucky_monster / 2) + 5))
                                                        if 9 < chance_acerto < 13:
                                                            poison_jogador = 1
                                                            efeito = str('e te envenenou por **1** turnos')
                                                        elif chance_acerto < 17:
                                                            poison_jogador = 2
                                                            efeito = str('e te envenenou por **2** turnos')
                                                        elif chance_acerto < 20:
                                                            poison_jogador = 3
                                                            efeito = str('e te envenenou por **3** turnos')
                                                        elif chance_acerto >= 20:
                                                            poison_jogador = 4
                                                            efeito = str('e te envenenou por **4** turnos')
                                                    chance_acerto = 0
                                                    atk = (randint(10, 30) + força_monster)
                                                    if critico is True:
                                                        atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(nome_do_mob,
                                                                                   ataque_mob[nome_atk_mob]),
                                                        color=resources.rpg_list.corlista[0],
                                                        description='{} causou **{}** de dano {}'.format(
                                                            nome_do_mob, atk, efeito)
                                                    )
                                                    embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                                    embed.set_thumbnail(url=img_monster)
                                                    await ctx.channel.send(embed=embed)
                                                    vida_jogador -= int(atk)
                                                if playat == 4:  # Dano Massivo
                                                    atk = (randint(25, 45) + força_monster)
                                                    if critico is True:
                                                        atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(nome_do_mob,
                                                                                   ataque_mob[nome_atk_mob]),
                                                        color=resources.rpg_list.corlista[0],
                                                        description='{} causou **{}** de dano.'.format
                                                        (nome_do_mob, atk)
                                                    )
                                                    embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                                    embed.set_thumbnail(url=img_monster)
                                                    await ctx.channel.send(embed=embed)
                                                    vida_jogador -= int(atk)
                                                if playat == 5:  # Explosão Estelar
                                                    atk = (randint(55, 115) + força_monster)
                                                    if critico is True:
                                                        atk += int(atk / 100 * 40)
                                                    embed = discord.Embed(
                                                        title='{} usou {}.'.format(nome_do_mob,
                                                                                   ataque_mob[nome_atk_mob]),
                                                        color=resources.rpg_list.corlista[0],
                                                        description='{} causou **{}** de dano {}'.format(
                                                            nome_do_mob, atk, efeito)
                                                    )
                                                    embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                                    embed.set_thumbnail(url=img_monster)
                                                    await ctx.channel.send(embed=embed)
                                                    vida_jogador -= int(atk)
                                                if vida_jogador < 0:
                                                    vida_jogador = 0
                                                if vida_jogador < (vida_total_jogador * 30 / 100):
                                                    vida = resources.rpg_list.cor_vida[0]
                                                elif vida_jogador < (vida_total_jogador * 70 / 100):
                                                    vida = resources.rpg_list.cor_vida[1]
                                                else:
                                                    vida = resources.rpg_list.cor_vida[2]
                                                embed = discord.Embed(
                                                    title='Vida do {}'.format(ctx.author),
                                                    color=vida,
                                                    description='Você ficou com {} de vida.'.format(vida_jogador)
                                                )
                                                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                                                embed.add_field(name='LEVEL:', value=str(level_jogador), inline=False)
                                                await ctx.channel.send(embed=embed)
                                                await ctx.channel.send('''```Markdown
#{}```'''.format(resposta[tratamento][3]))
                                            else:
                                                embed = discord.Embed(
                                                    title='{} errou o golpe.'.format(nome_do_mob),
                                                    color=resources.rpg_list.corlista[5]
                                                )
                                                embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                                embed.set_thumbnail(url=img_monster)
                                                await ctx.channel.send(embed=embed)
                                        if playat == 6:
                                            vida_cheia = False
                                            recuperação = randint(45, 135) + força_monster
                                            if mob_vida + recuperação > life_monster:
                                                mob_vida = life_monster
                                                vida_cheia = True
                                            if critico is True:
                                                recuperação += int(recuperação / 100 * 40)
                                                if mob_vida + recuperação > life_monster:
                                                    mob_vida = life_monster
                                                    vida_cheia = True
                                            if not vida_cheia:
                                                embed = discord.Embed(
                                                    title='{} usou {}'.format(nome_do_mob, ataque_mob[nome_atk_mob]),
                                                    color=resources.rpg_list.corlista[9],
                                                    description='{} recuperou **{}** pontos de vida.'.format(
                                                        nome_do_mob, recuperação)
                                                )
                                                embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                                embed.set_thumbnail(url=img_monster)
                                                await ctx.channel.send(embed=embed)
                                                mob_vida += int(recuperação)
                                            else:
                                                embed = discord.Embed(
                                                    title='{} usou {}'.format(nome_do_mob, ataque_mob[nome_atk_mob]),
                                                    color=resources.rpg_list.corlista[9],
                                                    description='{} **RECUPEROU TODOS OS SEUS PONTOS DE VIDA.**'.format(
                                                        nome_do_mob)
                                                )
                                                embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                                embed.set_thumbnail(url=img_monster)
                                                await ctx.channel.send(embed=embed)
                                    else:
                                        embed = discord.Embed(
                                            title='{} esta estunado(a).'.format(nome_do_mob),
                                            color=resources.rpg_list.corlista[6],
                                            description='E ficará assim por mais **{}** turnos.'.format(stun_monster)
                                        )
                                        embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                        embed.set_thumbnail(url=img_monster)
                                        await ctx.channel.send(embed=embed)
                                        stun_monster -= 1
                                    if poison_monster > 0:
                                        poison = randint(int(força_jogador / 3), (força_jogador * randint(1, 2)))
                                        mob_vida -= poison
                                        embed = discord.Embed(
                                            title='{} esta envenanado(a).'.format(nome_do_mob),
                                            color=resources.rpg_list.corlista[6],
                                            description='{} recebeu **{}** de dano por envenenamento e ficou com {} de vida'.format(
                                                nome_do_mob, poison, mob_vida),
                                        )
                                        embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                                        poison_monster -= 1
                                        embed.set_thumbnail(url=img_monster)
                                        await ctx.channel.send(embed=embed)
                            if mob_vida <= 0:
                                if vida_jogador < 0:
                                    vida_jogador = 0
                                embed = discord.Embed(
                                    title='Enfim, você venceu! **{}**'.format(ctx.author),
                                    color=resources.rpg_list.corlista[8],
                                    description='Não fique tão feliz, na proxima vez que nos encontrar-mos não vai ser desta forma!'
                                )
                                embed.set_image(url=img_monster)
                                await ctx.channel.send(embed=embed)
                                lvl_moster = monster[12]
                                if champion:
                                    lvl_moster = monster[12] + 10
                                lvl_bonus = record['level'] - lvl_moster
                                if lvl_bonus < 8:
                                    await CANAL.send('rp!givemoney {} {}'.format(vida_jogador, ctx.author.mention))
                                    await CANAL.send('```VOCE GANHOU {} GOLDS DO QUE RESTOU DO SEU LP!```'.format(vida_jogador))
                                    XP = experience + (record['level'] * randint(1, 5))
                                    await self.bot.data.add_experience(ctx.author, XP)
                                    await ctx.channel.send('{}, acaba de ganhar **{}** de experiencia!'.format(ctx.author.mention, XP))
                                    await self.bot.data.level_up(ctx.author, ctx.channel)
                                    if champion:
                                        if 'Armadura_de_Ouro' in Data['items']:
                                            chance = randint(1, 100)
                                            if chance >= 80:
                                                if 'Discharge_Crystal' in Data['items']:
                                                    await ctx.channel.send('rp!takeitem {} 1 {}'.format('Discharge_Crystal',
                                                                                                        ctx.author.mention))
                                                    await ctx.channel.send('rp!giveitem {} 1 {}'.format('Crystal_of_Death',
                                                                                                        ctx.author.mention))
                                            else:
                                                if 'Discharge_Crystal' in Data['items']:
                                                    await ctx.channel.send('rp!takeitem {} 1 {}'.format('Discharge_Crystal',
                                                                                                        ctx.author.mention))
                                    if bonus:
                                        await CANAL.send(P.format(recompença, ctx.author.mention))
                                        await CANAL.send('O membro {} ganhou **{}** COINS DE BOOSTER batalhando contra o/a '
                                                         '{} as {}h e {}min em {}/{}/{}'.format(ctx.author, recompença,
                                                                                                nome_do_mob,
                                                                                                hora[3], hora[4], hora[2], hora[1],
                                                                                                hora[0]))
                                        if hora[4] in (15, 16, 17, 18, 19, 20) or hora[4] in (45, 46, 47, 48, 49, 50):
                                            await CANAL.send("rp!givemoney {} {}".format(gold, ctx.author.mention))
                                            await CANAL.send(
                                                f'O membro {ctx.author} ganhou {gold} golds **EXTRA** batalhando contra o/a '
                                                f'{nome_do_mob} as {hora[3]}h e {hora[4]}min em '
                                                f'{hora[2]}/{hora[1]}/{hora[0]} por ganhar na hora exata')
                                            await ctx.channel.send("{} Parabens, Você acaba de ganhar **{}** Golds!".format(
                                                ctx.author.mention, gold))
                                    azar_loot -= lucky
                                    if azar_loot < 2:
                                        azar_loot = 2
                                    chance = randint(1, azar_loot)
                                    if chance < 6:
                                        for p in range(0, len(loot_monster)):
                                            quantidade_loot = randint(1, 3)
                                            await CANAL.send('rp!giveitem {} {} {}'.format(loot_monster[p], quantidade_loot, ctx.author.mention))
                                    await self.bot.data.remove_battle(ctx)
                                else:
                                    await ctx.channel.send('```VOCE PRECISA ENFRENTAR UM MONSTRO MAIS FORTE PRA GANHAR ALGO!```')
                                    await self.bot.data.remove_battle(ctx)
                            else:
                                embed = discord.Embed(
                                    title='TENTE UMA PROXIMA VEZ {}!'.format(ctx.author),
                                    color=resources.rpg_list.corlista[7]
                                )
                                embed.set_image(url=img_monster)
                                await ctx.channel.send(embed=embed)
                                await ctx.channel.send('rp!takeitem {} {} {}'.format(item_monster, quantidade_item_mobs, ctx.author.mention))
                                await ctx.channel.send('''```Markdown
#Entregue o que é meu por direito mortal...```''')
                                await self.bot.data.remove_battle(ctx)
                        else:
                            embed = discord.Embed(
                                title='{} não demonstrou interesse em {}'.format(nome_do_mob, ctx.author),
                                color=resources.rpg_list.corlista[6],
                                description='{} sumiu...\n'
                                            'Por que você nao tem {} no seu inventário!'.format(
                                    nome_do_mob, item_monster)
                            )
                            embed.add_field(name='LEVEL:', value=str(level_monster), inline=False)
                            embed.set_image(url=img_monster)
                            await ctx.channel.send(embed=embed)
                    else:
                        await ctx.channel.send('```VOCE JA ESTA BATALHANDO EM: {}```'.format(record['provincia']))
                else:
                    await ctx.channel.send('```VOCE PRECISA ESTA REGISTRADO PARA PODER BATALHAR, USE: .register```')


def setup(bot):
    bot.add_cog(BattleRpg(bot))
    print('\033[1;32mO comando \033[1;34mBATTLE\033[1;32m foi carregado com sucesso!\33[m')
