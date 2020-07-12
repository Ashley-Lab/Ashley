from discord.ext import commands
from resources.utility import get_response, include
from random import choice, randint
from config import data as config
from ia.scripts import ia
from resources.ia_heart import HeartIA


class IaInteractions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = {}
        self.num = 1
        self.scripts = [ia.about_me, ia.concept, ia.deeping, ia.introduction, ia.responses, ia.commands, ia.common,
                        ia.yugioh]
        self.heart = HeartIA(self.scripts, 0.9)

    async def send_message(self, message, content=None):
        link_ = f'images/avatar/possessed_ashley.png'
        if content is None:
            msg = await get_response(message)
        else:
            msg = content
        name = choice(['Possessed Ashley'])
        ctx = await self.bot.get_context(message)
        return await self.bot.web_hook_rpg(ctx, link_, name, msg, 'Ashley')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and str(message.author.id) not in self.bot.blacklist:
            data_guild = await self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            user_data = await self.bot.db.get_data("user_id", message.author.id, "users")
            dg = data_guild
            ud = user_data
            if dg is not None and ud is not None and dg['ia_config']['auto_msg'] and ud['user']['ia_response']:

                # filtro de comandos ( para nao haver iteração em cima de comandos
                ctx = await self.bot.get_context(message)
                if ctx.command is not None:
                    return

                # sistema de chance da ashley  responder a um usuario

                # ---======---
                self.num = 1
                # ---======---

                # -----------======================-----------
                try:
                    if '?' in self.msg[message.author.id][-1]:
                        num = 1
                        for msg in self.msg[message.author.id]:
                            if '?' in msg:
                                num += 4
                        self.num = randint(num, 99)
                except KeyError:
                    pass
                # -----------======================-----------

                # --------------============================--------------
                if include(message.content, ['ash', 'ashley']):
                    self.num = 99
                # --------------============================--------------

                # -------=================-------
                chance = randint(self.num, 100)
                and_num = (chance - self.num)
                if and_num < 5:
                    and_num = 5
                chance_not = randint(1, and_num)
                # -------=================-------

                # filtro de quantidade de mensagens salvas por usuario
                try:
                    # filtro de pergunta repetida a longo prazo
                    if len(self.msg[message.author.id]) >= 11:
                        for msg in self.msg[message.author.id]:
                            if message.content == msg:
                                content = choice(['Eu acho que ja respondi isso pra você!',
                                                  'Voce ja tem essa resposta',
                                                  'Eu nao vou te responder isso de novo!',
                                                  'Quantas vezes eu vou ter que falar a mesma coisa?'])
                                if chance >= 99 and "?" in message.content:
                                    return await self.send_message(message, content)
                    self.msg[message.author.id].append(message.content)
                    if len(self.msg[message.author.id]) >= 22:
                        self.msg[message.author.id] = [message.content]
                except KeyError:
                    self.msg[message.author.id] = [message.content]

                # filtro de repetição de perguntas e mensagens
                try:
                    if self.msg[message.author.id][-1] == self.msg[message.author.id][-2]:
                        if self.msg[message.author.id][-1] == self.msg[message.author.id][-3]:
                            content = choice(['Você so sabe falar isso, é?',
                                              'Não tem outra coisa pra falar não?',
                                              'Para de falar a mesma coisa...',
                                              'Você tem problema é? Fica se repetindo...'])
                            if chance >= 99:
                                return await self.send_message(message, content)
                except IndexError:
                    pass

                # remoção do codi-name "ash" ou "ashley"
                content_ = message.content.lower()
                content_ = content_.replace("ashley", "").replace("ash", "")
                content_ = content_.replace(" ?", "?").replace("  ", " ").strip()

                # sistema de IA
                if '?' in message.content and len(message.content) > 2:
                    response = self.heart.get_response(content_)
                    if response is not None:
                        if chance >= 99:
                            return await self.send_message(message, response)
                    else:
                        if chance >= 99:
                            return await self.send_message(message)
                        else:
                            if chance_not < 3 and "?" in message.content:
                                content = choice(['Não estou afim de responder...',
                                                  'Não falo com você...',
                                                  'Estou de mal de você...',
                                                  'Você é muito chato...'])
                                return await self.send_message(message, content)
                else:
                    response = self.heart.get_response(content_)
                    if response is not None:
                        if chance >= 99 and include(message.content, ['ash', 'ashley']):
                            return await self.send_message(message, response)
                    else:
                        if chance >= 99:
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
