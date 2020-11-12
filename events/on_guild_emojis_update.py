import io
import logging
import discord
import asyncio

from discord.ext import commands


class EmojiUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.session

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        data = await self.bot.db.get_data("guild_id", guild.id, "guilds")

        if not data:
            return

        data = data['log_config']
        if data['emoji_update'] and data['log_channel_id']:
            lookup = {e.id for e in before}
            added = [e for e in after if e.id not in lookup and len(e.roles) == 0]

            if not added:
                return

            self.bot.logger.info('Servidor %s adicinou %s emojis.', guild, len(added))
            channel = self.bot.get_channel(data['log_config']['log_channel_id'])

            if not channel:
                return

            for _ in added:
                try:
                    async with self.session.get(_.url) as resp:
                        if resp.status != 200:
                            continue

                        data = io.BytesIO(await resp.read())
                        await channel.send(_.name, file=discord.File(data, f'{_.name}.png'))
                        await asyncio.sleep(1)
                except TypeError:
                    continue


def setup(bot):
    bot.add_cog(EmojiUpdate(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mEMOJI_UPDATE\033[1;33m foi carregado com sucesso!\33[m')
