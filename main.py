# ARQUIVO PRINCIPAL DE INICIALIZAÇÃO DO BOT: ASHLEY PARA DISCORD.
# CRIADO POR: DANIEL AMARAL -> Denky#5960
# SEGUE ABAIXO OS IMPORTS COMPLETOS
import discord
import logging
import psutil
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
                              'SEJA VIP: SENDO VIP VOCÊ ACABA COM OS ANUNCIOS',
                              'SISTEMA DE ANUNCIOS: O SISTEMA DE ANUNCIO EXISTE PARA EU PODER ME MANTER']
        self.languages = ("pt", "en")
        self.version = "5.3.6"
        self.server_ = "heroku"
        self.prefix_ = "'ash.', 'ash '"
        self.all_prefix = ['ash.', 'Ash.', 'aSh.', 'asH.', 'ASh.', 'aSH.', 'ASH.', 'AsH.',
                           'ash ', 'Ash ', 'aSh ', 'asH ', 'ASh ', 'aSH ', 'ASH ', 'AsH ']
        self.github = "https://github.com/Ashley-Lab/Ashley"
        self.progress = "V.5 -> 36.0%"
        self.data_cog = {}
        self.vip_cog = ['commands.music.default', 'commands.admin.staff']

        self.log_dir = os.path.dirname(__file__)
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename=os.path.join(self.log_dir, 'discord.log'), encoding='utf-8',
                                           mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

        self.db: Database = Database(self)
        self.data: DataInteraction = DataInteraction(self)

        self.staff = [235937029106434048, 300592580381376513]
        self.bl_item = ['medal', 'rank_point']

        with open("resources/translations.json") as translations:
            self.translations = json.loads(translations.read())

        with open("resources/blacklist.json") as blacklist:
            self.blacklist = json.loads(blacklist.read())

        with open("resources/shutdown.json") as shutdown:
            self.shutdowns = json.loads(shutdown.read())

    def shutdown(self, reason):
        date = dt(*dt.utcnow().timetuple()[:6])
        self.shutdowns['shutdown'][f"{date}"] = reason
        with open("resources/shutdown.json", "w") as shutdown:
            json.dump(self.shutdowns, shutdown)
        shutdown.close()

    def ban_(self, id_: str, reason: str):
        date = dt(*dt.utcnow().timetuple()[:6])
        if id_ not in self.blacklist:
            self.blacklist[id_] = {f"{date}": reason}
        else:
            self.blacklist[id_][f"{date}"] = reason
        with open("resources/blacklist.json", "w") as blacklist:
            json.dump(self.blacklist, blacklist)
        blacklist.close()

    def un_ban_(self, id_: str):
        if id_ not in self.blacklist:
            return
        del self.blacklist[id_]
        with open("resources/blacklist.json", "w") as blacklist:
            json.dump(self.blacklist, blacklist)
        blacklist.close()

    async def on_command(self, ctx):
        if ctx.guild is not None:
            data = self.db.get_data("guild_id", ctx.guild.id, "guilds")
            data_user = self.db.get_data("user_id", ctx.author.id, "users")
            if isinstance(ctx.author, discord.Member) and data is not None:
                self.commands_used[ctx.command] += 1
                self.guilds_commands[ctx.guild.id] += 1
                self.user_commands[ctx.author.id] += 1
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

    async def on_command_completion(self, ctx):
        if ctx.guild is not None:
            if ctx.author.id not in self.blacklist:
                await self.data.level_up(ctx)
            data = self.db.get_data("guild_id", ctx.guild.id, "guilds")
            data_user = self.db.get_data("user_id", ctx.author.id, "users")
            if isinstance(ctx.author, discord.Member) and data is not None:
                await self.db.add_money(ctx, 6)
                await self.data.add_experience(ctx.message, 5)
            if isinstance(ctx.author, discord.Member) and data_user is not None:
                update_user = data_user
                try:
                    update_user['user']['commands'] += 1
                except KeyError:
                    update_user['user']['commands'] = 1
                if (update_user['user']['commands'] % 10) == 0:
                    chance = randint(1, 100)
                    if chance >= 80:
                        update_user['inventory']['rank_point'] += 1
                        await ctx.send("<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``VOCÊ GANHOU:`` "
                                       "<:coin:519896843388452864> **1** ``RANKPOINT A MAIS!``")
                if (update_user['user']['commands'] % 50) == 0:
                    guild_ = self.get_guild(update_user['guild_id'])
                    if guild_ is None:
                        await ctx.send("<:negate:520418505993093130>│``SUA GUILDA DE CADASTRO FOI DELETADA, TENTE "
                                       "USAR O COMANDO`` **ASH TRANS** ``PARA MUDAR SUA GUILDA DE ORIGEM``")
                if (update_user['user']['commands'] % 100) == 0:
                    chance = randint(1, 100)
                    if chance >= 90:
                        update_user['inventory']['medal'] += 1
                        await ctx.send("<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``VOCÊ GANHOU:`` "
                                       "<:coin:519896843388452864> **1** ``MEDALHA A MAIS!``")
                self.db.update_data(data_user, update_user, 'users')

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
        if guild.id in self.blacklist:
            await guild.leave()

    async def on_guild_remove(self, guild):
        if guild.id not in self.blacklist:
            blacklist = self.get_channel(542134573010518017)
            await blacklist.send(f"{guild.id}: **{guild.name}** ``ME RETIROU DO SERVIDOR LOGO ENTROU NA BLACKLIST``")
            self.ban_(guild.id, f"{guild.id}: **{guild.name}** ``ME RETIROU DO SERVIDOR LOGO ENTROU NA BLACKLIST``")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.author.id not in self.blacklist:
            await self.process_commands(message)

        if message.guild is not None and message.author.id not in self.blacklist:
            await self.data.add_experience(message, 5)
            if message.content.lower() == "ash rec":
                msg = copy.copy(message)
                msg.content = "ash daily rec"
                await self.process_commands(msg)

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
