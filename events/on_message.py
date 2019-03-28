import json
import time
import pytz
import discord

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer
from chatterbot.response_selection import get_most_frequent_response as resp

from random import choice, randint
from scripts import about_me as me
from asyncio import TimeoutError
from discord.ext import commands
from resources.utility import negate, goodbye
from resources.ia_list import perg_pq, resposta_pq, perg_qual, resposta_outras, \
    resposta_ou, denky_r, denky_f, bomdia, boanoite, resposta_comum

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())


class SystemMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ping_test = {}
        self.tz = pytz.all_timezones
        self.scripts = [me.about_me, me.introduction, me.deeping, me.concept]
        self.heart = ChatBot(
            'Ashley',
            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            read_only=True,
            logic_adapters=[
                "chatterbot.logic.BestMatch",
            ],
            database_uri=_auth['db_url'],
            response_selection_method=resp
        )
        self.trainer = ListTrainer(self.heart)
        for script in self.scripts:
            self.trainer.train(script)

    async def get_feedback(self, message):
        def is_correct(m):
            return m.author == message.author and m.channel == message.channel

        try:
            response = await self.bot.wait_for('message', check=is_correct, timeout=30.0)
        except TimeoutError:
            data = self.bot.db.get_data("channel_id", message.channel.id, "channels")
            update = data
            update['channel_state'] = 0
            self.bot.db.update_data(data, update, "channels")
            return await message.channel.send('``Desculpe, você demorou muito, Tchau`` {}**!** ``Até '
                                              'uma próxima``'.format(message.author.mention))
        if response.content.lower() in ['sim', 'yes']:
            return True
        elif response.content.lower() in ['não', 'nao', 'not', 'no']:
            return False
        else:
            await message.channel.send('``por favor digite`` **sim** ``ou`` **não**')
            return None

    @staticmethod
    async def get_response(message, data_guild, bot):
        if '?' in message.content.lower() and data_guild['ia_config']['auto_msg']:
            if 'ashley' in message.content.lower() and len(message.content) > 20:
                try:
                    if message.mentions[0] == bot.user:
                        return
                except IndexError:
                    pass
                for c in range(0, len(perg_pq)):
                    if perg_pq[c] in message.content.lower():
                        response = choice(resposta_pq)
                        return await message.channel.send(response)
                for c in range(0, len(perg_qual)):
                    if perg_qual[c] in message.content.lower():
                        response = choice(resposta_outras)
                        return await message.channel.send(response)
                if ' ou ' in message.content.lower():
                    response = choice(resposta_ou)
                    return await message.channel.send(response)
                elif 'denky' in message.content.lower():
                    response = choice(denky_f)
                    return await message.channel.send(response)
                else:
                    response = choice(resposta_comum)
                    return await message.channel.send(response)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and message.author.id not in self.bot.blacklist:
            data_guild = self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            if data_guild is not None:
                data = self.bot.db.get_channel_data(message.channel.id)
                if data['channel_id'] == message.channel.id and data['channel_state'] == 0:
                    if 'ashley' in message.content.lower() and data_guild['ia_config']['auto_msg']:
                        if 'bom dia' in message.content.lower() or 'boa tarde' in message.content.lower():
                            response = choice(bomdia)
                            return await message.channel.send(f"```{response}```")
                        if 'boa noite' in message.content.lower():
                            response = choice(boanoite)
                            return await message.channel.send(f"```{response}```")
                    elif 'denky' in message.content.lower() and data_guild['ia_config']['auto_msg']:
                        if message.author.id != self.bot.owner_id:
                            for c in range(0, len(denky_r)):
                                if denky_r[c] in message.content:
                                    return await message.channel.send('**Ei,** {}**! Eu to vendo você falar mal do meu '
                                                                      'pai!**\n```VOU CONTAR TUDO PRO '
                                                                      'PAPAI```'.format(message.author.mention))

                    await self.get_response(message, data_guild, self.bot)
                    try:
                        if message.author.id == self.bot.owner_id:
                            chance = randint(1, 100)
                            if chance >= 95:
                                avatar = choice(['a', 'b', 'c', 'd', 'e', 'f'])
                                link_ = f'images/pet/denky/mask_{avatar}.png'
                                msg = choice(resposta_comum)
                                await self.bot.web_hook_rpg(message, link_, 'Dynno', msg, 'Pet')
                    except discord.Forbidden:
                        pass

                try:
                    if message.mentions[0] == self.bot.user and 'vamos conversar' in message.content.lower():
                        if '?' in message.content and len(message.content) > 12:
                            data = self.bot.db.get_channel_data(message.channel.id)
                            if data['channel_id'] == message.channel.id and data['channel_state'] == 0:
                                update = data
                                update['channel_state'] = 1
                                self.bot.db.update_data(data, update, "channels")
                                if message.author.id not in self.bot.staff:
                                    await message.channel.send('``Olá`` {}**!** ``Certo, Vamos conversar?`` **Me '
                                                               'pergunte alguma '
                                                               'coisa!**'.format(message.author.mention))
                                else:
                                    await message.channel.send('``Olha só um dos meus desenvolvedores, como vai`` '
                                                               '{}**!** ``Certo, estou pronta para aprender!`` **Me '
                                                               'pergunte alguma '
                                                               'coisa!**'.format(message.author.mention))
                                while True:
                                    def is_correct(m):
                                        return m.author == message.author and m.channel == message.channel

                                    try:
                                        response = await self.bot.wait_for('message', check=is_correct, timeout=30.0)
                                    except TimeoutError:
                                        data = self.bot.db.get_data("channel_id", message.channel.id, "channels")
                                        update = data
                                        update['channel_state'] = 0
                                        self.bot.db.update_data(data, update, "channels")
                                        return await message.channel.send('``Desculpe, você demorou muito, Tchau`` '
                                                                          '{}**!** ``Até uma '
                                                                          'próxima``'.format(message.author.mention))
                                    if response.content.lower() in goodbye:
                                        data = self.bot.db.get_data("channel_id", message.channel.id, "channels")
                                        update = data
                                        update['channel_state'] = 0
                                        self.bot.db.update_data(data, update, "channels")
                                        await message.channel.send('``Tchau`` {}!``, Até uma '
                                                                   'próxima!``'.format(message.author.mention))
                                        break

                                    if message.author.id in self.bot.staff:
                                        input_statement = Statement(text=response.content)
                                        response_ = self.heart.generate_response(input_statement)
                                        await message.channel.send('``É`` **{}** ``uma resposta coerente para`` **{}**'
                                                                   '``?``'.format(response_.text, input_statement.text))
                                        result = await self.get_feedback(message)
                                        if result is None:
                                            data = self.bot.db.get_data("channel_id", message.channel.id, "channels")
                                            update = data
                                            update['channel_state'] = 0
                                            self.bot.db.update_data(data, update, "channels")
                                            await message.channel.send('``Tchau`` {}!``, Até uma '
                                                                       'próxima!``'.format(message.author.mention))
                                            break
                                        if result is True:
                                            await message.channel.send('**Resposta verificada com sucesso** '
                                                                       '``Qual a proxima pergunta?``')
                                        else:
                                            await message.channel.send('```Por favor insira a correta!```')
                                            try:
                                                response = await self.bot.wait_for('message', check=is_correct,
                                                                                   timeout=30.0)
                                            except TimeoutError:
                                                data = self.bot.db.get_data("channel_id", message.channel.id,
                                                                            "channels")
                                                update = data
                                                update['channel_state'] = 0
                                                self.bot.db.update_data(data, update, "channels")
                                                return await message.channel.send(
                                                    '``Desculpe, você demorou muito, Tchau`` {}**!** ``Até '
                                                    'uma próxima``'.format(message.author.mention))
                                            correct_response = Statement(text=response.content)
                                            self.heart.learn_response(correct_response, input_statement)
                                            await message.channel.send('**Resposta adicionada ao meu DB!** '
                                                                       '``Qual a proxima pergunta?``')
                                    else:
                                        response_ashley = self.heart.get_response(response.content)
                                        if float(response_ashley.confidence) >= 0.3:
                                            await message.channel.send(response_ashley)
                                        else:
                                            await message.channel.send(choice(negate))
                            else:
                                await message.channel.send('{}, ``Eu já estou conversando '
                                                           'com alguem nesse canal!``'.format(message.author.mention))
                except IndexError:
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
