import io
import aiohttp
import logging
import discord
import asyncio

log = logging.getLogger(__name__)


class EmojiUpdate(object):
    def __init__(self, bot):
        self.bot = bot
        self.session = None

    async def on_guild_emojis_update(self, guild, before, after):

        data = self.bot.db.get_data("guild_id", guild.id, "guilds")
        if data is not None:

            if data['log_config']['emoji_update'] and data['log_config']['log_channel_id'] is not None:

                self.session = aiohttp.ClientSession()
                lookup = {e.id for e in before}
                added = [e for e in after if e.id not in lookup and len(e.roles) == 0]
                if len(added) == 0:
                    return

                log.info('Servidor %s adicinou %s emojis.', guild, len(added))

                channel = self.bot.get_channel(data['log_config']['log_channel_id'])
                if channel is None:
                    return

                for emoji in added:
                    async with self.session.get(emoji.url) as resp:
                        if resp.status != 200:
                            continue

                        data = io.BytesIO(await resp.read())
                        await channel.send(emoji.name, file=discord.File(data, f'{emoji.name}.png'))
                        await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(EmojiUpdate(bot))
    print('\033[1;32mO evento \033[1;34mEMOJI_UPDATE\033[1;32m foi carregado com sucesso!\33[m')
