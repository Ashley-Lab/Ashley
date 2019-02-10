# ARQUIVO PRINCIPAL DE INICIALIZAÇÃO DO BOT: ASHLEY PARA DISCORD.
# CRIADO POR: DANIEL AMARAL -> Denky#0001
# SEGUE ABAIXO OS IMPORTS COMPLETOS
import discord
import logging
import psutil
import json
import os
# SEGUE ABAIXO OS IMPORTS PARCIAIS
from random import choice
from datetime import datetime as dt
from collections import Counter
from discord.ext import commands
from resources.color import random_color
from resources.webhook import WebHook
from resources.translation import t_
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
        self.announcements = ['**Anuncie comigo**: ``ENTRE NA FP E SAIBA COMO ANUNCIAR!``',
                              '**Seja VIP**: ``SENDO VIP VOCÊ ACABA COM OS ANUNCIOS``']
        self.languages = ("pt", "en")
        self.version = "4.9.5"
        self.server_ = "heroku"
        self.prefix_ = "'ash.', 'ash '"
        self.all_prefix = ['ash.', 'Ash.', 'aSh.', 'asH.', 'ASh.', 'aSH.', 'ASH.', 'AsH.',
                           'ash ', 'Ash ', 'aSh ', 'asH ', 'ASh ', 'aSH ', 'ASH ', 'AsH ']
        self.github = "FECHADO"
        self.progress = "99.5%"
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

    async def on_command(self, ctx):
        if ctx.guild is not None:
            data = self.db.get_data("guild_id", ctx.guild.id, "guilds")
            if isinstance(ctx.author, discord.Member) and data is not None:
                self.commands_used[ctx.command] += 1
                self.guilds_commands[ctx.guild.id] += 1
                if not data['vip']:
                    if (self.guilds_commands[ctx.guild.id] % 20) == 0:
                        for data in self.db.get_announcements():
                            self.announcements.append(data["data"]["announce"])
                        announce = choice(self.announcements)
                        await ctx.send(t_(ctx, f"{announce}", "guilds"))

    async def on_command_completion(self, ctx):
        if ctx.guild is not None:
            data = self.db.get_data("guild_id", ctx.guild.id, "guilds")
            if isinstance(ctx.author, discord.Member) and data is not None:
                await self.db.add_money(ctx, 6)
                await self.data.add_experience(ctx.message, 5)

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
            if exception.__str__() not in ERRORS and not isinstance(exception, commands.CommandNotFound):
                channel = self.get_channel(530419409311760394)
                await channel.send(f"<:oc_status:519896814225457152>│``Ocorreu um erro no comando:`` "
                                   f"**{ctx.command}**, ``no servidor:`` **{ctx.guild}**, ``no canal:`` "
                                   f"**{ctx.channel}** ``e o erro foi:`` **{exception}**")

    async def on_guild_join(self, guild):
        if guild.id in self.blacklist:
            await guild.leave()

    async def on_guild_remove(self, guild):
        blacklist = self.get_channel(542134573010518017)
        blacklist.send(f"{guild.id} ``ME RETIROU DO SERVIDOR LOGO PODERÁ ENTRAR NA BLACKLIST``")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.author.id not in self.blacklist:
            await self.process_commands(message)

        if message.guild is not None and message.author.id not in self.blacklist:
            await self.data.add_experience(message, 5)
            await self.data.level_up(message)

    @staticmethod
    def get_ram():
        mem = psutil.virtual_memory()
        return f"{mem.used / 0x40_000_000:.2f}/{mem.total / 0x40_000_000:.2f}GB ({mem.percent}%)"

    @staticmethod
    async def web_hook_rpg(ctx, avatar_dir, web_hook_name, msg, quest_name):
        avatar = open(avatar_dir, 'rb')
        web_hook_ = await ctx.channel.create_webhook(name=web_hook_name, avatar=avatar.read())
        web_hook = WebHook(url=web_hook_.url)
        web_hook.embed = discord.Embed(
            colour=random_color(),
            description=f"**{msg}**",
            timestamp=dt.utcnow()
        ).set_author(
            name=quest_name,
            icon_url=ctx.guild.icon_url
        ).set_thumbnail(
            url=ctx.author.avatar_url
        ).to_dict()
        web_hook.send_()
        await web_hook_.delete()


if __name__ == "__main__":

    with open("resources/auth.json") as security:
        _auth = json.loads(security.read())

    description_ashley = f"Um bot de assistencia para servidores criado por: Denky#4002\n" \
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
