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
from resources.utility import date_format
from resources.db import Database, DataInteraction
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
        self.announcements = ['VIP: VOCÊ SÓ SE TORNA VIP ENTRANDO NO MEU SERVIDOR E USANDO O COMANDO "ASH VIP"!',
                              'O COMANDO "ASH RANK" ESTÁ FINALIZADO, AGORA VOCÊ PODERÁ OLHAR SEU RANK A QUALQUER'
                              ' MOMENTO!',
                              'O COMANDO "ASH REC" SERVE PARA VOCÊ ADIQUIRIR ESTRELAS NO SEU RANK, POREM VOCÊ APENAS'
                              ' PODE DAR RECOMENDAÇÃO PARA OUTRAS PESSOAS!',
                              'PARA SUBIR DE PATENTE, VC PRECISA USAR OS MEUS COMANDOS E ADQUIRIR RANKPOINTS E'
                              ' MEDALHAS!',
                              'VOCE ADQUIRE ETHERNYAS USANDO OS COMANDOS GERAIS E OS COMANDOS DIARIOS, TAIS COMO:'
                              '"ASH DAILY REC", "ASH DAILY COIN", "ASH DAILY WORK" OU "ASH DAILY VIP"!',
                              'AGORA SEU SERVIDOR TAMBEM SE TORNA VIP, COM ISSO O DONO DO SERVIDOR PODE CADASTRAR SEUS'
                              ' PROPRIOS ANUNCIOS COMIGO. ENTRETANDO OS ANUNCIOS EXTERNOS TERÃO QUE PASSAR POR UMA'
                              ' APROVAÇÃO HUMANA POR QUESTÕES DE SEGURANÇA!',
                              'PEÇO QUE TODOS OS DONOS OU ADMINISTRADORES DOS SERVIDORES QUE TEM A ASHLEY, ATIVEM A '
                              'FUNÇÃO DO ASH NEWS, VOCÊS CONSEGUEM FAZER ISSO NO COMANDO (ASH CONFIG GUILD), POIS A '
                              'PARTIR DE AGORA TODAS NOVIDADES DO BOT VAO SER INSERIDAS NO CANAL EM DESTAQUE QUE VOCÊS'
                              ' DEFINIREM! OBRIGADO A TODOS PELA ATENÇÃO.\n ASS: DENKY (DEVELOPER MASTER)']
        self.languages = ("pt", "en")
        self.progress = "V.6 -> 82.1%"
        self.version = "API: " + str(discord.__version__) + " | BOT: 6.8.21 | PROGRESS: " + str(self.progress)
        self.server_ = "HEROKU"
        self.prefix_ = "'ash.', 'ash '"
        self.all_prefix = ['ash.', 'Ash.', 'aSh.', 'asH.', 'ASh.', 'aSH.', 'ASH.', 'AsH.',
                           'ash ', 'Ash ', 'aSh ', 'asH ', 'ASh ', 'aSH ', 'ASH ', 'AsH ']
        self.money = ['<:etherny_amarelo:691015381296480266>', '<:etherny_roxo:691014717761781851>',
                      '<:etherny_preto:691016493957251152>']
        self.github = "https://github.com/Ashley-Lab/Ashley"
        self.data_cog = {}
        self.shortcut = {'ash coin': 'ash daily coin', 'ash work': 'ash daily work', 'ash rec': 'ash daily rec',
                         'ash vip': 'ash daily vip'}
        self.vip_cog = ['commands.music.default', 'commands.admin.staff', 'commands.game.coin', 'events.on_message',
                        'commands.game.guessing', 'commands.game.jkp', 'commands.ashley.farm', 'commands.rpg.status',
                        'commands.member.pet', 'commands.member.married', 'commands.member.booket',
                        'commands.member.transfer', 'commands.rpg.inventory', 'commands.rpg.shop']
        self.titling = {"10": "Vassal", "25": "Heir", "50": "Knight", "100": "Elder", "200": "Baron", "300": "Viscount",
                        "400": "Count", "500": "Marquis", "1000": "Duke", "1500": "Grand Duke"}

        self.boxes = ['https://i.imgur.com/YcfbVH8.png', 'https://i.imgur.com/RvWFG1H.png',
                      'https://i.imgur.com/SUdzwlM.png', 'https://i.imgur.com/1EEO1YV.png']
        self.boxes_l = {'0': "Blue Common", '1': "Blue Uncommon", '2': "Pink Common", '3': "Pink Uncommon"}
        self.box = {}

        self.db: Database = Database(self)
        self.data: DataInteraction = DataInteraction(self)

        self.staff = [235937029106434048, 300592580381376513, 299273939614564363]
        self.bl_item = ['medal', 'rank_point']
        self.blacklist = list()
        self.shutdowns = list()
        self.config = config

        self.translations = self.config['translations']
        self.items = self.config['items']
        self.icons = self.config['icons']
        self.pets = self.config['pets']
        self.color = int(self.config['config']['default_embed'], 16)

        self.booster: Booster = Booster(self.items)

    async def atr_initialize(self):
        self.blacklist = dumps(await self.db.get_all_data("blacklist"))
        self.shutdowns = dumps(await self.db.get_all_data("shutdown"))

    async def check(self, ctx):
        perms = ctx.channel.permissions_for(ctx.me)
        if not perms.send_messages:
            raise commands.CommandNotFound()
        if not perms.read_messages:
            raise commands.CommandNotFound()

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
            if isinstance(ctx.author, discord.Member) and data_guild is not None:
                self.commands_used[ctx.command] += 1
                self.guilds_commands[ctx.guild.id] += 1
                self.user_commands[ctx.author.id] += 1
                update_guild = data_guild
                try:
                    update_guild['data']['commands'] += 1
                except KeyError:
                    update_guild['data']['commands'] = 1
                await self.db.update_data(data_guild, update_guild, 'guilds')
                if data_user is not None:
                    if (self.guilds_commands[ctx.guild.id] % 10) == 0:
                        for data in await self.db.get_announcements():
                            if data['data']['status']:
                                self.announcements.append(data["data"]["announce"])
                        announce = choice(self.announcements)
                        embed = discord.Embed(
                            color=0x000000,
                            description=f'<:confirmado:519896822072999937>│**ANUNCIO**\n '
                            f'```{announce}```')
                        await ctx.send(embed=embed)
                    if data_user['config']['vip']:
                        try:
                            epoch = dt.utcfromtimestamp(0)
                            cooldown = data_user["cooldown"]["daily vip"]
                            time_diff = (dt.utcnow() - epoch).total_seconds() - cooldown
                            if time_diff >= 86400:
                                data_ = await self.db.get_data("user_id", ctx.author.id, "users")
                                update_ = data_
                                if update_['config']['vip']:
                                    update_['config']['vip'] = False
                                    await self.db.update_data(data_, update_, 'users')
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
                commands_log = self.get_channel(575688812068339717)
                await commands_log.send(f"``O membro`` {ctx.author.name} ``acabou de usar o comando`` "
                                        f"**{str(ctx.command).upper()}** ``dentro da guilda`` {ctx.guild.name} ``na "
                                        f"data e hora`` **{date_format(dt.now())}**")

    async def on_command_completion(self, ctx):
        if ctx.guild is not None:
            _name = ctx.author.name.upper()
            if str(ctx.author.id) not in self.blacklist:
                await self.data.level_up(ctx)
            data = await self.db.get_data("guild_id", ctx.guild.id, "guilds")
            data_user = await self.db.get_data("user_id", ctx.author.id, "users")
            if isinstance(ctx.author, discord.Member) and data_user is not None:
                update_user = data_user
                try:
                    update_user['user']['commands'] += 1
                except KeyError:
                    update_user['user']['commands'] = 1
                if (update_user['user']['commands'] % 2) == 0:
                    chance = randint(1, 100)
                    quant = randint(1, 3)
                    if chance >= 51:
                        update_user['inventory']['rank_point'] += quant
                        await ctx.send(f"<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``{_name} GANHOU:`` "
                                       f"<:coin:519896843388452864> **{quant}** ``RANKPOINT A MAIS!``")
                if (update_user['user']['commands'] % 10) == 0:
                    guild_ = self.get_guild(update_user['guild_id'])
                    if guild_ is None:
                        await ctx.send(f"<:negate:520418505993093130>│``{_name} SUA GUILDA DE CADASTRO FOI DELETADA, "
                                       f"TENTE USAR O COMANDO`` **ASH TRANS** ``PARA MUDAR SUA GUILDA DE ORIGEM``")
                if (update_user['user']['commands'] % 10) == 0:
                    chance = randint(1, 100)
                    if chance >= 81:
                        update_user['inventory']['medal'] += 1
                        await ctx.send(f"<:rank:519896825411665930>│🎊 **PARABENS** 🎉 ``{_name} GANHOU:`` "
                                       f"<:coin:519896843388452864> **1** ``MEDALHA A MAIS!``")
                for key in self.titling.keys():
                    if update_user['user']['commands'] >= int(key):
                        update_user['user']['titling'] = self.titling[key]
                await self.db.update_data(data_user, update_user, 'users')
                if isinstance(ctx.author, discord.Member) and data is not None:
                    msg = await self.db.add_money(ctx, 6, True)
                    await ctx.send(f"``{_name} ganhou`` {msg}", delete_after=5.0)
                _chance = randint(1, 1000)
                if _chance <= 5:

                    BOX = choice(self.boxes)
                    box_type = self.boxes.index(BOX)
                    if ctx.guild.id not in self.box:
                        self.box[ctx.guild.id] = {"status": True, "quant": 1, "boxes": [box_type]}
                    else:
                        self.box[ctx.guild.id]['quant'] += 1
                        self.box[ctx.guild.id]['boxes'].append(box_type)

                    embed = discord.Embed(
                        title="**Presente Liberado**",
                        colour=self.color,
                        description=f"Esse servidor foi gratificado com uma box **{self.boxes_l[str(box_type)]}**!\n"
                                    f"Para abri-la é so usar o comando ``ash open``\n"
                                    f"**qualquer membro pode abrir uma box**\n"
                                    f"**Obs:** Essa guilda tem {self.box[ctx.guild.id]['quant']} box(es) disponiveis!")
                    embed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
                    embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                    embed.set_thumbnail(url=BOX)
                    await ctx.send(embed=embed)

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
            msg = f"{guild.id}: **{guild.name}** ``ME ADICINOU NO SERVIDOR!``"
            await entrance.send(msg)

    async def on_guild_remove(self, guild):
        if str(guild.id) not in self.blacklist:
            data = await self.db.get_data("guild_id", guild.id, "guilds")
            if data is not None:
                blacklist = self.get_channel(542134573010518017)
                msg = f"**{guild.id}:** ||{guild.name}|| ``ME RETIROU DO SERVIDOR LOGO ENTROU NA BLACKLIST``"
                await blacklist.send(msg)
                await self.ban_(guild.id, msg)
            else:
                blacklist = self.get_channel(542134573010518017)
                msg = f"**{guild.id}:** ||{guild.name}|| ``ME RETIROU DO SERVIDOR MAS NÃO TINHA FEITO O RESGISTRO, " \
                      f"ENTÃO NÃO ENTROU NA MINHA BLACKLIST!``"
                await blacklist.send(msg)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.webhook_id is not None:
            ctx = await self.get_context(message)
            await self.invoke(ctx)

        if message.guild is not None and str(message.author.id) not in self.blacklist:
            await self.data.add_experience(message, 5)
            if message.content.lower() in self.shortcut:
                msg = copy.copy(message)
                msg.content = self.shortcut[message.content.lower()]
                await self.process_commands(msg)
            else:
                await self.process_commands(message)

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
            return await ctx.send(f'<:negate:520418505993093130>│``Eu não tenho a permissão de:`` '
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

    try:
        print("\033[1;35m( >> ) | Iniciando...\033[m")
        print("\033[1;35m( > ) | Iniciando carregamento de extensões...\033[m")
        f = open("modulos.txt", "r")
        for name in f.readlines():
            if len(name.strip()) > 0:
                try:
                    if '@' not in name.strip() and '#' not in name.strip():
                        bot.load_extension(name.strip())
                        if name.strip() not in bot.vip_cog:
                            bot.data_cog[name.strip()] = "<:on_status:519896814799945728>"
                        else:
                            bot.data_cog[name.strip()] = "<:stream_status:519896814825242635>"
                        cont += 1
                    else:
                        if '#' not in name.strip():
                            print(f'\033[1;36m( ☢️ ) | Cog: \033[1;34m{name.strip()}\033[1;36m não foi carregada!\33[m')
                            bot.data_cog[name.strip()] = "<:oc_status:519896814225457152>"
                except Exception as e:
                    if '#' not in name.strip():
                        print(f"\033[1;31m( ❌ ) | Cog: \033[1;34m{name}\033[1;31m teve um [Erro] : \033[1;35m{e}\33[m")
                        bot.data_cog[name.strip()] = "<:alert_status:519896811192844288>"
                        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
                    continue
        f.close()
    except Exception as e:
        print('[Erro] : {}'.format(e))

    print(f"\033[1;35m( ✔ ) | {cont}/{len(bot.data_cog.keys())} extensões foram carregadas!\033[m")
    bot.run(_auth['_t__ashley'])
