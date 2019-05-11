# ARQUIVO PRINCIPAL DE INICIALIZAÇÃO DO BOT: ASHLEY PARA DISCORD.
# CRIADO POR: DANIEL AMARAL -> Denky#5960
# SEGUE ABAIXO OS IMPORTS COMPLETOS
import discord
import logging
import psutil
import datetime
import json
import os
import copy
# SEGUE ABAIXO OS IMPORTS PARCIAIS
from random import choice, randint
from datetime import datetime as dt
from collections import Counter
from discord.ext import commands
from resources.color import random_color
from resources.webhook import WebHook
from bson.json_util import dumps
# from resources.translation import t_
from resources.utility import ERRORS
from resources.db import Database, DataInteraction


# CLASSE PRINCIPAL SENDO SUBCLASSE DA BIBLIOTECA DISCORD
class Ashley(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, shard_count=1, **kwargs)
        self.owner_id = 300592580381376513
        self.start_time = dt.utcnow()
        self.commands_used = Counter()
        self.guilds_commands = Counter()
        self.guilds_messages = Counter()
        self.user_commands = Counter()
        self.announcements = ['ANUNCIE COMIGO: ENTRE NO MEU SERVIDOR E SAIBA COMO ANUNCIAR!',
                              'SISTEMA DE LINGAGUEM: O IDIOMA INGLES SERÁ LIBERADO EM POUCAS SEMANAS!',
                              'VIP: AO ENTRAR NO MEU SERVIDOR VOCÊ SE TORNA VIP!',
                              'O COMANDO "RANK" ESTÁ FINALIZADO, AGORA VOCÊ PODERÁ OLHAR SEU RANK A QUALQUER MOMENTO!',
                              'O COMANDO REC SERVE PARA VOCÊ ADIQUIRIR ESTRELAS NO SEU RANK!',
                              'A COR DAS ESTRELAS VARIA PELO SEU RANKING ATUAL (BRONZE, PRATA OU OURO) OU DO SEU STATUS'
                              'QUE PODE SER: VIP MEMBRO, DONO DE SERVIDOR (GUILD) OU MEU DESENVOLVEDOR!',
                              'PARA SUBIR DE PATENTE, VC PRECISA USAR OS MEUS COMANDOS E FARMAR RANKPOINTS E MEDALHAS!',
                              'QUANTO MAIS COMANDOS DIFERENTES VC USAR, MAIS CHANCES DE VC SUBIR O SEU NIVEL DE '
                              'RANKING',
                              'VC ADQUIRE DINHEIRO USANDO OS COMANDOS GERAIS E OS COMANDOS DIARIOS, TAIS COMO:'
                              '"ASH DAILY REC", "ASH DAILY COIN", "ASH DAILY WORK" OU "ASH DAILY VIP"!',
                              'SISTEMA DE ANUNCIOS: O SISTEMA DE ANUNCIO EXISTE PARA EU ME MANTER!']
        self.languages = ("pt", "en")
        self.version = "5.5.0"
        self.server_ = "HEROKU"
        self.prefix_ = "'ash.', 'ash '"
        self.all_prefix = ['ash.', 'Ash.', 'aSh.', 'asH.', 'ASh.', 'aSH.', 'ASH.', 'AsH.',
                           'ash ', 'Ash ', 'aSh ', 'asH ', 'ASh ', 'aSH ', 'ASH ', 'AsH ']
        self.github = "https://github.com/Ashley-Lab/Ashley"
        self.progress = "V.5 -> 50.0%"
        self.data_cog = {}
        self.shortcut = {'ash coin': 'ash daily coin', 'ash work': 'ash daily work', 'ash rec': 'ash daily rec',
                         'ash vip': 'ash daily vip'}
        self.vip_cog = ['commands.music.default', 'commands.admin.staff']
        self.titling = {"10": "Vassal", "25": "Heir", "50": "Knight", "100": "Elder", "200": "Baron", "300": "Viscount",
                        "400": "Count", "500": "Marquis", "1000": "Duke", "1500": "Grand Duke"}

        self.ld = os.path.dirname(__file__)
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename=os.path.join(self.ld, 'discord.log'), encoding='utf-8', mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

        self.db: Database = Database(self)
        self.data: DataInteraction = DataInteraction(self)

        self.staff = [235937029106434048, 300592580381376513]
        self.bl_item = ['medal', 'rank_point']
        self.blacklist = dumps(self.db.get_all_data("blacklist"))
        self.shutdowns = dumps(self.db.get_all_data("shutdown"))

        with open("resources/translations.json") as translations:
            self.translations = json.loads(translations.read())

        with open("resources/items.json") as items:
            self.items = json.loads(items.read())

        with open("resources/icons.json") as icons:
            self.icons = json.loads(icons.read())

    def shutdown(self, reason):
        date = dt(*dt.utcnow().timetuple()[:6])
        data = {"_id": date, "reason": reason}
        self.db.push_data(data, "shutdown")
        self.shutdowns = dumps(self.db.get_all_data("shutdown"))

    def ban_(self, id_, reason: str):
        date = dt(*dt.utcnow().timetuple()[:6])
        data = {"_id": id_, str(date): reason}
        if str(id_) not in self.blacklist:
            self.db.push_data(data, "blacklist")
            self.blacklist = dumps(self.db.get_all_data("blacklist"))
            return True
        else:
            return False

    def un_ban_(self, id_):
        if str(id_) not in self.blacklist:
            return False
        else:
            self.db.delete_data({"_id": int(id_)}, "blacklist")
            self.blacklist = dumps(self.db.get_all_data("blacklist"))
            return True

    async def on_command(self, ctx):
        if ctx.guild is not None:
            data = self.db.get_data("guild_id", ctx.guild.id, "guilds")
            data_user = self.db.get_data("user_id", ctx.author.id, "users")
            if isinstance(ctx.author, discord.Member) and data is not None:
                self.commands_used[ctx.command] += 1
                self.guilds_commands[ctx.guild.id] += 1
                self.user_commands[ctx.author.id] += 1
                update = data
                try:
                    update['data']['commands'] += 1
                except KeyError:
                    update['data']['commands'] = 1
                self.db.update_data(data, update, 'guilds')
                if data_user is not None:
                    if not data_user['config']['vip']:
                        if (self.guilds_commands[ctx.guild.id] % 20) == 0:
                            for data in self.db.get_announcements():
                                self.announcements.append(data["data"]["announce"])
                            announce = choice(self.announcements)
                            embed = discord.Embed(
                                color=0x000000,
                                description=f'<:confirmado:519896822072999937>│**ANUNCIO**\n '
                                f'```{announce}```')
                            await ctx.send(embed=embed)
                    else:
                        try:
                            epoch = datetime.datetime.utcfromtimestamp(0)
                            cooldown = data_user["cooldown"]["daily vip"]
                            time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - cooldown
                            if time_diff >= 86400:
                                data_ = self.db.get_data("user_id", ctx.author.id, "users")
                                update_ = data_
                                if update_['config']['vip']:
                                    update_['config']['vip'] = False
                                    self.db.update_data(data_, update_, 'users')
                                    await ctx.send(f'<:negate:520418505993093130>│{ctx.author.mention} ``INFELIZMENTE'
                                                   f' VOCÊ ACABOU DE PERDER SEU VIP DIARIO!``\n **Vá no meu servidor'
                                                   f' para receber seu proximo dia de vip!**')
                                else:
                                    if (self.guilds_commands[ctx.guild.id] % 10) == 0:
                                        await ctx.send("<:alert_status:519896811192844288>**│** ``Você pode ganhar "
                                                       "VIP DIARIO ENTRANDO NO MEU SERVIDOR!``\n **Saiba mais usando "
                                                       "ASH INVITE**")
                        except KeyError:
                            if (self.guilds_commands[ctx.guild.id] % 10) == 0:
                                await ctx.send("<:alert_status:519896811192844288>**│** ``Agora você pode ganhar "
                                               "VIP DIARIO ENTRANDO NO MEU SERVIDOR!``\n **Saiba mais usando ASH "
                                               "INVITE**")

    async def on_command_completion(self, ctx):
        if ctx.guild is not None:
            if str(ctx.author.id) not in self.blacklist:
                await self.data.level_up(ctx)
            data = self.db.get_data("guild_id", ctx.guild.id, "guilds")
            data_user = self.db.get_data("user_id", ctx.author.id, "users")
            if isinstance(ctx.author, discord.Member) and data_user is not None:
                update_user = data_user
                try:
                    update_user['user']['commands'] += 1
                except KeyError:
                    update_user['user']['commands'] = 1
                if (update_user['user']['commands'] % 10) == 0:
                    chance = randint(1, 100)
                    if chance >= 51:
                        update_user['inventory']['rank_point'] += 1
                        await ctx.send("<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``VOCÊ GANHOU:`` "
                                       "<:coin:519896843388452864> **1** ``RANKPOINT A MAIS!``")
                if (update_user['user']['commands'] % 50) == 0:
                    guild_ = self.get_guild(update_user['guild_id'])
                    if guild_ is None:
                        await ctx.send("<:negate:520418505993093130>│``SUA GUILDA DE CADASTRO FOI DELETADA, TENTE "
                                       "USAR O COMANDO`` **ASH TRANS** ``PARA MUDAR SUA GUILDA DE ORIGEM``")
                if (update_user['user']['commands'] % 20) == 0:
                    chance = randint(1, 100)
                    if chance >= 80:
                        update_user['inventory']['medal'] += 1
                        await ctx.send("<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``VOCÊ GANHOU:`` "
                                       "<:coin:519896843388452864> **1** ``MEDALHA A MAIS!``")
                for key in self.titling.keys():
                    if update_user['user']['commands'] >= int(key):
                        update_user['user']['titling'] = self.titling[key]
                self.db.update_data(data_user, update_user, 'users')
                if isinstance(ctx.author, discord.Member) and data is not None:
                    await self.db.add_money(ctx, 6)

    async def on_command_error(self, ctx, exception):
        logging.info(f"Exception in {ctx.command}, {ctx.guild}: {ctx.channel}. With error: {exception}")
        if isinstance(exception, commands.MissingRequiredArgument):
            await ctx.send(f"<:negate:520418505993093130>│``ESTÁ FALTANDO ALGO PARA QUE VOCÊ POSSA USAR ESSE "
                           f"COMANDO!``")
        elif isinstance(exception, commands.CheckFailure):
            if exception.__str__() == 'The check functions for command register guild failed.':
                await ctx.send(f"<:negate:520418505993093130>│``VOCÊ NÃO TEM PERMISSÃO PARA USAR ESSE COMANDO!``")
            elif exception.__str__() not in ERRORS:
                await ctx.send(f"{exception}")
        elif isinstance(exception, commands.CommandOnCooldown):
            await ctx.send(f"<:negate:520418505993093130>│**Aguarde**: `Você deve esperar` **{{:.2f}}** "
                           f"`segundos` `para mandar outro comando!`".format(exception.retry_after),
                           delete_after=float("{:.2f}".format(exception.retry_after)))
        else:
            if isinstance(exception, commands.errors.DiscordException):
                return
            elif exception.__str__() not in ERRORS and not isinstance(exception, commands.CommandNotFound):
                channel = self.get_channel(530419409311760394)
                await channel.send(f"<:oc_status:519896814225457152>│``Ocorreu um erro no comando:`` "
                                   f"**{ctx.command}**, ``no servidor:`` **{ctx.guild}**, ``no canal:`` "
                                   f"**{ctx.channel}** ``e o erro foi:`` **{exception}**")

    async def on_guild_join(self, guild):
        if str(guild.id) in self.blacklist:
            owner = self.get_user(guild.owner.id)
            msg = "EU FUI RETIRADA DESSE SERVIDOR SEM MOTIVO APARENTE, LOGO VC DEVE ENTRAR COM UM PEDIDO PARA RETIRAR" \
                  " SEU SERVIDOR (GUILD) DA MINHA LISTA NEGRA, VOCÊ PODE FAZER ISSO ENTRANDO NO MEU SERVIDOR (GUILD)" \
                  " DE SUPORTE E FALANDO COM UM DOS MEUS DESENVOLVEDORES\n LINK DO SERVIDOR:\n " \
                  "https://discord.gg/rYT6QrM"
            try:
                await owner.send(msg)
            except discord.errors.Forbidden:
                await guild.system_channel.send(msg)
            await guild.leave()

    async def on_guild_remove(self, guild):
        if str(guild.id) not in self.blacklist:
            blacklist = self.get_channel(542134573010518017)
            msg = f"{guild.id}: **{guild.name}** ``ME RETIROU DO SERVIDOR LOGO ENTROU NA BLACKLIST``"
            await blacklist.send(msg)
            self.ban_(guild.id, msg)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.guild is not None and str(message.author.id) not in self.blacklist:
            await self.data.add_experience(message, 5)
            if message.content.lower() in self.shortcut:
                msg = copy.copy(message)
                msg.content = self.shortcut[message.content.lower()]
                await self.process_commands(msg)
                shortcut = self.get_channel(575688812068339717)
                await shortcut.send(f"**{message.content.lower()}**: ``atalho usado com sucesso!``")
            else:
                await self.process_commands(message)

    @staticmethod
    def get_ram():
        mem = psutil.virtual_memory()
        return f"{mem.used / 0x40_000_000:.2f}/{mem.total / 0x40_000_000:.2f}GB ({mem.percent}%)"

    @staticmethod
    async def web_hook_rpg(ctx, avatar_dir, web_hook_name, msg, quest_name):
        avatar = open(avatar_dir, 'rb')
        web_hook_ = await ctx.channel.create_webhook(name=web_hook_name, avatar=avatar.read())
        if 'a_' in web_hook_.avatar:
            format_1 = '.gif'
        else:
            format_1 = '.webp'
        web_hook = WebHook(url=web_hook_.url)
        web_hook.embed = discord.Embed(
            colour=random_color(),
            description=f"{quest_name} do {ctx.author.name} disse:\n```{msg}```",
            timestamp=dt.utcnow()
        ).set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
        ).set_thumbnail(
            url=f'https://cdn.discordapp.com/avatars/{web_hook_.id}/{web_hook_.avatar}{format_1}?size=1024'
        ).to_dict()
        web_hook.send_()
        await web_hook_.delete()


