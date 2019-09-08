import json
import time
import discord

from random import choice
from asyncio import TimeoutError
from discord.ext import commands
from resources.utility import get_response
from resources.ia_list import *

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())


class SystemMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = {}
        self.ping_test = {}
        self.letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z')

    async def send_message(self, message):
        try:
            if self.msg[message.author.id] is None:
                return
        except KeyError:
            self.msg[message.author.id] = "não entendi..."
        pet_n = choice(list(self.bot.pets.keys()))
        pet = self.bot.pets[pet_n]
        if pet['colour'][0] is True:
            pet_c = choice(pet['colour'][2])
            indice = pet['colour'][2].index(pet_c)
            mask = choice(self.letters[:pet['mask'][indice]])
            link_ = f'images/pet/{pet_n}/{pet_c}/mask_{mask}.png'
        else:
            mask = choice(self.letters[:pet['mask'][0]])
            link_ = f'images/pet/{pet_n}/mask_{mask}.png'
        await self.bot.web_hook_rpg(message, link_, pet_n, self.msg[message.author.id], 'Pet')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and str(message.author.id) not in self.bot.blacklist:
            data_guild = self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            if data_guild is not None:
                data = self.bot.db.get_channel_data(message.channel.id)
                if data['channel_id'] == message.channel.id and data['channel_state'] == 0:
                    if 'denky' in message.content.lower() and data_guild['ia_config']['auto_msg']:
                        if message.author.id != self.bot.owner_id and "pet " not in message.content.lower():
                            for c in range(0, len(denky_r)):
                                if denky_r[c] in message.content:
                                    return await message.channel.send('**Ei,** {}**! Eu to vendo você falar mal do meu'
                                                                      ' pai!**\n```VOU CONTAR TUDO PRO '
                                                                      'PAPAI```'.format(message.author.mention))

                    try:
                        user_data = self.bot.db.get_data("user_id", message.author.id, "users")
                        if user_data is not None:
                            if user_data['config']['vip'] is True and 'pet ' in message.content.lower():
                                if 'bom dia' in message.content.lower() or 'boa tarde' in message.content.lower():
                                    self.msg[message.author.id] = choice(bomdia)
                                    await self.send_message(message)
                                if 'boa noite' in message.content.lower():
                                    self.msg[message.author.id] = choice(boanoite)
                                    await self.send_message(message)
                                if '?' in message.content.lower():
                                    self.msg[message.author.id] = await get_response(message)
                                    await self.send_message(message)
                            elif 'pet ' in message.content.lower() and '?' in message.content.lower() \
                                    and user_data['config']['vip'] is False:
                                await message.channel.send("<:negate:520418505993093130>│``APENAS USUARIOS COM VIP"
                                                           " ATIVO PODEM USAR ESSE COMANDO``\n **Para ganhar seu vip"
                                                           " diário use ASH INVITE entre no meu canal de suporte e"
                                                           " use o comando ASH VIP**")
                    except discord.Forbidden:
                        pass

                if data_guild['ia_config']['auto_msg']:
                    if message.author.id not in self.ping_test:
                        self.ping_test[message.author.id] = False
                    try:
                        if message.mentions[0] == self.bot.user and self.ping_test[message.author.id] is False:
                            if '?' not in message.content and len(message.content) < 12:
                                end_time = time.time() + 30
                                count_ashley = 0
                                self.ping_test[message.author.id] = True

                                def check(m):
                                    return m.author.id == message.author.id

                                while time.time() < end_time:
                                    if count_ashley == 0:
                                        await message.channel.send('**SE VC PRECISA DE AJUDA USE** ``ASH AJUDA``')
                                    elif count_ashley == 1:
                                        await message.channel.send('``EM QUE POSSO AJUDA-LO?``')
                                    elif count_ashley == 2:
                                        await message.channel.send('``DE NOVO CORAÇÃO?``')
                                    elif count_ashley == 3:
                                        await message.channel.send('``VOCÊ SABE QUE É CHATO MARCAR ALGUEM ASSIM?``')
                                    else:
                                        await message.channel.send('<a:pingada:520418507817615364>'
                                                                   ' ``PARA PELO AMOR DE DEUS!``')
                                        break

                                    message_ashley = await self.bot.wait_for('message', check=check, timeout=10.0)

                                    if '<@478977311266570242>' in message_ashley.content:
                                        if '?' not in message_ashley.content:
                                            count_ashley += 1
                                    else:
                                        await message.channel.send('<a:hi:520418511856730123> ``NÃO SEJA TIMIDO!``')
                                        break
                                self.ping_test[message.author.id] = False
                    except IndexError:
                        self.ping_test[message.author.id] = False
                    except TimeoutError:
                        self.ping_test[message.author.id] = False


def setup(bot):
    bot.add_cog(SystemMessage(bot))
    print('\033[1;32mO evento \033[1;34mON_MESSAGE\033[1;32m foi carregado com sucesso!\33[m')
