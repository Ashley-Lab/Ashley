from resources.color import random_color
from discord import Embed
from discord.ext import commands
from resources.webhook import Webhook
from datetime import datetime


class Shards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook = Webhook(url="https://discordapp.com/api/webhooks/627584094959829002/FvTv2bT2k3pbSgO-7pp4-"
                                   "nf6xPsE_oKp9BWbVhCpphzJJyWWVrjQjpXIveUWvIdNzOvL")

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        self.webhook.embed = Embed(
            colour=random_color(),
            description=f"**O shard `{shard_id}` se encontra pronto para uso**\nAproveite o dia ;)",
            timestamp=datetime.utcnow()
        ).set_author(
            name=f"Shard {shard_id}",
            icon_url=self.bot.user.avatar_url
        ).set_thumbnail(
            url=self.bot.user.avatar_url
        ).to_dict()

        await self.webhook.send()


def setup(bot):
    bot.add_cog(Shards(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mON_SHARD_READY\033[1;33m foi carregado com sucesso!\33[m')
