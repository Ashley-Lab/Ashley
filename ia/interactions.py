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
        self.num = 0
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
            dg = data_guild
            ud = user_data
            if dg is not None and ud is not None and dg['ia_config']['auto_msg'] and ud['user']['ia_response']:

                # filtro de comandos ( para nao haver iteração em cima de comandos
                ctx = await self.bot.get_context(message)
                if ctx.command:
                    return

                # filtro de quantidade de mensagens salvas por usuario
                try:
                    self.msg[message.author.id].append(message.content)
                    if len(self.msg[message.author.id]) >= 20:
                        self.msg[message.author.id] = [message.content]
                except KeyError:
                    self.msg[message.author.id] = [message.content]

                # sistema de chance da ashley  responder a um usuario

                # ---======---
                self.num = 1
                # ---======---

                # -----------======================-----------
                if '?' in self.msg[message.author.id][-1]:
                    num = 1
                    for msg in self.msg[message.author.id]:
                        if '?' in msg:
                            num += 4
                        else:
                            num = 1
                    self.num = randint(num, 95)
                # -----------======================-----------

                # --------------============================--------------
                if 'ash' in self.msg[message.author.id][-1].lower():
                    self.num = 95
                # --------------============================--------------

                chance = randint(self.num, 100)

                # filtro de repetição de perguntas e mensagens
                try:
                    if self.msg[message.author.id][-1] == self.msg[message.author.id][-2]:
                        if self.msg[message.author.id][-1] == self.msg[message.author.id][-3]:
                            content = choice(['Você so sabe falar isso, é?',
                                              'Não tem outra coisa pra falar não?',
                                              'Para de falar a mesma coisa...',
                                              'Você tem problema é? Fica se repetindo...'])
                            if chance >= 95:
                                return await self.send_message(message, content)
                except IndexError:
                    pass

                # filtro de pergunta repetida a longo prazo
                if len(self.msg[message.author.id]) >= 10 and message.content in self.msg[message.author.id]:
                    content = choice(['Eu acho que ja respondi isso pra você!',
                                      'Voce ja tem essa resposta',
                                      'Eu nao vou te responder isso de novo!',
                                      'Quantas vezes eu vou ter que falar a mesma coisa?'])
                    if chance >= 95:
                        return await self.send_message(message, content)

                # sistema de IA
                if '?' in message.content and len(message.content) > 2:
                    response = self.heart.get_response(message.content)

                    if float(response.confidence) >= 0.8:

                        # sistema de log de perguntas de respostas
                        channel = self.bot.get_channel(706571512550785045)
                        await channel.send(f'**Mensagem enviada pelo usuario:**\n > ``{message.content}``\n'
                                           f'**Resposta processada pela ashley:**\n > ``{response}``')

                        if chance >= 95:
                            return await self.send_message(message, response)
                    else:
                        if chance >= 95:
                            return await self.send_message(message)
                        elif chance < 5:
                            content = choice(['Não estou afim de responder...',
                                              'Não falo com você...',
                                              'Estou de mal de você...',
                                              'Você é muito chato...'])
                            return await  self.send_message(message, content)
                else:
                    response = self.heart.get_response(message.content)

                    if float(response.confidence) >= 0.9:

                        # sistema de log de perguntas de respostas
                        channel = self.bot.get_channel(706571512550785045)
                        await channel.send(f'**Mensagem enviada pelo usuario:**\n > ``{message.content}``\n'
                                           f'**Resposta processada pela ashley:**\n > ``{response}``')

                        if chance >= 95:
                            return await self.send_message(message, response)
                    else:
                        if chance >= 95:
                            if 'bom dia' in message.content.lower() or 'boa tarde' in message.content.lower():
                                content = choice(config['salutation']['day'])
                                content = content.lower()
                                content = content.replace('bom dia', 'boa tarde')
                                return await self.send_message(message, content)
                            elif 'boa noite' in message.content.lower():
                                content = choice(config['salutation']['night'])
                                return await self.send_message(message, content)


def setup(bot):
    bot.add_cog(IaInteractions(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mIA_INTERACTIONS\033[1;33m foi carregado com sucesso!\33[m')
