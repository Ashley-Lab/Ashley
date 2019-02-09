import json
import time
import pytz

from asyncio import sleep, TimeoutError
from discord.ext import commands
from random import choice
from resources.ia_list import perg_pq, resposta_pq, perg_qual, resposta_outras, \
    resposta_ou, denky_r, denky_f, bomdia, boanoite, resposta_comum
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot.response_selection import get_most_frequent_response as resp
import scripts.about_me as me
from pymongo import MongoClient
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

guild_fp = _auth['default_guild']
database = MongoClient(_auth['db_url'], connectTimeoutMS=30000)
db = database.get_database(_auth['db_name'])
delete = db.channels
deleted = delete.delete_many({})
print("\033[1;31m", deleted.deleted_count, " \033[1;30mregistros de canais bloqueados pela IA deletados.\33[m")
goodbye = ['tchau', 'xau', 'adeus', 'ate mais', 'ate a proxima', 'fim', 'finalizar', 'desliga', 'logoff', 'bye',
           'goodbye']
negate = ['desculpe eu nao conseguir entender!', 'sinto muito, mas não tenho essa informação!',
          'isso nao consta no meu banco de dados.', 'não sei, ainda preciso aprender sobre isso!']
scripts = [me.about_me, me.introduction, me.server]
IA_1 = True
PINGADA = {}
if pytz.all_timezones:
    pass


