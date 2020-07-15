from ia.scripts import ia
from discord.ext import commands
from config import data as config
from random import choice, randint
from resources.ia_heart import HeartIA
from resources.utility import get_response, include

C_SIM = 98
C_NAO = 98


class IaInteractions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = {}
        self.scripts = [ia.about_me, ia.concept, ia.deeping, ia.introduction, ia.responses, ia.commands, ia.common]
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
            dg, ud = data_guild, user_data
            if dg is not None and ud is not None and dg['ia_config']['auto_msg'] and ud['user']['ia_response']:

                # filtro de comandos ( para nao haver iteração em cima de comandos )
                # -----------======================-----------
                ctx = await self.bot.get_context(message)
                if ctx.command is not None:
                    return
                # -----------======================-----------

                # sistema de chance da ashley  responder a um usuario
                # -------=================-------
                chance = randint(1, 100)
                chance_not = randint(1, 100)
                # -------=================-------

                # sistema de bloqueio de commando em canal / tambem afeta a ia
                # ----------------------==================================----------------------
                run_command = False
                if data_guild['command_locked']['status']:
                    if message.channel.id in data_guild['command_locked']['while_list']:
                        run_command = True
                else:
                    if message.channel.id not in data_guild['command_locked']['black_list']:
                        run_command = True
                # ----------------------==================================----------------------

                # --------------============================--------------
                if run_command is True and include(message.content, ['ash', 'ashley']) is False:
                    chance = 1
                    chance_not = 1
                # --------------============================--------------

                # filtro de quantidade de mensagens salvas por usuario
                try:
                    # filtro de pergunta repetida a longo prazo
                    if len(self.msg[message.author.id]) >= 10:
                        for msg in self.msg[message.author.id]:
                            if message.content == msg and "?" in message.content:
                                if chance >= C_SIM or include(message.content, ['ash', 'ashley']):
                                    content = choice(self.bot.config['answers']['repeat'])
                                    return await self.send_message(message, content)

                    self.msg[message.author.id].append(message.content)
                    if len(self.msg[message.author.id]) >= 20:
                        self.msg[message.author.id] = [message.content]

                except KeyError:
                    self.msg[message.author.id] = [message.content]

                # filtro de repetição de perguntas e mensagens
                try:
                    if self.msg[message.author.id][-1] == self.msg[message.author.id][-2]:
                        if self.msg[message.author.id][-1] == self.msg[message.author.id][-3]:
                            if chance >= C_SIM or include(message.content, ['ash', 'ashley']):
                                content = choice(self.bot.config['answers']['repeated'])
                                return await self.send_message(message, content)
                except IndexError:
                    pass

                # remoção do codi-name "ash" ou "ashley"
                # --------------------============================--------------------
                content_ = message.content.lower()
                content_ = content_.replace("ashley", "").replace("ash", "")
                content_ = content_.replace(" ?", "?").replace("  ", " ").strip()
                # --------------------============================--------------------

                # sistema de IA
                if chance >= C_SIM or include(message.content, ['ash', 'ashley']):
                    if '?' in message.content and len(message.content) > 2:
                        response = self.heart.get_response(content_)
                        if response is not None:
                            return await self.send_message(message, response)
                        else:
                            return await self.send_message(message)
                    else:
                        response = self.heart.get_response(content_)
                        if response is not None:
                            return await self.send_message(message, response)
                        else:
                            if 'bom dia' in message.content.lower() or 'boa tarde' in message.content.lower():
                                content = choice(config['salutation']['day'])
                                return await self.send_message(message, content)
                            elif 'boa noite' in message.content.lower():
                                content = choice(config['salutation']['night'])
                                return await self.send_message(message, content)
                else:
                    if chance_not >= C_NAO and "?" in message.content:
                        content = choice(self.bot.config['answers']['upset'])
                        return await self.send_message(message, content)


def setup(bot):
    bot.add_cog(IaInteractions(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mIA_INTERACTIONS\033[1;33m foi carregado com sucesso!\33[m')
