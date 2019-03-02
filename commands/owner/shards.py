from resources.color import random_color
from discord import Embed
from discord.ext import commands
from resources.webhook import WebHook
from datetime import datetime
from resources.check import check_it
from resources.db import Database
from random import choice


class Shards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.web_hook = WebHook(url="https://discordapp.com/api/webhooks/529827969129250827/hf9iQua6Yqk6GZI6wGW9oyk"
                                    "WqpCHS9dA0QVg7NNVtZcbZCJJMR4u5SWK2qAgMoFKkNaP")

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        self.web_hook.embed = Embed(
            colour=random_color(),
            description=f"**O shard `{shard_id}` se encontra pronto para uso**\nAproveite o dia ;)",
            timestamp=datetime.utcnow()
        ).set_author(
            name=f"Shard {shard_id}",
            icon_url=self.bot.user.avatar_url
        ).set_thumbnail(
            url=self.bot.user.avatar_url
        ).to_dict()
        
        self.web_hook.send_()

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def pet(self, ctx, *, msg=None):
        avatar = choice(['a', 'b', 'c', 'd', 'e', 'f'])
        link_ = f'images/pet/denky/mask_{avatar}.png'
        avatar = open(link_, 'rb')
        web_hook_ = await ctx.channel.create_webhook(name="Dynno", avatar=avatar.read())
        web_hook = WebHook(url=web_hook_.url)

        web_hook.embed = Embed(
            colour=random_color(),
            description=f"**{msg}**",
            timestamp=datetime.utcnow()
        ).set_author(
            name="Pet",
            icon_url=ctx.author.avatar_url
        ).set_thumbnail(
            url=ctx.guild.icon_url
        ).to_dict()

        web_hook.send_()
        await web_hook_.delete()


def setup(bot):
    bot.add_cog(Shards(bot))
