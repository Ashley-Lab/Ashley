import io
import discord

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
        self.task_temporizer_draw_member = self.bot.loop.create_task(self.draw_member_in_server())
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

    async def draw_member_in_server(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            list_ = list()
            for guild in self.bot.guilds:
                data = self.bot.db.get_data("guild_id", guild.id, "guilds")
                if data is not None:
                    if data['bot_config']['ash_news']:
                        list_.append(1)
            premium = list()
            for c in range(len(self.bot.guilds)):
                min__ = localtime()
                if str(min__[4]) in ["00", "10", "20", "30", "40", "50"]:
                    for guild in self.bot.guilds:
                        data = self.bot.db.get_data("guild_id", guild.id, "guilds")
                        if data is not None:
                            if data['bot_config']['ash_news']:
                                channel__ = self.bot.get_channel(data['bot_config']['ash_news_id'])
                                if channel__ is None:
                                    continue
                                if len(guild.members) < 50:
                                    continue
                                draw_member = choice(list(guild.members))
                                member = discord.utils.get(guild.members, name="{}".format(draw_member.name))
                                data_member = self.bot.db.get_data("user_id", member.id, "users")
                                update_member = data_member
                                if data_member is None:
                                    await channel__.send(f"<:negate:520418505993093130>│{member.name} ``FOI SORTEADO"
                                                         f" POREM NÃO TINHA REGISTRO!`` **USE ASH REGISTER**")
                                    premium.append(c)
                                    continue
                                coins = randint(2, 10)
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
                                premium.append(c)
                        await sleep(60)
                await sleep(60)
            if len(premium) == len(list_):
                time = 3600
            else:
                time = 10
            await sleep(time)

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


def setup(bot):
    bot.add_cog(OnReady(bot))
    print('\033[1;33m( * ) | O evento \033[1;34mON_READY\033[1;33m foi carregado com sucesso!\33[m')