class SystemMessage(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name="training", aliases=['treinamento'])
    async def training(self, ctx):
        try:
            if ctx.message.mentions[0] == self.bot.user:
                await ctx.channel.send('```Oi PAPAI, me da 1 minuto...```')
                heart = ChatBot('Ashley',
                                database='database/ashley_memory',
                                logic_adapters=["chatterbot.logic.BestMatch"],
                                response_selection_method=resp
                                )
                heart.set_trainer(ListTrainer)
                for script in scripts:
                    heart.train(script)
                await ctx.channel.send('Prontinho **PAPAI**, Vamos treinar?'.format(ctx.author.mention))
                while True:
                    def is_correct(m):
                        return m.author == ctx.author

                    try:
                        include = await self.bot.wait_for('message', check=is_correct, timeout=60.0)
                    except TimeoutError:
                        return await ctx.channel.send('Desculpe, você demorou muito, Tchau {}! '
                                                      'Até uma próxima'.format(ctx.author.mention))
                    if include.content.lower() in goodbye:
                        await ctx.channel.send('Tchau {}!, Até uma próxima!'.format(ctx.author.mention))
                        break
                    response = heart.get_response(include.content)
                    if float(response.confidence) > 0.2:
                        await ctx.channel.send(response)
                    else:
                        await ctx.channel.send(choice(negate))
        except IndexError:
            await ctx.send('Você deve me marcar para treinar!')

    async def on_message(self, message):

        global IA_1, PINGADA

        if message.guild is not None and message.author.id not in self.bot.blacklist:

            data_guild = self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            if data_guild is not None:

                if '?' in message.content.lower() and data_guild['ia_config']['auto_msg']:
                    if 'ashley' in message.content.lower():
                        IA_1 = True
                        for c in range(0, len(perg_pq)):
                            if perg_pq[c] in message.content.lower():
                                resposta = choice(resposta_pq)
                                await message.channel.send(resposta)
                                IA_1 = False
                        for c in range(0, len(perg_qual)):
                            if perg_qual[c] in message.content.lower() and IA_1:
                                resposta = choice(resposta_outras)
                                await message.channel.send(resposta)
                                IA_1 = False
                        if ' ou ' in message.content.lower() and IA_1:
                            resposta = choice(resposta_ou)
                            await message.channel.send(resposta)
                            IA_1 = False
                        if 'denky' in message.content.lower() and IA_1:
                            IA_1 = False
                            resposta = choice(denky_f)
                            await message.channel.send(resposta)
                        if IA_1:
                            resposta = choice(resposta_comum)
                            await message.channel.send(resposta)
                            IA_1 = False
                        await sleep(1)
                        message.content = ''
                        IA_1 = True

                if 'denky' in message.content.lower() and data_guild['ia_config']['auto_msg']:
                    if message.author.id != _auth['owner_id'] and IA_1 is True:
                        for c in range(0, len(denky_r)):
                            if denky_r[c] in message.content:
                                await message.channel.send('Ei, {}! Eu to vendo você falar mal do meu criador!\n'
                                                           '```VOU CONTAR TUDO PRO '
                                                           'DENKY!```'.format(message.author.mention))

                if 'ashley bom dia' in message.content.lower() or 'bom dia ashley' in message.content.lower():
                    resposta = choice(bomdia)
                    await message.channel.send(resposta)

                if 'ashley boa noite' in message.content.lower() or 'boa noite ashley' in message.content.lower():
                    resposta = choice(boanoite)
                    await message.channel.send(resposta)

                if 'vamos conversar' in message.content.lower():
                    try:
                        if message.mentions[0] == self.bot.user:
                            data = self.bot.db.get_channel_data(message.channel.id)
                            if data['channel_id'] == message.channel.id and data['channel_state'] == 0:
                                update = data
                                update['channel_state'] = 1
                                self.bot.db.update_data(data, update, "channels")
                                await message.channel.send('```Markdown\n'
                                                           '[>]: Deixa eu me arrumar aqui, é so um minuto...```')
                                heart = ChatBot('Ashley',
                                                database='database/ashley_memory',
                                                logic_adapters=["chatterbot.logic.BestMatch"],
                                                response_selection_method=resp
                                                )
                                heart.set_trainer(ListTrainer)
                                for script in scripts:
                                    heart.train(script)
                                await message.channel.send('Olá {}! Certo, Vamos conversar? ``Me pergunte alguma '
                                                           'coisa!``'.format(message.author.mention))
                                while True:
                                    def is_correct(m):
                                        return m.author == message.author and m.channel == message.channel

                                    try:
                                        include = await self.bot.wait_for('message', check=is_correct, timeout=60.0)
                                    except TimeoutError:
                                        return await message.channel.send('Desculpe, você demorou muito, Tchau {}! Até '
                                                                          'uma próxima'.format(message.author.mention))
                                    if include.content.lower() in goodbye:
                                        data = self.bot.db.get_data("channel_id", message.channel.id, "channels")
                                        update = data
                                        update['channel_state'] = 0
                                        self.bot.db.update_data(data, update, "channels")
                                        await message.channel.send('Tchau {}!, Até uma '
                                                                   'próxima!'.format(message.author.mention))
                                        break
                                    response = heart.get_response(include.content)
                                    if float(response.confidence) > 0.6:
                                        await message.channel.send(response)
                                    else:
                                        await message.channel.send(choice(negate))
                            else:
                                await message.channel.send('{}, Eu já estou conversando '
                                                           'com alguem nesse canal!'.format(message.author.mention))
                    except IndexError:
                        pass

                if 'treinamento' not in message.content and len(message.content) > 21 \
                        and data_guild['ia_config']['auto_msg'] and 'vamos conversar' not in message.content:
                    if message.author.id not in PINGADA:
                        PINGADA[message.author.id] = False
                    try:
                        if message.mentions[0] == self.bot.user and PINGADA[message.author.id] is False:

                            end_time = time.time() + 30
                            count_ashley = 0
                            PINGADA[message.author.id] = True

                            def check(m):
                                return m.author.id == message.author.id

                            while time.time() < end_time:
                                if count_ashley == 0:
                                    await message.channel.send('``OI CORAÇÃO?``')
                                else:
                                    await message.channel.send('``DE NOVO CORAÇÃO?``')
                                message_ashley = await self.bot.wait_for('message', check=check, timeout=10.0)
                                if '?' not in message_ashley.content and '<@478977311266570242>' \
                                        in message_ashley.content:
                                    count_ashley += 1
                                    if count_ashley == 2:
                                        await message.channel.send('<a:pingada:520418507817615364>'
                                                                   ' ``PARA PELO AMOR DE DEUS!``')
                                        break
                                else:
                                    await message.channel.send('<a:hi:520418511856730123> ``NUNCA NEM VI``')
                                    break
                            PINGADA[message.author.id] = False
                    except IndexError:
                        PINGADA[message.author.id] = False
                    except TimeoutError:
                        PINGADA[message.author.id] = False


def setup(bot):
    bot.add_cog(SystemMessage(bot))
    print('\033[1;32mO evento \033[1;34mSYSTEM_MESSAGE\033[1;32m foi carregado com sucesso!\33[m')
