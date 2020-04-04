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
        self.task_chance = self.bot.loop.create_task(self.change_status())
        self.url = 'https://www.twitch.tv/d3nkyt0'
        self.details = ['Yu-gi-oh!', 'RPG', 'Magic', 'Ashley Project']
        self.state = ['online', 'idle', 'dnd']
        self.status = ['meu criador nos pensamentos!', '😢 + 💸 = 😍 & 🍫', 'meus cabelos ao vento!', '😢 + 💸 = 😍 & 🍫',
                       'minha amiga no buraco!', '😢 + 💸 = 😍 & 🍫', 'meu charme em você!', '😢 + 💸 = 😍 & 🍫',
                       'novidades no sistema!', '😢 + 💸 = 😍 & 🍫', 'minha roupa na sua cara!', '😢 + 💸 = 😍 & 🍫',
                       'meu feitiço na sua vida!', '😢 + 💸 = 😍 & 🍫']

    async def change_status(self):
        await self.bot.wait_until_ready()
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

        self.bot.loop.create_task(self.remove_role_zdd())


def setup(bot):
    bot.add_cog(OnReady(bot))
    print('\033[1;33m( * ) | O evento \033[1;34mON_READY\033[1;33m foi carregado com sucesso!\33[m')