if __name__ == "__main__":

    with open("resources/auth.json") as security:
        _auth = json.loads(security.read())

    description_ashley = f"Um bot de assistencia para servidores criado por: Denky#5960\n" \
        f"**Adicione para seu servidor:**: {_auth['default_link']}\n" \
        f"**Servidor de Origem**: {_auth['default_invite']}\n"

    prefix = ['ash.', 'Ash.', 'aSh.', 'asH.', 'ASh.', 'aSH.', 'ASH.', 'AsH.',
              'ash ', 'Ash ', 'aSh ', 'asH ', 'ASh ', 'aSH ', 'ASH ', 'AsH ']

    bot = Ashley(command_prefix=prefix, description=description_ashley, pm_help=True, case_insensitive=True)
    bot.remove_command('help')

    try:
        f = open("resources/modulos.txt", "r")
        for name in f.readlines():
            if len(name.strip()) > 0:
                try:
                    if '@' not in name.strip() and '#' not in name.strip():
                        bot.load_extension(name.strip())
                        if name.strip() not in bot.vip_cog:
                            bot.data_cog[name.strip()] = "<:on_status:519896814799945728>"
                        else:
                            bot.data_cog[name.strip()] = "<:stream_status:519896814825242635>"
                    else:
                        if '#' not in name.strip():
                            print(f'\033[1;30mCog: \033[1;34m{name.strip()}\033[1;30m não foi carregada!\33[m')
                            bot.data_cog[name.strip()] = "<:oc_status:519896814225457152>"
                except Exception as e:
                    if '#' not in name.strip():
                        print(
                            '\033[1;30mCog: \033[1;34m{}\033[1;30m teve um [Erro] : \033[1;31m{}\33[m'.format(name, e))
                        bot.data_cog[name.strip()] = "<:alert_status:519896811192844288>"
                    continue
        f.close()
    except Exception as e:
        print('[Erro] : {}'.format(e))

    bot.run(_auth['_t__ashley'])
