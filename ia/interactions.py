import logging
import discord

from discord.ext import commands
from resources.utility import get_response
from random import choice, randint
from config import data as config
# importação dos scripts de ia (texto)
from ia.scripts import ia
# importação das libs do chatbot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# retirando a mensagem de avisos com respostas nao encontradas
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


class IaInteractions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = {}
        self.scripts = [ia.about_me, ia.concept, ia.deeping, ia.introduction, ia.responses]
        self.heart = ChatBot('Guardians', read_only=True)
        self.trainer = ListTrainer(self.heart)
        for script in self.scripts:
            self.trainer.train(script)

    async def send_message(self, message, content=None):
        link_ = f'images/avatar/possessed_ashley.png'
        if content is None:
            msg = await get_response(message)
        else:
            msg = content
        name = choice(['Possessed Ashley'])
        try:
            return await self.bot.web_hook_rpg(message, link_, name, msg, 'Ashley')
        except discord.errors.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and str(message.author.id) not in self.bot.blacklist:
            data_guild = self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            user_data = self.bot.db.get_data("user_id", message.author.id, "users")
            if data_guild is not None and user_data is not None and data_guild['ia_config']['auto_msg']:

                # filtro de mensagens
                try:
                    self.msg[message.author.id].append(message.content)
                    if len(self.msg[message.author.id]) >= 10:
                        self.msg[message.author.id] = [message.content]
                except KeyError:
                    self.msg[message.author.id] = [message.content]

                # sistema de chance
                num_i = 1
                if '?' in self.msg[message.author.id][-1] and '?' in self.msg[message.author.id][-2]:
                    num_i = randint(71, 99)
                elif 'ashley' in self.msg[message.author.id][-1].lower():
                    num_i = 99
                chance = randint(num_i, 100)

                # filtro de repetição de perguntas e mensagens
                if self.msg[message.author.id][-1] == self.msg[message.author.id][-2]:
                    if self.msg[message.author.id][-1] == self.msg[message.author.id][-3]:
                        content = choice(['Você so sabe falar isso, é?', 'Não tem outra coisa pra falar não?',
                                          'Para de falar a mesma coisa...', 'Você tem problema? Fica se repetindo...'])
                        return await self.send_message(message, content)

                # sistema de IA
                if '?' in message.content and len(message.content) > 2:
                    response = self.heart.get_response(message.content)
                    if float(response.confidence) >= 0.75:
                        return await self.send_message(message, response)
                    else:
                        if chance >= 75:
                            return await self.send_message(message)
                        elif chance < 10:
                            content = choice(['Não estou afim de responder...', 'Não falo com você...',
                                              'Estou de mal de você...', 'Você é muito chato...'])
                            return await  self.send_message(message, content)
                else:
                    response = self.heart.get_response(message.content)
                    if float(response.confidence) >= 0.80:
                        return await self.send_message(message, response)
                    else:
                        if 'bom dia' in message.content.lower() or 'boa tarde' in message.content.lower():
                            content = choice(config['salutation']['day'])
                            return await self.send_message(message, content)
                        elif 'boa noite' in message.content.lower():
                            content = choice(config['salutation']['night'])
                            return await self.send_message(message, content)


def setup(bot):
    bot.add_cog(IaInteractions(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mIA_INTERACTIONS\033[1;33m foi carregado com sucesso!\33[m')
