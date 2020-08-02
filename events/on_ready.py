import discord
import asyncio

import time as date
from itertools import cycle
from discord.ext import commands
from random import choice, randint
from datetime import datetime as dt
from resources.utility import date_format
from resources.verify_cooldown import verify_cooldown
from resources.structure import user_data_structure, guild_data_structure

cor = {
    'clear': '\033[m',
    'cian': '\033[1;36m',
    'roxo': '\033[1;35m',
    'azul': '\033[1;34m',
    'amar': '\033[1;33m',
    'verd': '\033[1;32m',
    'verm': '\033[1;31m',
    'pers': '\033[1;35;47m'
}

opt = {
    'before_options': '-nostdin',
    'options': '-vn -loglevel quiet'
}


class OnReady(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.time_ready = None
        self.color = self.bot.color
        self.url = 'https://www.twitch.tv/d3nkyt0'
        self.time = [0, 1]
        self.details = ['Yu-gi-oh!', 'RPG', 'Pokemon']
        self.state = [discord.Status.online, discord.Status.idle, discord.Status.dnd]
        self.status = ['minha equipe nos pensamentos!', '😢 + 💸 = 😍 & 🍫',
                       'meus cabelos ao vento!', '😢 + 💸 = 😍 & 🍫',
                       'minha amiga no buraco!', '😢 + 💸 = 😍 & 🍫',
                       'meu charme em você!', '😢 + 💸 = 😍 & 🍫',
                       'novidades no sistema!', '😢 + 💸 = 😍 & 🍫',
                       'minha roupa na sua cara!', '😢 + 💸 = 😍 & 🍫',
                       'meu feitiço na sua vida!', '😢 + 💸 = 😍 & 🍫']

    async def security_macro(self):
        while True:
            if await verify_cooldown(self.bot, "security_macro", 300):
                date_ = date.localtime()
                data_ = date_format(dt.now())

                all_data = await self.bot.db.get_all_data("users")
                for data in all_data:
                    update = data

                    update['security']['last_verify'] = dt.today()
                    update['security']['blocked'] = False
                    last_verify = update['security']['last_verify']
                    last_command = update['security']['last_command']

                    if last_command is None:
                        await self.bot.db.update_data(data, update, "users")
                        continue

                    if not update['security']['status']:
                        continue

                    if update['security']['commands_today'] > 900:
                        try:
                            update['security']['status'] = not update['security']['status']
                            update['security']['blocked'] = not update['security']['blocked']
                        except KeyError:
                            update['security']['status'] = False
                            update['security']['blocked'] = True

                        update['security']['last_blocked'] = dt.today()

                        try:
                            update['security']['strikes_to_ban'] += 1
                        except KeyError:
                            update['security']['strikes_to_ban'] = 1

                        channel_ = self.bot.get_channel(737467830571761786)
                        await channel_.send(f'```O USUARIO {data["user_id"]} ESTAVA POSSIVELMENTE USANDO MACRO E FOI '
                                            f'BLOQUEADO\nNa Data e Hora: {data_}```')
                        try:
                            if update['security']['last_channel'] is not None:
                                channel_ = self.bot.get_channel(update['security']['last_channel'])
                                await channel_.send(f'<a:red:525032764211200002>│``VOCE FOI BLOQUEADO POR 72 HORAS '
                                                    f'POIS EXTRAPOLOU OS LIMITES HOJE``<a:red:525032764211200002>'
                                                    f'**OBS: VOCE AINDA PODE USAR O BOT, POREM PERDEU OS PRIVILEGIOS '
                                                    f'DE GANHAR OS ITENS** <a:red:525032764211200002>'
                                                    f'<a:red:525032764211200002> ``ESSE BLOQUEIO FOI MAIS RIGIDO``'
                                                    f'<a:red:525032764211200002><a:red:525032764211200002>')
                        except KeyError:
                            pass

                    last_verify = date.mktime(last_verify.timetuple())
                    last_command = date.mktime(last_command.timetuple())
                    minutes = int(int(last_verify - last_command) / 60)

                    if minutes < 5 and update['security']['commands'] > 50:

                        update['security']['strikes'] += 1
                        update['security']['commands'] = 0
                        channel_ = self.bot.get_channel(737467830571761786)
                        await channel_.send(f'```O USUARIO {data["user_id"]} FOI DETECTADO POSSIVELMENTE USANDO MACRO\n'
                                            f'Na Data e Hora: {data_}```')
                        try:
                            if update['security']['strikes'] < 6:
                                if update['security']['last_channel'] is not None:
                                    channel_ = self.bot.get_channel(update['security']['last_channel'])
                                    await channel_.send(f'<a:blue:525032762256785409>│``EI TENHA CALMA VOCE TA '
                                                        f'USANDO COMANDOS RAPIDO DEMAIS, SE CONTINUAR ASSIM VAI SER '
                                                        f'BLOQUEADO ATE AS 0 HORAS DO DIA DE HOJE.`` '
                                                        f'<a:blue:525032762256785409>'
                                                        f'**AVISO {update["security"]["strikes"]}/5**')
                        except KeyError:
                            pass
                    else:
                        update['security']['commands'] = 0

                    if update['security']['strikes'] == 6:
                        update['security']['status'] = not update['security']['status']
                        channel_ = self.bot.get_channel(737467830571761786)
                        await channel_.send(f'```O USUARIO {data["user_id"]} ESTAVA POSSIVELMENTE USANDO MACRO E FOI '
                                            f'BLOQUEADO\nNa Data e Hora: {data_}```')

                        try:
                            if update['security']['last_channel'] is not None:
                                channel_ = self.bot.get_channel(update['security']['last_channel'])
                                await channel_.send(f'<a:blue:525032762256785409>│``VOCE FOI BLOQUEADO ATE AS 0 '
                                                    f'HORAS DO DIA DE HOJE..`` <a:blue:525032762256785409>'
                                                    f'**OBS: VOCE AINDA PODE USAR O BOT, POREM PERDEU OS PRIVILEGIOS '
                                                    f'DE GANHAR OS ITENS**')
                        except KeyError:
                            pass

                    await self.bot.db.update_data(data, update, "users")

                # existe uma diferença de hora de +3 para o servidor da ashley
                if date_[3] == 3 and date_[4] <= 30:
                    all_data = await self.bot.db.get_all_data("users")
                    for data in all_data:
                        update = data

                        try:
                            last_verify = date.mktime(update['security']['last_verify'].timetuple())
                            last_blocked = date.mktime(update['security']['last_blocked'].timetuple())
                            minutes = int(int(last_verify - last_blocked) / 60)
                            if minutes > 4320:
                                update['security']['blocked'] = False
                        except KeyError:
                            pass
                        except AttributeError:
                            pass

                        if not update['security']['blocked']:
                            update['security']['commands'] = 0
                            update['security']['commands_today'] = 0
                            update['security']['strikes'] = 0
                            update['security']['last_verify'] = dt.today()
                            update['security']['status'] = True
                            await self.bot.db.update_data(data, update, "users")

            await asyncio.sleep(60)

    async def draw_member(self):
        while True:
            if await verify_cooldown(self.bot, "draw_member", 7200):
                for guild in self.bot.guilds:
                    data = await self.bot.db.get_data("guild_id", guild.id, "guilds")
                    if data is not None and len(guild.members) >= 50 and data['data']['accounts'] >= 10:
                        if data['bot_config']['ash_draw']:
                            channel__ = self.bot.get_channel(data['bot_config']['ash_draw_id'])
                            if channel__ is None:
                                continue

                            draw_member = choice([member for member in guild.members if not member.bot])
                            try:
                                member = discord.utils.get(guild.members, name="{}".format(draw_member.name))
                            except TypeError:
                                continue
                            data_member = await self.bot.db.get_data("user_id", member.id, "users")
                            update_member = data_member
                            if data_member is None:
                                await channel__.send(f"<:alert:739251822920728708>│{member.name} ``FOI SORTEADO"
                                                     f" POREM NÃO TINHA REGISTRO!`` **USE ASH REGISTER**")
                                continue
                            coins = randint(10, 15)
                            embed = discord.Embed(
                                title="``Fiz o sorteio de um membro``",
                                colour=self.color,
                                description="Membro sorteado foi **{}**\n <a:palmas:520418512011788309>│"
                                            "``Parabens você acaba de ganhar`` **{}** "
                                            "``coins!!``".format(member.mention, coins))
                            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                            embed.set_thumbnail(url=member.avatar_url)
                            await channel__.send(embed=embed)
                            update_member['inventory']['coins'] += coins
                            await self.bot.db.update_data(data_member, update_member, 'users')
            await asyncio.sleep(300)

    async def draw_gift(self):
        while True:
            if await verify_cooldown(self.bot, "draw_gift", 17280):
                for guild in self.bot.guilds:
                    data = await self.bot.db.get_data("guild_id", guild.id, "guilds")
                    if data is not None and len(guild.members) >= 50 and data['data']['accounts'] >= 10:
                        if data['bot_config']['ash_draw']:
                            channel__ = self.bot.get_channel(data['bot_config']['ash_draw_id'])
                            if channel__ is None:
                                continue

                            BOX = choice(self.bot.boxes)
                            boxt = self.bot.boxes.index(BOX)
                            if guild.id not in self.bot.box:
                                self.bot.box[guild.id] = {"quant": 1, "boxes": [boxt]}
                            else:
                                self.bot.box[guild.id]['quant'] += 1
                                self.bot.box[guild.id]['boxes'].append(boxt)

                            embed = discord.Embed(
                                title="**Presente Liberado**",
                                colour=self.color,
                                description=f"Esse servidor foi gratificado com um presente "
                                            f"**{self.bot.boxes_l[str(boxt)]}**!\n"
                                            f"Para abri-lo é so usar o comando ``ash open``\n"
                                            f"**qualquer membro pode abrir um presente**\n"
                                            f"**Obs:** Essa guilda tem {self.bot.box[guild.id]['quant']} presente(s)"
                                            f"disponiveis!")
                            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                            embed.set_thumbnail(url=BOX)
                            await channel__.send(embed=embed)
            await asyncio.sleep(300)

    async def change_status(self):
        status = cycle(self.status)
        details = cycle(self.details)
        state = cycle(self.state)
        time = cycle(self.time)
        while True:
            if await verify_cooldown(self.bot, "change_status", 60):
                current_time = next(time)
                if current_time == 0:
                    current_status = next(status)
                    current_details = next(details)
                    if not self.bot.is_closed():
                        await self.bot.change_presence(activity=discord.Streaming(name=current_status,
                                                                                  url=self.url,
                                                                                  details=current_details))
                else:
                    current_status = next(status)
                    current_state = next(state)
                    if not self.bot.is_closed():
                        await self.bot.change_presence(activity=discord.Game(name=current_status),
                                                       status=current_state)
            await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):

        owner = str(self.bot.get_user(self.bot.owner_id))
        ver_ = self.bot.version
        id_bot = str(self.bot.user.id)
        name = str(self.bot.user)
        shards = self.bot.shard_count
        log = 'LOGADO COM SUCESSO'
        servs = str(len(self.bot.guilds))
        late = int(self.bot.latency * 1000)
        emoji = len(self.bot.emojis)
        users = len(self.bot.users)
        self.time_ready = dt.utcnow()
        time = self.time_ready - self.bot.start_time

        # inicializar os atributos awaits
        print("\n\033[1;35m( >> ) | Iniciando atributos assincronos...\033[m")
        await self.bot.atr_initialize()
        print("\033[1;35m( ✔ ) | Atributos assincronos inicializados com sucesso!\033[m\n")

        print("\n\033[1;35m( >> ) | Iniciando reestruturação de variaveis internas...\033[m")
        all_data = await self.bot.db.get_all_data("users")
        for data in all_data:
            update = data
            update['config']['playing'] = False
            update['config']['battle'] = False
            update['config']['buying'] = False
            update['user']['marrieding'] = False
            await self.bot.db.update_data(data, update, "users")
        print('\033[1;32m( 🔶 ) | Reestruturação da variavel \033[1;34mPLAYING\033[1;32m foi feita sucesso!\33[m')
        print('\033[1;32m( 🔶 ) | Reestruturação da variavel \033[1;34mBATTLE\033[1;32m foi feita sucesso!\33[m')
        print('\033[1;32m( 🔶 ) | Reestruturação da variavel \033[1;34mTOURNAMENT\033[1;32m foi feita sucesso!\33[m')
        print('\033[1;32m( 🔶 ) | Reestruturação da variavel \033[1;34mMARRIEDING\033[1;32m foi feita sucesso!\33[m')
        print("\033[1;35m( ✔ ) | Reestruturação de variaveis internas Finalizadas!\033[m\n")

        print("\n\033[1;35m( >> ) | Iniciando reestruturação do banco de dados...\033[m")
        all_data = await self.bot.db.get_all_data("users")
        for data in all_data:
            update = data
            for key in user_data_structure.keys():
                if key in data:
                    try:
                        for k in user_data_structure[key].keys():
                            if k not in data[key]:
                                update[key][k] = user_data_structure[key][k]
                    except AttributeError:
                        pass
                else:
                    update[key] = user_data_structure[key]
            await self.bot.db.update_data(data, update, "users")
        print('\033[1;32m( 🔶 ) | Reestruturação dos \033[1;34mUSUARIOS\033[1;32m foi feita sucesso!\33[m')
        all_data = await self.bot.db.get_all_data("guilds")
        for data in all_data:
            update = data
            for key in guild_data_structure.keys():
                if key in data:
                    try:
                        for k in guild_data_structure[key].keys():
                            if k not in data[key]:
                                update[key][k] = guild_data_structure[key][k]
                    except AttributeError:
                        pass
                else:
                    update[key] = guild_data_structure[key]
            await self.bot.db.update_data(data, update, "guilds")
        print('\033[1;32m( 🔶 ) | Reestruturação dos \033[1;34mSERVIDORES\033[1;32m foi feita sucesso!\33[m')
        print("\033[1;35m( ✔ ) | Reestruturação do banco de dados finalizada!\033[m\n")

        print("\n\033[1;35m( >> ) | Iniciando carregamento dos loops internos...\033[m")
        self.bot.loop.create_task(self.change_status())
        print('\033[1;32m( 🔶 ) | O loop \033[1;34mSTATUS_DA_ASHLEY\033[1;32m foi carregado com sucesso!\33[m')
        self.bot.loop.create_task(self.draw_member())
        print('\033[1;32m( 🔶 ) | O loop \033[1;34mDRAW_MEMBERS\033[1;32m foi carregado com sucesso!\33[m')
        self.bot.loop.create_task(self.draw_gift())
        print('\033[1;32m( 🔶 ) | O loop \033[1;34mDRAW_GIFT\033[1;32m foi carregado com sucesso!\33[m')
        self.bot.loop.create_task(self.security_macro())
        print('\033[1;32m( 🔶 ) | O loop \033[1;34mSECURITY_MACRO\033[1;32m foi carregado com sucesso!\33[m')
        print("\033[1;35m( ✔ ) | Loops internos carregados com sucesso!\033[m\n")

        print(cor['cian'], '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬', cor['clear'])
        print(cor['roxo'], log.center(70), cor['clear'])
        print(cor['azul'], '▍ Owner    ⠿', cor['clear'], cor['verd'], '{}'.format(str(owner).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ Versão   ⠿', cor['clear'], cor['amar'], '{}'.format(str(ver_).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ App      ⠿', cor['clear'], cor['amar'], '{}'.format(str(name).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ ID       ⠿', cor['clear'], cor['amar'], '{}'.format(str(id_bot).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ Shards   ⠿', cor['clear'], cor['amar'], '{}'.format(str(shards).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ Servers  ⠿', cor['clear'], cor['amar'], '{}'.format(str(servs).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ Latência ⠿', cor['clear'], cor['verm'], '{}ms'.format(str(late).rjust(48)), cor['clear'])
        print(cor['azul'], '▍ Emojis   ⠿', cor['clear'], cor['amar'], '{}'.format(str(emoji).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ Users    ⠿', cor['clear'], cor['amar'], '{}'.format(str(users).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ Uptime   ⠿', cor['clear'], cor['amar'], '{}s'.format(str(time).rjust(49)), cor['clear'])
        print(cor['cian'], '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬', cor['clear'])


def setup(bot):
    bot.add_cog(OnReady(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mON_READY\033[1;33m foi carregado com sucesso!\33[m')
