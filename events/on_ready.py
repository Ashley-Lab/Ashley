import discord
import json

from asyncio import sleep
from random import choice, randint
from itertools import cycle
from time import localtime
from datetime import datetime as dt
from resources.ia_list import reflita

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class OnReady(object):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.time_ready = None
        self.task_chance = self.bot.loop.create_task(self.change_status())
        self.task_temporizer_one = self.bot.loop.create_task(self.temporizer_channel_one())
        self.task_temporizer_two = self.bot.loop.create_task(self.temporizer_channel_two())
        self.url = 'https://www.twitch.tv/filizardproject'
        self.details = ['Yu-gi-oh!', 'RPG', 'Magic', 'Ashley Project']
        self.state = ['online', 'idle', 'dnd']
        self.status = ['meu criador nos pensamentos!', 'meus cabelos ao vento!', 'minha amiga no buraco!',
                       'meu charme em você!', 'novidades no sistema!', 'minha ajuda na sua mente',
                       'meus prefixos: {}'.format(self.bot.prefix_), 'meu servidor: {}'.format(self.bot.server_),
                       'meu comando de ajuda: help/ajuda', '😢 + 💸 = 😍 & 🍫']

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
            await sleep(60)
            current_status = next(status)
            current_state = next(state)
            await self.bot.change_presence(activity=discord.Game(name=current_status), status=current_state)
            await sleep(60)

    async def temporizer_channel_one(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for c in range(len(self.bot.guilds)):
                min_ = localtime()
                if str(min_[4]) in ["05", "15", "25", "35", "45", "55"]:
                    for guild in self.bot.guilds:
                        data = self.bot.db.get_data("guild_id", guild.id, "guilds")
                        if data is not None:
                            if data['bot_config']['ash_news']:
                                channel_ = self.bot.get_channel(data['bot_config']['ash_news_id'])
                                if channel_ is None:
                                    continue
                                message = choice(reflita)
                                await channel_.send("```{}```".format(message))
                        await sleep(10)
                await sleep(10)
            await sleep(3600)

    async def temporizer_channel_two(self):
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
                if str(min__[4]) in ["00", "10", "20", "30", "40", "50", "60"]:
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
                                                         f" POREM NÃO TINHA REGISTRO, LOGO NÃO HOUVE PREMIAÇÃO``")
                                    premium.append(c)
                                    continue
                                coins = randint(2, 10)
                                embed = discord.Embed(
                                    title="``Fiz o sorteio de um membro``",
                                    colour=color,
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
                        await sleep(10)
                await sleep(10)
            if len(premium) == len(list_):
                time = 3600
            else:
                time = 10
            await sleep(time)

    async def on_ready(self):
        all_data = self.bot.db.get_all_data("users")
        for data in all_data:
            update = data
            update['config']['playing'] = False
            update['config']['battle'] = False
            update['config']['tournament'] = False
            # update['inventory']['coins'] = 50
            try:
                update['user']['marrieding'] = False
            except KeyError:
                pass
            self.bot.db.update_data(data, update, "users")
        self.bot.db.delete_channels()
        self.time_ready = dt.utcnow()
        time_now = self.time_ready - self.bot.start_time

        print("\033[1;30m=================================\33[m")
        print('\033[1;32mNome: \033[1;34m%s\033[1;32m foi carregada com sucesso!\33[m' % self.bot.user.name)
        print('\033[1;32mID: \033[1;34m%s\033[1;32m foi definido com sucesso!\33[m' % self.bot.user.id)
        print('\033[1;32mOn line em : \033[1;34m{}\033[1;32m Servers!\33[m'.format(str(len(self.bot.guilds))))
        print(f'\033[1;32mBot Version: \033[1;34m{self.bot.version}\033[1;32m by Denky#4002!\33[m')
        print(f'\033[1;32mPronto em: \033[1;34m{time_now}\033[1;32m segundos!\33[m')
        print("\033[1;30m=================================\33[m")


def setup(bot):
    bot.add_cog(OnReady(bot))
    print('\033[1;32mO evento \033[1;34mON_READY\033[1;32m foi carregado com sucesso!\33[m')
