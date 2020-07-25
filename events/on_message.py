import time
import discord

from discord.ext import commands
from config import data as config
from asyncio import TimeoutError, sleep
from resources.utility import include


class SystemMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ping_test = {}
        self.time = None
        self.user_cont_msg = {}
        self.user_cont_word = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and str(message.author.id) not in self.bot.blacklist:
            data_guild = await self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            if data_guild is not None:

                # filtro de comandos ( para nao haver iteração em cima de comandos
                ctx = await self.bot.get_context(message)
                if ctx.command is not None:
                    return

                perms = ctx.channel.permissions_for(ctx.me)
                if not perms.send_messages or not perms.read_messages:
                    return

                if 'denky' in message.content.lower() and data_guild['ia_config']['auto_msg']:
                    if message.author.id != self.bot.owner_id and "pet " not in message.content.lower():
                        for c in range(0, len(config['questions']['denky_r'])):
                            if config['questions']['denky_r'][c] in message.content:
                                return await message.channel.send('**Ei,** {}**! Eu to vendo você falar mal do meu'
                                                                  ' pai!**\n```VOU CONTAR TUDO PRO '
                                                                  'PAPAI```'.format(message.author.mention))

                if data_guild['ia_config']['auto_msg']:
                    if message.author.id not in self.ping_test:
                        self.ping_test[message.author.id] = {"p": False, "t": time.time()}
                    try:
                        if message.mentions[0] == self.bot.user and self.ping_test[message.author.id]['p'] is False:
                            self.ping_test[message.author.id]['t'] = time.time() + 60
                            self.time = self.ping_test[message.author.id]['t']
                            if "ash " not in message.content.lower():
                                end_time = time.time() + 60
                                count_ashley = 0
                                self.ping_test[message.author.id]['p'] = True

                                def check(m):
                                    return m.author.id == message.author.id

                                while time.time() < end_time:
                                    _1 = "<:safada:530029764061298699> "
                                    _2 = "<:pqp:530031187331121152> "
                                    _3 = "<:afs:530031864350507028> "
                                    if count_ashley == 0:
                                        if time.time() < self.time:
                                            await message.channel.send(f'{_1}``SE VC PRECISA DE AJUDA USE`` '
                                                                       f'**ASH AJUDA**')
                                    elif count_ashley == 1:
                                        if time.time() < self.time:
                                            await message.channel.send(f'{_2}``EM QUE POSSO AJUDA-LO?``')
                                    elif count_ashley == 2:
                                        if time.time() < self.time:
                                            await message.channel.send(f'{_2}``DE NOVO CORAÇÃO?``')
                                    elif count_ashley == 3:
                                        if time.time() < self.time:
                                            await message.channel.send(f'{_3}``VOCÊ SABE QUE É CHATO FICAR '
                                                                       f'MARCANDO?``')
                                    else:
                                        if time.time() < self.time:
                                            await message.channel.send('<a:pingada:520418507817615364>'
                                                                       ' ``PARA PELO AMOR DE DEUS!``')
                                            self.time = time.time() - 1

                                    message_ = await self.bot.wait_for('message', check=check, timeout=30.0)

                                    if "<@!478977311266570242>" in message_.content:
                                        if '?' not in message_.content and "ash " not in message_.content.lower():
                                            count_ashley += 1
                                        else:
                                            if time.time() < self.time:
                                                await message.channel.send(f'{_1}``OI '
                                                                           f'{message.author.name.upper()} '
                                                                           f'ESTOU AQUI PARA TE AJUDAR, USE:`` '
                                                                           f'**ASH AJUDA**')
                                    else:
                                        if time.time() < self.time:
                                            await message.channel.send(f'<a:hi:520418511856730123> '
                                                                       f'{message.author.mention} ``NÃO SEJA '
                                                                       f'TIMIDO, USE:`` **ASH AJUDA**')
                                self.ping_test[message.author.id]['p'] = False
                    except IndexError:
                        self.ping_test[message.author.id]['p'] = False
                    except TimeoutError:
                        self.ping_test[message.author.id]['p'] = False
                    except discord.Forbidden:
                        self.ping_test[message.author.id]['p'] = False

                if message.guild.id == self.bot.config['config']['default_guild']:
                    if message.channel.id == 543589223467450398:
                        all_data = await self.bot.db.get_all_data("guilds")
                        for data in all_data:
                            try:
                                if data['bot_config']['ash_news']:
                                    channel_ = self.bot.get_channel(data['bot_config']['ash_news_id'])
                                    if channel_ is not None:
                                        await channel_.send(message.content)
                            except discord.Forbidden:
                                pass
                            await sleep(0.5)

                if message.guild.id == self.bot.config['config']['default_guild']:
                    if message.channel.id == 525360987373699073:
                        all_data = await self.bot.db.get_all_data("guilds")
                        for data in all_data:
                            try:
                                if data['bot_config']['ash_git']:
                                    channel_ = self.bot.get_channel(data['bot_config']['ash_git_id'])
                                    if channel_ is not None:
                                        await channel_.send(embed=message.embeds[0])
                            except discord.Forbidden:
                                pass
                            except IndexError:
                                pass
                            await sleep(0.5)
            else:
                try:
                    if message.mentions[0] == self.bot.user or include(message.content, ['ashley', 'ash']):
                        await message.channel.send('<:negate:520418505993093130>│``Sua guilda ainda não está '
                                                   'registrada, por favor digite:`` **ash register guild** '
                                                   '``para cadastrar sua guilda no meu`` **banco de dados!**')
                except IndexError:
                    pass


def setup(bot):
    bot.add_cog(SystemMessage(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mON_MESSAGE\033[1;33m foi carregado com sucesso!\33[m')
