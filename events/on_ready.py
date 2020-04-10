import io
import discord
import time as date

from asyncio import sleep
from random import choice, randint
from itertools import cycle
from time import localtime
from datetime import datetime as dt
from discord.ext import commands

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


class OnReady(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.reflect = self.bot.config['reflect']['list']
        self.time_ready = None
        self.color = self.bot.color
        self.url = 'https://www.twitch.tv/d3nkyt0'
        self.details = ['Yu-gi-oh!', 'RPG', 'Magic', 'Pokemon']
        self.state = [discord.Status.online, discord.Status.idle, discord.Status.dnd]
        self.status = ['minha equipe nos pensamentos!', '😢 + 💸 = 😍 & 🍫',
                       'meus cabelos ao vento!', '😢 + 💸 = 😍 & 🍫',
                       'minha amiga no buraco!', '😢 + 💸 = 😍 & 🍫',
                       'meu charme em você!', '😢 + 💸 = 😍 & 🍫',
                       'novidades no sistema!', '😢 + 💸 = 😍 & 🍫',
                       'minha roupa na sua cara!', '😢 + 💸 = 😍 & 🍫',
                       'meu feitiço na sua vida!', '😢 + 💸 = 😍 & 🍫']

    async def draw_member(self):
        while not self.bot.is_closed():
            list_ = list()
            for guild in self.bot.guilds:
                data = self.bot.db.get_data("guild_id", guild.id, "guilds")
                if data is not None:
                    if data['bot_config']['ash_draw']:
                        list_.append(1)
            premium = list()
            all_data = self.bot.db.get_all_data("users")
            for c in range(len(self.bot.guilds)):
                min__ = localtime()
                if min__[4] in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]:
                    for guild in self.bot.guilds:
                        data = self.bot.db.get_data("guild_id", guild.id, "guilds")
                        member_ = 0
                        for data in all_data:
                            if data['guild_id'] == guild.id:
                                member_ += 1
                        if data is not None and len(guild.members) >= 50 and member_ >= 10:
                            if data['bot_config']['ash_draw']:
                                channel__ = self.bot.get_channel(data['bot_config']['ash_draw_id'])
                                if channel__ is None:
                                    continue
                                draw_member = choice(list(guild.members))
                                member = discord.utils.get(guild.members, name="{}".format(draw_member.name))
                                data_member = self.bot.db.get_data("user_id", member.id, "users")
                                update_member = data_member
                                if data_member is None:
                                    await channel__.send(f"<:negate:520418505993093130>│{member.name} ``FOI SORTEADO"
                                                         f" POREM NÃO TINHA REGISTRO!`` **USE ASH REGISTER**")
                                    premium.append(1)
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
                                self.bot.db.update_data(data_member, update_member, 'users')
                                premium.append(1)
                await sleep(30)
            print(f'Lista Premium{premium}, Lista Comum {list_}')
            if len(premium) == len(list_):
                await sleep(3600)
            else:
                await sleep(60)

    async def change_status(self):
        status = cycle(self.status)
        details = cycle(self.details)
        state = cycle(self.state)
        while not self.bot.is_closed():
            current_status = next(status)
            current_details = next(details)
            await self.bot.change_presence(activity=discord.Streaming(name=current_status, url=self.url,
                                                                      details=current_details))
            await sleep(10)
            current_status = next(status)
            current_state = next(state)
            await self.bot.change_presence(activity=discord.Game(name=current_status), status=current_state)
            await sleep(10)

    async def remove_role_zdd(self):
        while not self.bot.is_closed():
            date_ = date.localtime()
            # existe uma diferença de hora de +3 para o servidor da ashley
            if date_[3] == 3 and 0 >= date_[4] >= 5:
                guild = self.bot.get_guild(643936732236087306)
                for member in guild.members:
                    member_ = guild.get_member(member.id)
                    for role in member_.roles:
                        if 'Membro Ativo' == role.name:
                            role = discord.utils.find(lambda r: r.name == 'Membro Ativo', guild.roles)
                            await member_.remove_roles(role)
            if date_[3] == 3:
                await sleep(60)
            else:
                await sleep(3600)

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
        chann = len(self.bot.private_channels)

        all_data = self.bot.db.get_all_data("users")
        for data in all_data:
            update = data
            update['config']['playing'] = False
            update['config']['battle'] = False
            update['config']['tournament'] = False
            update['user']['marrieding'] = False
            rpg = {"Name": None, "Level": 1, "XP": 0, "Status": {"con": 5, "prec": 5, "agi": 5, "atk": 5, "luk": 0,
                   "pdh": 0}, "Class": 'Default', "itens": list(), "img": None}
            update['rpg'] = rpg
            del update['status']
            del update['box']
            self.bot.db.update_data(data, update, "users")

        self.time_ready = dt.utcnow()
        time = self.time_ready - self.bot.start_time

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
        print(cor['azul'], '▍ PrivateC ⠿', cor['clear'], cor['amar'], '{}'.format(str(chann).rjust(50)), cor['clear'])
        print(cor['azul'], '▍ Uptime   ⠿', cor['clear'], cor['amar'], '{}s'.format(str(time).rjust(49)), cor['clear'])
        print(cor['cian'], '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬', cor['clear'])

        print("\033[1;35m( * ) | Iniciando carregamento dos loops internos...\033[m")
        self.bot.loop.create_task(self.remove_role_zdd())
        print('\033[1;32m( * ) | O loop \033[1;34mZONA_DE_DUELOS\033[1;32m foi carregado com sucesso!\33[m')
        self.bot.loop.create_task(self.change_status())
        print('\033[1;32m( * ) | O loop \033[1;34mSTATUS_DA_ASHLEY\033[1;32m foi carregado com sucesso!\33[m')
        self.bot.loop.create_task(self.draw_member())
        print('\033[1;32m( * ) | O loop \033[1;34mDRAW_MEMBERS\033[1;32m foi carregado com sucesso!\33[m')


def setup(bot):
    bot.add_cog(OnReady(bot))
    print('\033[1;33m( * ) | O evento \033[1;34mON_READY\033[1;33m foi carregado com sucesso!\33[m')
