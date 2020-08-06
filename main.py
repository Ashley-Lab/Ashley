# ARQUIVO PRINCIPAL DE INICIALIZAÇÃO DO BOT: ASHLEY PARA DISCORD.
# CRIADO POR: DANIEL AMARAL -> Denky#5960
# SEGUE ABAIXO OS IMPORTS COMPLETOS
import discord
import psutil
import json
import copy
import sys
import traceback
# SEGUE ABAIXO OS IMPORTS PARCIAIS
from random import choice, randint
from datetime import datetime as dt
from collections import Counter
from discord.ext import commands
from resources.color import random_color
from resources.webhook import WebHook
from bson.json_util import dumps
from resources.utility import date_format, patent_calculator
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
        self.commands_used = Counter()
        self.guilds_commands = Counter()
        self.guilds_messages = Counter()
        self.user_commands = Counter()
        self.blacklist = list()
        self.shutdowns = list()

        self.config = config
        self.color = int(config['config']['default_embed'], 16)
        self.announcements = config['attribute']['announcements']
        self.all_prefix = config['attribute']['all_prefix']
        self.vip_cog = config['attribute']['vip_cog']
        self.titling = config['attribute']['titling']
        self.boxes_l = config['attribute']['boxes_l']
        self.boxes = config['attribute']['boxes']
        self.money = config['attribute']['money']
        self.items = config['items']
        self.icons = config['icons']
        self.pets = config['pets']

        self.server_ = "HEROKU"
        self.progress = "V.7 -> 067.5%"
        self.github = "https://github.com/Ashley-Lab/Ashley"
        self.staff = [235937029106434048, 300592580381376513]
        self.version = "API: " + str(discord.__version__) + " | BOT: 7.6.75 | PROGRESS: " + str(self.progress)
        self.shortcut = config['attribute']['shortcut']
        self.data_cog = {}
        self.box = {}
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
        date = dt(*dt.utcnow().timetuple()[:6])
        data = {"_id": date, "reason": reason}
        await self.db.push_data(data, "shutdown")
        self.shutdowns = dumps(await self.db.get_all_data("shutdown"))

    async def ban_(self, id_, reason: str):
        date = dt(*dt.utcnow().timetuple()[:6])
        data = {"_id": id_, str(date): reason}
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
                    await ctx.send(embed=embed)

            commands_log = self.get_channel(575688812068339717)
            await commands_log.send(f"``O membro`` {ctx.author.name} ``acabou de usar o comando`` "
                                    f"**{str(ctx.command).upper()}** ``dentro da guilda`` {ctx.guild.name} ``na "
                                    f"data e hora`` **{date_format(dt.now())}**")

    async def on_command_completion(self, ctx):
        if ctx.guild is not None:
            _name = ctx.author.name.upper()

            data_guild = await self.db.get_data("guild_id", ctx.guild.id, "guilds")
            update_guild = data_guild

            data_user = await self.db.get_data("user_id", ctx.author.id, "users")
            update_user = data_user

            if isinstance(ctx.author, discord.Member) and update_user is not None:
                self.user_commands[ctx.author.id] += 1
                self.commands_used[ctx.command] += 1
                self.guilds_commands[ctx.guild.id] += 1

                if update_user['security']['status']:
                    update_user['user']['commands'] += 1

                if (update_user['user']['commands'] % 10) == 0:
                    guild_ = self.get_guild(update_user['guild_id'])
                    if guild_ is None:
                        await ctx.send(f"<:negate:721581573396496464>│``{_name} SUA GUILDA DE CADASTRO FOI DELETADA, "
                                       f"TENTE USAR O COMANDO`` **ASH TRANS** ``PARA MUDAR SUA GUILDA DE ORIGEM``")

                if (update_user['user']['commands'] % 2) == 0:
                    chance = randint(1, 100)
                    quant = randint(1, 3)
                    if chance <= 50:
                        if update_user['security']['status']:
                            update_user['inventory']['rank_point'] += quant
                            await ctx.send(f"<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``{_name} GANHOU:`` "
                                           f"<:coin:519896843388452864> **{quant}** ``RANKPOINT A MAIS!``")

                if (update_user['user']['commands'] % 10) == 0:
                    chance = randint(1, 100)
                    if chance <= 20:
                        if update_user['security']['status']:
                            update_user['inventory']['medal'] += 1
                            await ctx.send(f"<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``{_name} GANHOU:`` "
                                           f"<:coin:519896843388452864> **1** ``MEDALHA A MAIS!``")

                for key in self.titling.keys():
                    if update_user['user']['commands'] >= int(key):
                        update_user['user']['titling'] = self.titling[key]

                if str(ctx.command).lower() in ['card', 'whats', 'hot', 'guess', 'hangman', 'jkp', 'pokemon']:
                    update_user['config']['playing'] = False

                if str(ctx.command).lower() in ['box buy', 'box booster']:
                    update_user['config']['buying'] = False

                if update_user['security']['status']:
                    update_guild['data']['commands'] += 1

                update_user['security']['commands'] += 1
                try:
                    update_user['security']['commands_today'] += 1
                except KeyError:
                    update_user['security']['commands_today'] = 1

                update_user['security']['last_command'] = dt.today()
                update_user['security']['last_channel'] = ctx.channel.id

                if (update_guild['data']['commands'] // 1000) > 5 and update_guild['data']['ranking'] == "Bronze":
                    min_ = 1 + (update_guild['data']['commands'] // 1000)
                    chance = randint(min_, 200)
                    if chance < min_:
                        try:
                            update_user['inventory']['coins'] += 1000
                        except KeyError:
                            update_user['inventory']['coins'] = 1000
                        update_guild['data']['ranking'] = "Silver"
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
                        await ctx.send(f'🎊 **PARABENS** 🎉 {ctx.author} ``você upou sua guilda para o ranking`` '
                                       f'**Gold** ``e ganhou a`` **chance** ``de garimpar mais ethernyas a '
                                       f'partir de agora e `` **+2000** ``Fichas para jogar``')

                _chance = randint(1, 200)
                if _chance <= 4 and update_user['security']['status']:
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
                    await ctx.send(embed=embed)

                    role = discord.utils.find(lambda r: r.name == "</Ash_Lovers>", ctx.guild.roles)
                    msg = "<:alert:739251822920728708>│``CRIE UM CARGO CHAMADO`` **</Ash_Lovers>** ``PARA SER" \
                          " PINGADO QUANDO UM PRESENTE DROPAR.``"
                    if role is not None:
                        msg = f"<:confirmed:721581574461587496>│``Olha só gente, dropou um presente...`` " \
                              f"{role.mention}\n **Obs:** ``se voce tambem quiser ser pingado use o comando``" \
                              f" **ASH LOVER** ``ou se vc nao quiser mais ser pingado, use o comando`` " \
                              f"**ASH UNLOVER**."
                    await ctx.send(msg)

                patent = patent_calculator(update_user['inventory']['rank_point'], update_user['inventory']['medal'])
                if patent > update_user['user']['patent']:
                    update_user['user']['patent'] = patent
                    file = discord.File(f'images/patente/{patent}.png', filename="patent.png")
                    embed = discord.Embed(title='🎊 **PARABENS** 🎉\n``VOCE SUBIU DE PATENTE``', color=self.color)
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_image(url="attachment://patent.png")
                    await ctx.send(file=file, embed=embed)

                if update_user['config']['vip']:
                    try:
                        epoch = dt.utcfromtimestamp(0)
                        cooldown = update_user["cooldown"]["daily vip"]
                        time_diff = (dt.utcnow() - epoch).total_seconds() - cooldown
                        if time_diff >= 86400:
                            if update_user['config']['vip']:
                                update_user['config']['vip'] = False
                                if ctx.guild.id == 519894833783898112:
                                    await ctx.send(f'<:negate:721581573396496464>│{ctx.author.mention} '
                                                   f'``INFELIZMENTE VOCÊ ACABOU DE PERDER SEU VIP DIARIO!``')
                                    await ctx.send("<:alert:739251822920728708>│``APROVEITE QUE"
                                                   " VC ESTA AQUI E USE O COMANDO`` **ASH VIP**")
                                else:
                                    await ctx.send(f'<:negate:721581573396496464>│{ctx.author.mention} ``INFELIZMENTE'
                                                   f' VOCÊ ACABOU DE PERDER SEU VIP DIARIO!``\n **Vá no meu servidor'
                                                   f' para receber seu proximo dia de vip!**')
                            else:
                                if (self.guilds_commands[ctx.guild.id] % 10) == 0:
                                    if ctx.guild.id == 519894833783898112:
                                        await ctx.send("<:alert:739251822920728708>│``APROVEITE QUE"
                                                       " VC ESTA AQUI E USE O COMANDO`` **ASH VIP**")
                                    else:
                                        await ctx.send("<:alert:739251822920728708>│``Você pode ganhar "
                                                       "VIP DIARIO ENTRANDO NO MEU SERVIDOR!``\n **Saiba mais usando "
                                                       "ASH INVITE**")
                    except KeyError:
                        if (self.guilds_commands[ctx.guild.id] % 10) == 0:
                            if ctx.guild.id == 519894833783898112:
                                await ctx.send("<:alert:739251822920728708>│``APROVEITE QUE VC ESTA"
                                               " AQUI E USE O COMANDO`` **ASH VIP**")
                            else:
                                await ctx.send("<:alert:739251822920728708>│``Agora você pode ganhar "
                                               "VIP DIARIO ENTRANDO NO MEU SERVIDOR!``\n **Saiba mais usando ASH "
                                               "INVITE**")

                await self.db.update_data(data_user, update_user, 'users')
                await self.db.update_data(data_guild, update_guild, 'guilds')

                if isinstance(ctx.author, discord.Member) and data_user is not None:
                    msg = await self.db.add_money(ctx, 6, True)
                    await ctx.send(f"``Por usar um comando, {_name} tambem ganhou`` {msg}", delete_after=5.0)

                await self.data.level_up(ctx)

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
        else:
            entrance = self.get_channel(619899848082063372)
            msg = f"> **{guild.id}:** {guild.name} ``ME ADICINOU NO SERVIDOR!``"
            await entrance.send(msg)

    async def on_guild_remove(self, guild):
        if str(guild.id) not in self.blacklist:
            data = await self.db.get_data("guild_id", guild.id, "guilds")
            if data is not None:
                blacklist = self.get_channel(542134573010518017)
                msg = f"> **{guild.id}:** {guild.name} ``ME RETIROU DO SERVIDOR LOGO ENTROU NA BLACKLIST``"
                await blacklist.send(msg)
                await self.ban_(guild.id, msg)
            else:
                blacklist = self.get_channel(542134573010518017)
                msg = f"> **{guild.id}:** {guild.name} ``ME RETIROU DO SERVIDOR MAS NÃO TINHA FEITO O RESGISTRO, " \
                      f"ENTÃO NÃO ENTROU NA MINHA BLACKLIST!``"
                await blacklist.send(msg)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        ctx = await self.get_context(message)
        perms = ctx.channel.permissions_for(ctx.me)
        if not perms.send_messages or not perms.read_messages:
            return

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
                                await message.guild.owner.send(embed=embed)
                            except discord.Forbidden:
                                pass

            if str(ctx.command) in ['channel']:
                run_command = True

            if run_command:
                if message.content.lower() in self.shortcut:
                    msg = copy.copy(message)
                    msg.content = self.shortcut[message.content.lower()]
                    await self.process_commands(msg)
                else:
                    await self.process_commands(message)
            else:
                if ctx.command is not None:
                    await message.channel.send("<:alert:739251822920728708>|``NAO POSSO EXECUTAR COMANDOS NESSE"
                                               " CANAL!``")

    @staticmethod
    def get_ram():
        mem = psutil.virtual_memory()
        return f"{mem.used / 0x40_000_000:.2f}/{mem.total / 0x40_000_000:.2f}GB ({mem.percent}%)"

    @staticmethod
    async def web_hook_rpg(ctx, avatar_dir, web_hook_name, msg, quest_name):

        perms = ctx.channel.permissions_for(ctx.me)
        if not perms.manage_webhooks:
            if not perms.send_messages:
                return
            return await ctx.send(f'<:negate:721581573396496464>│``Eu não tenho a permissão de:`` '
                                  f'**Gerenciar Webhooks**')

        avatar = open(avatar_dir, 'rb')
        web_hook_ = await ctx.channel.create_webhook(name=web_hook_name, avatar=avatar.read())
        if 'a_' in web_hook_.avatar:
            format_1 = '.gif'
        else:
            format_1 = '.webp'
        web_hook = WebHook(url=web_hook_.url)
        content = f"{quest_name} do {ctx.author.name} disse:\n```{msg}```"
        web_hook.embed = discord.Embed(
            colour=random_color(),
            description=f"{content if quest_name != 'Ashley' else msg}",
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

    with open("data/auth.json") as auth:
        _auth = json.loads(auth.read())

    description_ashley = f"Um bot de assistencia para servidores criado por: Denky#5960\n" \
                         f"**Adicione para seu servidor:**: {config['config']['default_link']}\n" \
                         f"**Servidor de Origem**: {config['config']['default_invite']}\n"

    prefix = ['ash.', 'Ash.', 'aSh.', 'asH.', 'ASh.', 'aSH.', 'ASH.', 'AsH.',
              'ash ', 'Ash ', 'aSh ', 'asH ', 'ASh ', 'aSH ', 'ASH ', 'AsH ']

    bot = Ashley(command_prefix=prefix, description=description_ashley, pm_help=True, case_insensitive=True)
    bot.remove_command('help')
    cont = 0
    emojis = {"ON": "``🟢``", "IDLE": "``🟡``", "OFF": "``🔴``", "VIP": "``🟣``"}

    print("\033[1;35m( >> ) | Iniciando...\033[m\n")
    print("\033[1;35m( >> ) | Iniciando carregamento de extensões...\033[m")
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
