import discord

from discord.ext import commands
from config import data as config
from asyncio import sleep
from resources.utility import include


class SystemMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and str(message.author.id) not in self.bot.blacklist:

            # filtro de comandos ( para nao haver iteração em cima de comandos
            ctx = await self.bot.get_context(message)
            if ctx.command is not None:
                return

            data_guild = await self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            if data_guild is not None:
                if message.guild.id == self.bot.config['config']['default_guild']:
                    if message.channel.id == 543589223467450398:
                        all_data = await self.bot.db.get_all_data("guilds")
                        for data in all_data:
                            try:
                                if data['bot_config']['ash_news']:
                                    channel_ = self.bot.get_channel(data['bot_config']['ash_news_id'])
                                    if channel_ is not None:

                                        perms = ctx.channel.permissions_for(ctx.me)
                                        if not perms.send_messages or not perms.read_messages:
                                            return
                                        msg = message.content.replace("here", "[censored]")
                                        await channel_.send(msg.replace("everyone", "[censored]"))
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

                                        perms = ctx.channel.permissions_for(ctx.me)
                                        if not perms.send_messages or not perms.read_messages:
                                            return

                                        await channel_.send(embed=message.embeds[0])
                            except discord.Forbidden:
                                pass
                            except IndexError:
                                pass
                            await sleep(0.5)
            else:
                try:
                    if message.mentions[0] == self.bot.user:

                        perms = ctx.channel.permissions_for(ctx.me)
                        if not perms.send_messages or not perms.read_messages:
                            return

                        await message.channel.send('<:negate:721581573396496464>│``Sua guilda ainda não está '
                                                   'registrada, por favor digite:`` **ash register guild** '
                                                   '``para cadastrar sua guilda no meu`` **banco de dados!**')
                except IndexError:
                    pass


def setup(bot):
    bot.add_cog(SystemMessage(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mON_MESSAGE\033[1;33m foi carregado com sucesso!\33[m')
