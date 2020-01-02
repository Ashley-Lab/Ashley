import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import paginator

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)
legend = {"Comum": 500, "Normal": 400, "Raro": 300, "Super Raro": 200, "Ultra Raro": 150, "Secret": 100}


class BoxClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='box', aliases=['caixa'])
    async def box(self, ctx):
        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        if ctx.author.id == data["user_id"]:
            try:
                if data['box']:
                    status = data['box']['status']['active']
                    rarity = data['box']['status']['rarity']
                    num = legend[rarity]
                    secret = data['box']['status']['secret']
                    ur = data['box']['status']['ur']
                    sr = data['box']['status']['sr']
                    r = data['box']['status']['r']
                    n = data['box']['status']['n']
                    c = data['box']['status']['c']
                    size = data['box']['status']['size']
                    images = {'Secret': 'https://i.imgur.com/qjenk0j.png',
                              'Ultra Raro': 'https://i.imgur.com/fdudP2k.png',
                              'Super Raro': 'https://i.imgur.com/WYebgvF.png',
                              'Raro': 'https://i.imgur.com/7LnlnDA.png',
                              'Normal': 'https://i.imgur.com/TnoC2j1.png',
                              'Comum': 'https://i.imgur.com/ma5tHvK.png'}
                    description = '''
Raridade da Box:
**{}**
 ```Markdown
STATUS:
<ACTIVE: {}>
ITEMS:
<SECRET: {}>
<UR: {}>
<SR: {}>
<R: {}>
<N: {}>
<C: {}>
<SIZE: {}/{}>```'''.format(rarity, status, secret, ur, sr, r, n, c, size, num)
                    box = discord.Embed(
                        title="{}'s box:".format(ctx.author.name),
                        color=color,
                        description=description
                    )
                    box.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                    box.set_thumbnail(url="{}".format(images[rarity]))
                    box.set_footer(text="Ashley ® Todos os direitos reservados.")
                    await ctx.send(embed=box)
            except KeyError:
                await ctx.send("<:negate:520418505993093130>│``Você nao tem box na sua conta ainda...``")


def setup(bot):
    bot.add_cog(BoxClass(bot))
    print('\033[1;32mO comando \033[1;34mBOXCLASS\033[1;32m foi carregado com sucesso!\33[m')
