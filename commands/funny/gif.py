import json
import discord
import requests

from random import randrange
from resources.db import Database
from discord.ext import commands
from resources.check import check_it
from resources.translation import t_

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


def gif_api(tag):
    url = 'http://api.giphy.com/v1/gifs/search?q={}&api_key=NTK5lt0KnPWsHfNmtquZq2FLtAsqharZ&limit=16'.format(tag)
    get_url = requests.get(url)
    url_json = json.loads(get_url.text)
    gif = url_json['data'][randrange(0, 15)]['id']
    return 'https://media.giphy.com/media/{}/giphy.gif'.format(gif)


class GetGif(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.command(name='gif', aliases=['giphy'])
    async def gif(self, ctx, *, tag: str = None):
        if tag is None:
            return await ctx.send('<:negate:520418505993093130>│``DIGITE UMA TAG PARA O GIF``')
        try:
            answer = gif_api(tag)
            embed_gif = discord.Embed(title="\n", description='\n', color=color)
            embed_gif.set_image(url=answer)
            embed_gif.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed_gif)
        except None:
            await ctx.send(t_(ctx, 'Não encontrei nenhuma gif para essa tag!', "guilds"))


def setup(bot):
    bot.add_cog(GetGif(bot))
    print('\033[1;32mO comando \033[1;34mGIF\033[1;32m foi carregado com sucesso!\33[m')
