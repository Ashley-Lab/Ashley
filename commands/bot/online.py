import json
import discord

from asyncio import sleep
from discord.ext import commands
from resources.check import check_it
from resources.db import Database


with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)

seconds = None
minutes = None
hour = None
day = None


class UpTimeOnline(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args, **kwargs)
        self.bg_task = self.bot.loop.create_task(self.up_time())

    async def up_time(self):
        await self.bot.wait_until_ready()
        global seconds
        seconds = 0
        global minutes
        minutes = 0
        global hour
        hour = 0
        global day
        day = 0
        while not self.bot.is_closed():
            seconds += 1
            if seconds == 60:
                seconds = 0
                minutes += 1
            await sleep(1)
            if minutes == 60:
                minutes = 0
                hour += 1
            if hour == 24:
                hour = 0
                day += 1

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='online', aliases=['uptime'])
    async def online(self, ctx):
        embed_up_time = discord.Embed(
            title="TEMPO ONLINE DO MODULO PRINCIPAL:",
            color=color,
            description="``Estou online faz {0} dias, {1} horas, {2} minutos e {3} segundos.``".format(day,
                                                                                                       hour,
                                                                                                       minutes,
                                                                                                       seconds))
        embed_up_time.set_author(name="Filizard Project", icon_url="https://i.imgur.com/GY4nTTj.png")
        embed_up_time.set_thumbnail(url="http://vapc.org/qa/wp-content/plugins/RunClickPlugin/images/animator.gif")
        embed_up_time.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.channel.send(embed=embed_up_time)


def setup(bot):
    bot.add_cog(UpTimeOnline(bot))
    print('\033[1;32mO comando \033[1;34mUPTIME\033[1;32m foi carregado com sucesso!\33[m')
