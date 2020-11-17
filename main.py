# ARQUIVO PRINCIPAL DE INICIALIZAÇÃO DO BOT: ASHLEY PARA DISCORD.
# CRIADO POR: DANIEL AMARAL -> Denky#5960
# SEGUE ABAIXO OS IMPORTS COMPLETOS
import logging
import discord
import aiohttp
import psutil
import json
import copy
import sys
import os
import traceback
# SEGUE ABAIXO OS IMPORTS PARCIAIS
import time as date
from random import choice, randint
from datetime import datetime as dt
from collections import Counter
from discord.ext import commands
from resources.color import random_color
from resources.webhook import Webhook
from bson.json_util import dumps
from resources.utility import date_format, patent_calculator, guild_info
from resources.db import Database, DataInteraction
from resources.verify_cooldown import verify_cooldown
from resources.boosters import Booster
from config import data as config


# CLASSE PRINCIPAL SENDO SUBCLASSE DA BIBLIOTECA DISCORD
class Ashley(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, shard_count=1, **kwargs)
        self.owner_id = 300592580381376513
        self.start_time = dt.utcnow()
        self.cmd_event = {}
        self.commands_used = Counter()
        self.guilds_commands = Counter()
        self.guilds_messages = Counter()
        self.user_commands = Counter()
        self.blacklist = list()
        self.shutdowns = list()
        self.session = aiohttp.ClientSession()

        self.config = config
        self.em = self.config["emojis"]["msg"]
        self.color = int(config['config']['default_embed'], 16)
        self.announcements = self.config['attribute']['announcements']
        self.all_prefix = self.config['attribute']['all_prefix']
        self.vip_cog = self.config['attribute']['vip_cog']
        self.titling = self.config['attribute']['titling']
        self.boxes_l = self.config['attribute']['boxes_l']
        self.chests_l = self.config['attribute']['chests_l']
        self.boxes = self.config['attribute']['boxes']
        self.chests = self.config['attribute']['chests']
        self.money = self.config['attribute']['money']
        self.items = self.config['items']
        self.icons = self.config['icons']
        self.pets = self.config['pets']
        self.no_panning = self.config['attribute']['no_panning']
        self.testers = self.config['attribute']['testers']
        self.maintenance = False
        self.event_special = False

        self.log_dir = os.path.join('log', 'discord.log')
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename=self.log_dir, encoding='utf-8', mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

        self.server_ = "EXTRAVM.COM"
        self.progress = "V.9 -> 5.0%"
        self.python_version = "3.8.2"
        self.github = "https://github.com/Ashley-Lab/Ashley"
        self.staff = self.config['attribute']['staff']
        self.team = self.config['attribute']['team']
        self.version = "API: " + str(discord.__version__) + " | BOT: 9.0.50 | PROGRESS: " + str(self.progress)
        self.shortcut = self.config['attribute']['shortcut']
        self.block = self.config['attribute']['block']
        self.data_cog = {}
        self.box = {}
        self.chests_users = {}
        self.msg_cont = 0

        self.db: Database = Database(self)
        self.data: DataInteraction = DataInteraction(self)
        self.booster: Booster = Booster(self.items)

    async def atr_initialize(self):
        self.blacklist = dumps(await self.db.get_all_data("blacklist"))
        print('\033[1;32m( 🔶 ) | Inicialização do atributo \033[1;34mBLACKLIST\033[1;32m foi feita sucesso!\33[m')
        self.shutdowns = dumps(await self.db.get_all_data("shutdown"))
        print('\033[1;32m( 🔶 ) | Inicialização do atributo \033[1;34mSHUTDOWN\033[1;32m foi feita sucesso!\33[m')

    async def shutdown(self, reason):
        date_ = dt(*dt.utcnow().timetuple()[:6])
        data = {"_id": date_, "reason": reason}
        await self.db.push_data(data, "shutdown")
        self.shutdowns = dumps(await self.db.get_all_data("shutdown"))

    async def ban_(self, id_, reason: str):
        date_ = dt(*dt.utcnow().timetuple()[:6])
        data = {"_id": id_, str(date_): reason}
        if str(id_) not in self.blacklist:
            await self.db.push_data(data, "blacklist")
            self.blacklist = dumps(await self.db.get_all_data("blacklist"))
            return True
        else:
            return False

    async def un_ban_(self, id_):
        if str(id_) not in self.blacklist:
            return False
        else:
            await self.db.delete_data({"_id": int(id_)}, "blacklist")
            self.blacklist = dumps(await self.db.get_all_data("blacklist"))
            return True

    async def on_command(self, ctx):
        if ctx.guild is not None:
            data_guild = await self.db.get_data("guild_id", ctx.guild.id, "guilds")
            data_user = await self.db.get_data("user_id", ctx.author.id, "users")
            if data_user is not None and data_guild is not None:
                if (self.guilds_commands[ctx.guild.id] % 10) == 0:
                    for data in await self.db.get_announcements():
                        if data['data']['status']:
                            self.announcements.append(data["data"]["announce"])
                    announce = choice(self.announcements)
                    embed = discord.Embed(
                        color=0x000000,
                        description=f'<:confirmed:721581574461587496>│**ANUNCIO**\n '
                                    f'```{announce}```')
                    perms = ctx.channel.permissions_for(ctx.me)
                    if perms.send_messages and perms.read_messages:
                        if perms.embed_links and perms.attach_files:
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` **ADICIONAR "
                                           "LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR CORRETAMENTE!**")

            commands_log = self.get_channel(575688812068339717)
            await commands_log.send(f"``O membro`` {ctx.author.name} ``acabou de usar o comando`` "
                                    f"**{str(ctx.command).upper()}** ``dentro da guilda`` {ctx.guild.name} ``na "
                                    f"data e hora`` **{date_format(dt.now())}**")

    async def on_command_completion(self, ctx):
        if ctx.guild is not None:
            _name = ctx.author.name.upper()
            cmd = str(ctx.command).lower()

            data_guild = await self.db.get_data("guild_id", ctx.guild.id, "guilds")
            update_guild = data_guild

            data_user = await self.db.get_data("user_id", ctx.author.id, "users")
            update_user = data_user

            if update_user is not None and update_guild is not None:
                self.user_commands[ctx.author.id] += 1
                self.commands_used[ctx.command] += 1
                self.guilds_commands[ctx.guild.id] += 1

                if ctx.author.id in self.cmd_event.keys():
                    try:
                        self.cmd_event[ctx.author.id][str(ctx.command).lower()] += 1
                    except KeyError:
                        self.cmd_event[ctx.author.id][str(ctx.command).lower()] = 1
                else:
                    self.cmd_event[ctx.author.id] = {str(ctx.command).lower(): 1}

                if update_user['security']['status']:
                    update_user['user']['commands'] += 1
                if (update_user['user']['commands'] % 10) == 0:
                    guild_ = self.get_guild(update_user['guild_id'])
                    if guild_ is None:
                        perms = ctx.channel.permissions_for(ctx.me)
                        if perms.send_messages and perms.read_messages:
                            await ctx.send(f"<:negate:721581573396496464>│``{_name} SUA GUILDA DE CADASTRO FOI "
                                           f"DELETADA, TENTE USAR O COMANDO`` **ASH TRANS** "
                                           f"``PARA MUDAR SUA GUILDA DE ORIGEM``")

                if (update_user['user']['commands'] % 2) == 0:
                    chance, quant = randint(1, 100), randint(1, 3)
                    if chance <= 50:
                        if update_user['security']['status']:
                            update_user['inventory']['rank_point'] += quant
                            perms = ctx.channel.permissions_for(ctx.me)
                            if perms.send_messages and perms.read_messages:
                                await ctx.send(f"<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``{_name} GANHOU:`` "
                                               f"<:silver:519896828120924170> **{quant}** ``RANKPOINT A MAIS!``")

                if (update_user['user']['commands'] % 10) == 0:
                    chance = randint(1, 100)
                    if chance <= 20:
                        if update_user['security']['status']:
                            update_user['inventory']['medal'] += 1
                            perms = ctx.channel.permissions_for(ctx.me)
                            if perms.send_messages and perms.read_messages:
                                await ctx.send(f"<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``{_name} GANHOU:`` "
                                               f"<:medals:519896836375314442> **1** ``MEDALHA A MAIS!``")

                for key in self.titling.keys():
                    if update_user['user']['commands'] >= int(key):
                        update_user['user']['titling'] = self.titling[key]

                if str(ctx.command).lower() in ['marry', 'divorce']:
                    if update_user['user']['married']:
                        dm = await self.db.get_data("user_id", update_user['user']['married_at'], "users")
                        um = dm
                        um['user']['married'] = True
                        um['user']['married_at'] = ctx.author.id
                        um['user']['marrieding'] = False
                        await self.db.update_data(dm, um, 'users')
                        update_user['user']['married'] = True
                        update_user['user']['married_at'] = update_user['user']['married_at']
                        update_user['user']['marrieding'] = False
                    else:
                        dm = await self.db.get_data("user_id", update_user['user']['married_at'], "users")
                        um = dm
                        um['user']['married'] = False
                        um['user']['married_at'] = None
                        await self.db.update_data(dm, um, 'users')
                        update_user['user']['married'] = False
                        update_user['user']['married_at'] = None

                if str(ctx.command).lower() in ['card', 'whats', 'hot', 'guess', 'hangman', 'jkp', 'pokemon']:
                    update_user['config']['playing'] = False

                if str(ctx.command).lower() in ['box buy', 'box booster', 'craft', 'box']:
                    update_user['config']['buying'] = False

                if str(ctx.command).lower() in ['mine']:
                    update_user['config']['mine'] = False

                if str(ctx.command).lower() in ['battle', 'raid']:
                    update_user['config']['battle'] = False

                if update_user['security']['status']:
                    update_guild['data']['commands'] += 1

                if (update_guild['data']['commands'] // 1000) > 5 and update_guild['data']['ranking'] == "Bronze":
                    min_ = 1 + (update_guild['data']['commands'] // 1000)
                    chance = randint(min_, 200)
                    if chance < min_:
                        try:
                            update_user['inventory']['coins'] += 1000
                        except KeyError:
                            update_user['inventory']['coins'] = 1000
                        update_guild['data']['ranking'] = "Silver"
                        perms = ctx.channel.permissions_for(ctx.me)
                        if perms.send_messages and perms.read_messages:
                            await ctx.send(f'🎊 **PARABENS** 🎉 {ctx.author} ``você upou sua guilda para o ranking`` '
                                           f'**Silver** ``e ganhou a`` **chance** ``de garimpar mais ethernyas a '
                                           f'partir de agora e `` **+1000** ``Fichas para jogar``')

                elif (update_guild['data']['commands'] // 1000) > 10 and update_guild['data']['ranking'] == "Silver":
                    min_ = 1 + (update_guild['data']['commands'] // 1000)
                    chance = randint(min_, 200)
                    if chance < min_:
                        try:
                            update_user['inventory']['coins'] += 2000
                        except KeyError:
                            update_user['inventory']['coins'] = 2000
                        update_guild['data']['ranking'] = "Gold"
                        perms = ctx.channel.permissions_for(ctx.me)
                        if perms.send_messages and perms.read_messages:
                            await ctx.send(f'🎊 **PARABENS** 🎉 {ctx.author} ``você upou sua guilda para o ranking`` '
                                           f'**Gold** ``e ganhou a`` **chance** ``de garimpar mais ethernyas a '
                                           f'partir de agora e `` **+2000** ``Fichas para jogar``')

                try:
                    cmds_event = len(self.cmd_event[ctx.author.id].keys())
                except KeyError:
                    cmds_event = 0

                if randint(1, 200) - cmds_event < 5 and update_user['security']['status'] and self.event_special:
                    try:
                        del self.cmd_event[ctx.author.id]
                    except KeyError:
                        pass
                    list_chests = []
                    for k, v in self.chests.items():
                        list_chests += [k] * v
                    CHEST = choice(list_chests)
                    chest_type = [k for k in self.chests.keys()].index(CHEST)

                    if ctx.author.id not in self.chests_users:
                        self.chests_users[ctx.author.id] = {"quant": 1, "chests": [chest_type]}
                    else:
                        self.chests_users[ctx.author.id]['quant'] += 1
                        self.chests_users[ctx.author.id]['chests'].append(chest_type)

                    embed = discord.Embed(
                        title="**Baú de Evento Liberado**",
                        colour=self.color,
                        description=f"{ctx.author.mention} foi gratificado com 1 "
                                    f"**{self.chests_l[str(chest_type)]}**!\n "
                                    f"Para abri-lo é so usar o comando ``ash event``\n "
                                    f"**Apenas você pode abrir seu baú**\n"
                                    f"**Obs:** Você tem **{self.chests_users[ctx.author.id]['quant']}** bau(s)!")
                    embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
                    embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                    embed.set_thumbnail(url=CHEST)
                    awards = 'images/elements/chest.gif'
                    file = discord.File(awards, filename="reward_chest.gif")
                    embed.set_image(url="attachment://reward_chest.gif")
                    perms = ctx.channel.permissions_for(ctx.me)
                    if perms.send_messages and perms.read_messages:
                        if perms.embed_links and perms.attach_files:
                            await ctx.send(file=file, embed=embed)
                        else:
                            await ctx.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` **ADICIONAR "
                                           "LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR CORRETAMENTE!**")

                if randint(1, 200) < 3 and update_user['security']['status'] and cmd not in self.block:
                    list_boxes = []
                    for k, v in self.boxes.items():
                        list_boxes += [k] * v

                    BOX = choice(list_boxes)
                    box_type = [k for k in self.boxes.keys()].index(BOX)
                    for _ in range(box_type + 1):
                        if ctx.guild.id not in self.box:
                            self.box[ctx.guild.id] = {"quant": 1, "boxes": [box_type]}
                        else:
                            self.box[ctx.guild.id]['quant'] += 1
                            self.box[ctx.guild.id]['boxes'].append(box_type)

                    embed = discord.Embed(
                        title="**Presente Liberado**",
                        colour=self.color,
                        description=f"Esse servidor foi gratificado com {box_type + 1} presente(s) "
                                    f"**{self.boxes_l[str(box_type)]}**!\n Para abri-lo é so usar o comando "
                                    f"``ash open``\n **qualquer membro pode abrir um presente**\n"
                                    f"**Obs:** Essa guilda tem {self.box[ctx.guild.id]['quant']} presente(s) "
                                    f"disponiveis!")
                    embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
                    embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                    embed.set_thumbnail(url=BOX)
                    perms = ctx.channel.permissions_for(ctx.me)
                    if perms.send_messages and perms.read_messages:
                        if perms.embed_links and perms.attach_files:
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` **ADICIONAR "
                                           "LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR CORRETAMENTE!**")

                patent = patent_calculator(update_user['inventory']['rank_point'], update_user['inventory']['medal'])
                if patent > update_user['user']['patent']:
                    update_user['user']['patent'] = patent
                    file = discord.File(f'images/patente/{patent}.png', filename="patent.png")
                    embed = discord.Embed(title='🎊 **PARABENS** 🎉\n``VOCE SUBIU DE PATENTE``', color=self.color)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_image(url="attachment://patent.png")
                    perms = ctx.channel.permissions_for(ctx.me)
                    if perms.send_messages and perms.read_messages:
                        if perms.embed_links and perms.attach_files:
                            await ctx.send(file=file, embed=embed)
                        else:
                            await ctx.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` **ADICIONAR "
                                           "LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR CORRETAMENTE!**")

                if update_user['config']['vip'] and str(ctx.command).lower() != "daily vip":
                    try:
                        epoch = dt.utcfromtimestamp(0)
                        cooldown = update_user["cooldown"]["daily vip"]
                        time_diff = (dt.utcnow() - epoch).total_seconds() - cooldown
                        if time_diff >= 86400:
                            if update_user['config']['vip']:
                                update_user['config']['vip'] = False
                                if ctx.guild.id == 519894833783898112:
                                    perms = ctx.channel.permissions_for(ctx.me)
                                    if perms.send_messages and perms.read_messages:
                                        await ctx.send(f'<:negate:721581573396496464>│{ctx.author.mention} '
                                                       f'``INFELIZMENTE VOCÊ ACABOU DE PERDER SEU VIP DIARIO!``')

                                        await ctx.send("<:alert:739251822920728708>│``APROVEITE QUE"
                                                       " VC ESTA AQUI E USE O COMANDO`` **ASH VIP**")
                                else:
                                    perms = ctx.channel.permissions_for(ctx.me)
                                    if perms.send_messages and perms.read_messages:
                                        await ctx.send(f'<:negate:721581573396496464>│{ctx.author.mention} '
                                                       f'``INFELIZMENTE VOCÊ ACABOU DE PERDER SEU VIP DIARIO!``\n '
                                                       f'**Vá no meu servidor para receber seu proximo dia de vip!**')
                            else:
                                if (self.guilds_commands[ctx.guild.id] % 10) == 0:
                                    if ctx.guild.id == 519894833783898112:
                                        perms = ctx.channel.permissions_for(ctx.me)
                                        if perms.send_messages and perms.read_messages:
                                            await ctx.send("<:alert:739251822920728708>│``APROVEITE QUE"
                                                           " VC ESTA AQUI E USE O COMANDO`` **ASH VIP**")
                                    else:
                                        perms = ctx.channel.permissions_for(ctx.me)
                                        if perms.send_messages and perms.read_messages:
                                            await ctx.send("<:alert:739251822920728708>│``Você pode ganhar "
                                                           "VIP DIARIO ENTRANDO NO MEU SERVIDOR!``\n "
                                                           "**Saiba mais usando ASH INVITE**")
                    except KeyError:
                        if (self.guilds_commands[ctx.guild.id] % 10) == 0:
                            if ctx.guild.id == 519894833783898112:
                                perms = ctx.channel.permissions_for(ctx.me)
                                if perms.send_messages and perms.read_messages:
                                    await ctx.send("<:alert:739251822920728708>│``APROVEITE QUE VC ESTA"
                                                   " AQUI E USE O COMANDO`` **ASH VIP**")
                            else:
                                perms = ctx.channel.permissions_for(ctx.me)
                                if perms.send_messages and perms.read_messages:
                                    await ctx.send("<:alert:739251822920728708>│``Agora você pode ganhar "
                                                   "VIP DIARIO ENTRANDO NO MEU SERVIDOR!``\n **Saiba mais usando ASH "
                                                   "INVITE**")

                # -----------------------------------------------------------------------------------------
                #                                  INICIO DO MACRO SYSTEM
                # -----------------------------------------------------------------------------------------

                update_user['security']['commands'] += 1
                update_user['security']['commands_today'] += 1
                update_user['security']['last_command'] = dt.today()
                update_user['security']['last_channel'] = ctx.channel.id

                if update_user['security']['last_verify'] is None:
                    update_user['security']['last_verify'] = dt.today()
                    update_user['security']['blocked'] = False

                last_verify_date, date_now = update_user['security']['last_verify'], dt.today()
                data_, limit = date_format(date_now), 2500
                last_verify = date.mktime(last_verify_date.timetuple())
                last_command = date.mktime(date_now.timetuple())
                m_last_verify = int(int(last_command - last_verify) / 60)

                if m_last_verify > 5:
                    update_user['security']['last_verify'] = dt.today()
                    update_user['security']['blocked'] = False
                    last_verify = date.mktime(update_user['security']['last_verify'].timetuple())

                if update_user['security']['last_command'] is not None and update_user['security']['status']:
                    if update_user['security']['commands_today'] > int(limit / 100 * 80):
                        if update_user['security']['commands_today'] < limit:
                            warns = False
                            percent = int(update_user['security']['commands_today'] * 100 / limit)
                            if update_user['security']['commands_today'] >= int(limit / 100 * 80):
                                percent = 80
                            if update_user['security']['commands_today'] >= int(limit / 100 * 85):
                                percent = 85
                            if update_user['security']['commands_today'] >= int(limit / 100 * 90):
                                percent = 90
                            if update_user['security']['commands_today'] >= int(limit / 100 * 95):
                                percent = 95
                            if update_user['security']['commands_today'] >= int(limit / 100 * 100):
                                percent = 100
                            if percent >= 80 and not update_user['security']['warns'][str(percent)]:
                                warns = True
                            if update_user['security']['last_channel'] is not None and warns:
                                channel_ = self.get_channel(update_user['security']['last_channel'])
                                if channel_ is not None:
                                    cmds = update_user['security']['commands_today']
                                    pe = update_user['security']['commands_today'] * 100 / limit
                                    await channel_.send(f'<a:red:525032764211200002>│``VOCE JA ATINGIU`` **{pe}%**'
                                                        f' ``DA SUA COTA DIARIA DE COMANDOS:`` **{cmds}/{limit}** '
                                                        f'``SE CONTINUAR ASSIM VAI SER BLOQUEADO POR 72 HORAS.``')
                                    update_user['security']['warns'][str(percent)] = True

                    if update_user['security']['commands_today'] > limit:
                        update_user['security']['status'] = not update_user['security']['status']
                        update_user['security']['blocked'] = not update_user['security']['blocked']
                        update_user['security']['last_blocked'] = dt.today()
                        update_user['security']['strikes_to_ban'] += 1
                        channel_ = self.get_channel(737467830571761786)
                        user = self.get_user(update_user["user_id"])
                        await channel_.send(f'```O USUARIO {update_user["user_id"]} {user} ESTAVA POSSIVELMENTE USANDO'
                                            f' MACRO E FOI BLOQUEADO\nNa Data e Hora: {data_}```')

                        if update_user['security']['last_channel'] is not None:
                            channel_ = self.get_channel(update_user['security']['last_channel'])
                            if channel_ is not None:
                                await channel_.send(f'<a:red:525032764211200002>│``VOCE FOI BLOQUEADO POR 72 HORAS '
                                                    f'POIS EXTRAPOLOU OS LIMITES HOJE``\n<a:red:525032764211200002>'
                                                    f' **OBS: VOCE AINDA PODE USAR O BOT, POREM PERDEU OS '
                                                    f'PRIVILEGIOS DE GANHAR OS ITENS** ``ESSE BLOQUEIO FOI MAIS '
                                                    f'RIGIDO,`` **SE VOCE CONTINUAR LEVANDO ESSE BLOQUEIO IRÁ SER'
                                                    f' BANIDO DE USAR MEUS SERVIÇOS** ``AVISO PARA BANIMENTO:`` '
                                                    f'**{update_user["security"]["strikes_to_ban"]}**/10')

                    if update_user['security']['strikes_to_ban'] > 10:
                        answer = await self.ban_(update_user['user_id'], "BANIDO POR USAR MACRO!")
                        if answer:
                            embed = discord.Embed(
                                color=discord.Color.red(),
                                description=f'<:cry:530735037243719687>│``VOCE FOI BANIDO POR USAR MACRO!``'
                                            f' **SE QUISER CONTESTAR ENTRE NO MEU SERVIDOR DE SUPORTE!**')
                            if update_user['security']['last_channel'] is not None:
                                channel_ = self.get_channel(update_user['security']['last_channel'])
                                if channel_ is not None:
                                    await channel_.send(embed=embed)

                    m_last_verify = int(int(last_command - last_verify) / 60)
                    if m_last_verify < 5 and update_user['security']['commands'] > 40:

                        update_user['security']['strikes'] += 1
                        update_user['security']['commands'] = 0
                        channel_ = self.get_channel(737467830571761786)
                        user = self.get_user(update_user["user_id"])
                        await channel_.send(f'```O USUARIO {update_user["user_id"]} {user} FOI DETECTADO POSSIVELMENTE'
                                            f' USANDO MACRO\nNa Data e Hora: {data_}```')

                        if update_user['security']['strikes'] < 11:
                            if update_user['security']['last_channel'] is not None:
                                channel_ = self.get_channel(update_user['security']['last_channel'])
                                if channel_ is not None:
                                    await channel_.send(f'<a:red:525032764211200002>│``EI TENHA CALMA VOCE TA '
                                                        f'USANDO COMANDOS RAPIDO DEMAIS, SE CONTINUAR ASSIM VAI SER'
                                                        f' BLOQUEADO ATE AS 0 HORAS DO DIA DE HOJE.`` '
                                                        f'<a:red:525032764211200002>'
                                                        f'**AVISO {update_user["security"]["strikes"]}/10**')

                    if update_user['security']['commands'] > 0:
                        update_user['security']['commands'] = 0

                    else:
                        update_user['security']['commands'] = 0
                        update_user['security']['strikes'] = 0

                    if update_user['security']['strikes'] == 11:
                        update_user['security']['status'] = not update_user['security']['status']
                        channel_ = self.get_channel(737467830571761786)
                        user = self.get_user(update_user["user_id"])
                        await channel_.send(f'```O USUARIO {update_user["user_id"]} {user} ESTAVA POSSIVELMENTE USANDO'
                                            f' MACRO E FOI BLOQUEADO\nNa Data e Hora: {data_}```')

                        if update_user['security']['last_channel'] is not None:
                            channel_ = self.get_channel(update_user['security']['last_channel'])
                            if channel_ is not None:
                                await channel_.send(f'<a:red:525032764211200002>│``VOCE FOI BLOQUEADO ATE AS 0 '
                                                    f'HORAS DO DIA DE HOJE..`` <a:red:525032764211200002>'
                                                    f'**OBS: VOCE AINDA PODE USAR O BOT, POREM PERDEU OS '
                                                    f'PRIVILEGIOS DE GANHAR OS ITENS**')

                # -----------------------------------------------------------------------------------------
                #                                    FIM DO MACRO SYSTEM
                # -----------------------------------------------------------------------------------------

                await self.db.update_data(data_user, update_user, 'users')
                await self.db.update_data(data_guild, update_guild, 'guilds')

                if isinstance(ctx.author, discord.Member) and data_user is not None:
                    if str(ctx.command) not in self.no_panning:
                        msg = await self.db.add_money(ctx, randint(6, 12), True)
                        perms = ctx.channel.permissions_for(ctx.me)
                        if perms.send_messages and perms.read_messages:
                            await ctx.send(f"``Por usar um comando, {_name} tambem ganhou`` {msg}", delete_after=5.0)

    async def on_guild_join(self, guild):
        if str(guild.id) in self.blacklist:
            msg = "EU FUI RETIRADA DESSE SERVIDOR SEM MOTIVO APARENTE, LOGO VC DEVE ENTRAR COM UM PEDIDO PARA RETIRAR" \
                  " SEU SERVIDOR (GUILD) DA MINHA LISTA NEGRA, VOCÊ PODE FAZER ISSO ENTRANDO NO MEU SERVIDOR (GUILD)" \
                  " DE SUPORTE E FALANDO COM UM DOS MEUS DESENVOLVEDORES\n LINK DO SERVIDOR:\n " \
                  "https://discord.gg/rYT6QrM"
            try:
                await guild.system_channel.send(msg)
            except discord.errors.Forbidden:
                pass
            await guild.leave()
        else:
            entrance = self.get_channel(619899848082063372)
            embed = await guild_info(guild)
            await entrance.send(embed=embed)

    async def on_guild_remove(self, guild):
        if str(guild.id) not in self.blacklist:
            data = await self.db.get_data("guild_id", guild.id, "guilds")
            if data is not None:
                blacklist = self.get_channel(542134573010518017)
                msg = f"> **{guild.id}:** {guild.name} ``ME RETIROU DO SERVIDOR LOGO ENTROU NA BLACKLIST``"
                await blacklist.send(msg)
                embed = await guild_info(guild)
                await blacklist.send(embed=embed)
                await self.ban_(guild.id, msg)
            else:
                blacklist = self.get_channel(542134573010518017)
                msg = f"> **{guild.id}:** {guild.name} ``ME RETIROU DO SERVIDOR MAS NÃO TINHA FEITO O RESGISTRO, " \
                      f"ENTÃO NÃO ENTROU NA MINHA BLACKLIST!``"
                await blacklist.send(msg)
                embed = await guild_info(guild)
                await blacklist.send(embed=embed)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        ctx = await self.get_context(message)
        if str(ctx.command) != "eval":
            msg = copy.copy(message)
            msg.content = message.content.lower()
        else:
            msg = copy.copy(message)

        ctx = await self.get_context(msg)
        perms = ctx.channel.permissions_for(ctx.me)
        if not perms.send_messages or not perms.read_messages:
            return

        if ctx.command is not None:
            if not perms.embed_links or not perms.attach_files:
                return await ctx.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` **ADICIONAR "
                                      "LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR CORRETAMENTE!**")
            if message.author.id not in self.testers and self.maintenance:
                msg = self.config['attribute']['maintenance']
                embed = discord.Embed(color=self.color, description=msg)
                return await message.channel.send(embed=embed)

        self.msg_cont += 1

        if message.webhook_id is not None:
            return await self.invoke(ctx)

        if message.guild is not None and str(message.author.id) not in self.blacklist:
            await self.data.add_experience(message, randint(5, 15))

            run_command = False
            data_guild = await self.db.get_data("guild_id", message.guild.id, "guilds")
            if data_guild is not None:
                if data_guild['command_locked']['status']:
                    if message.channel.id in data_guild['command_locked']['while_list']:
                        run_command = True
                else:
                    if message.channel.id not in data_guild['command_locked']['black_list']:
                        run_command = True
            else:
                run_command = True
                if message.guild.system_channel is not None and (self.msg_cont % 10) == 0:
                    if await verify_cooldown(self, f"{message.guild.id}_no_register", 86400):
                        embed = discord.Embed(
                            color=self.color,
                            description="<a:blue:525032762256785409>│``SEU SERVIDOR AINDA NAO ESTA CADASTRADO USE``"
                                        " **ASH REGISTER GUILD** ``PARA QUE EU POSSA PARTICIPAR DAS ATIVIDADES DE "
                                        "VOCES TAMBEM, É MUITO FACIL E RAPIDO. QUALQUER DUVIDA ENTRE EM CONTATO COM "
                                        "MEU SERVIDOR DE SUPORTE`` [CLICANDO AQUI](https://discord.gg/rYT6QrM)")
                        try:
                            await message.guild.system_channel.send(embed=embed)
                        except discord.Forbidden:
                            try:
                                if message.guild.owner is not None:
                                    await message.guild.owner.send(embed=embed)
                                else:
                                    await message.channel.send(embed=embed)
                            except discord.Forbidden:
                                pass
            if str(ctx.command) in ['channel', 'daily']:
                run_command = True

            if run_command:
                if msg.content in self.shortcut:
                    msg.content = self.shortcut[message.content.lower()]
                await self.process_commands(msg)
            else:
                if ctx.command is not None:
                    await message.channel.send("<:alert:739251822920728708>|``NAO POSSO EXECUTAR COMANDOS NESSE"
                                               " CANAL!``\n**CASO QUERIA ALTERAR ESSA CONFIGURAÇÃO, USE O COMANDO "
                                               "ASH CHANNEL**")

    @staticmethod
    def get_ram():
        mem = psutil.virtual_memory()
        return f"{mem.used / 0x40_000_000:.2f}/{mem.total / 0x40_000_000:.2f}GB ({mem.percent}%)"

    async def web_hook_rpg(self, ctx, avatar_dir, web_hook_name, msg, quest_name):

        perms = ctx.channel.permissions_for(ctx.me)
        if not perms.manage_webhooks:
            if not perms.send_messages:
                return
            return await ctx.send(f'<:negate:721581573396496464>│``Eu não tenho a permissão de:`` '
                                  f'**Gerenciar Webhooks**')

        avatar = open(avatar_dir, 'rb')
        _webhook = await ctx.channel.create_webhook(name=web_hook_name, avatar=avatar.read())
        emoji = choice(self.config['emojis']['ashley'])
        guild = self.get_guild(519894833783898112)
        link = [emo for emo in guild.emojis if str(emo) == emoji][0].url

        webhook = Webhook(url=_webhook.url)
        content = f"{quest_name} do {ctx.author.name} disse:\n```{msg}```"
        webhook.embed = discord.Embed(
            colour=random_color(),
            description=f"{content if quest_name != 'Ashley' else msg}",
            timestamp=dt.utcnow()
        ).set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
        ).set_thumbnail(
            url=link
        ).to_dict()
        await webhook.send()
        await _webhook.delete()


if __name__ == "__main__":

    with open("data/auth.json") as auth:
        _auth = json.loads(auth.read())

    description_ashley = f"Um bot de assistencia para servidores criado por: Denky#5960\n" \
                         f"**Adicione para seu servidor:**: {config['config']['default_link']}\n" \
                         f"**Servidor de Origem**: {config['config']['default_invite']}\n"

    intents = discord.Intents.default()
    intents.members = True
    bot = Ashley(command_prefix=['ash.', 'ash '], description=description_ashley, pm_help=True, intents=intents)
    bot.remove_command('help')
    cont = 0
    emojis = {"ON": "🟢", "IDLE": "🟡", "OFF": "🔴", "VIP": "🟣"}

    print("\033[1;35m( >> ) | Iniciando...\033[m\n")
    print("\033[1;35m( >> ) | Iniciando carregamento de extensões...\033[m")

    if bot.maintenance:
        f = open("maintenance.txt", "r")
    else:
        f = open("modulos.txt", "r")

    for name in f.readlines():
        if len(name.strip()) > 0:
            try:
                if '@' not in name.strip() and '#' not in name.strip():
                    bot.load_extension(name.strip())
                    if name.strip() not in bot.vip_cog:
                        bot.data_cog[name.strip()] = emojis['ON']
                    else:
                        bot.data_cog[name.strip()] = emojis['VIP']
                    cont += 1
                else:
                    if '#' not in name.strip():
                        print(f'\033[1;36m( ☢️ ) | Cog: \033[1;34m{name.strip()}\033[1;36m não foi carregada!\33[m')
                        bot.data_cog[name.strip()] = emojis['OFF']
            except Exception as e:
                if '#' not in name.strip():
                    print(f"\033[1;31m( ❌ ) | Cog: \033[1;34m{name}\033[1;31m teve um [Erro] : \033[1;35m{e}\33[m")
                    bot.data_cog[name.strip()] = emojis['IDLE']
                    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
                continue
    f.close()

    print(f"\033[1;35m( ✔ ) | {cont}/{len(bot.data_cog.keys())} extensões foram carregadas!\033[m")
    bot.run(_auth['_t__ashley'])
