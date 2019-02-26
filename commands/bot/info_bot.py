import json
import discord
import psutil

from discord.ext import commands
from resources.check import check_it
from datetime import datetime
from resources.db import Database
from collections import Counter
from datetime import datetime as dt

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class BotInfo(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='botinfo', aliases=['infobot', 'info'])
    async def botinfo(self, ctx):

        total_members = sum(len(s.members) for s in self.bot.guilds)
        total_online = sum(1 for m in self.bot.get_all_members() if m.status != discord.Status.offline)
        channel_types = Counter(isinstance(c, discord.TextChannel) for c in self.bot.get_all_channels())
        ver_ = "API: " + str(discord.__version__) + " | BOT: " + str(self.bot.version) + \
               " | PROGRESS: " + str(self.bot.progress)
        voice = channel_types[False]
        text = channel_types[True]
        owner = str(self.bot.get_user(self.bot.owner_id))

        embed_bot = discord.Embed(title='🤖 **Informações da Ashley**', color=color, description='\n')
        embed_bot.set_thumbnail(url=self.bot.user.avatar_url)
        embed_bot.add_field(name="📨 | Comandos Executados",
                            value='**{}** ``comandos``'.format(sum(self.bot.commands_used.values())))
        embed_bot.add_field(name="📖 | Canais de texto", value='**{}** ``canais de texto``'.format(text))
        embed_bot.add_field(name="🎤 | Canais de voz", value='**{}** ``canais de voz``'.format(voice))
        embed_bot.add_field(name="<:processor:522400972094308362> | Porcentagem da CPU",
                            value="**{}%**".format(psutil.cpu_percent()))
        embed_bot.add_field(name="<:memory:522400971406573578> | Memoria Usada", value=f'**{self.bot.get_ram()}**')
        embed_bot.add_field(name="<:bot:526147892919140371> | Entre no meu servidor",
                            value="[Clique Aqui](https://discord.gg/rYT6QrM)")
        embed_bot.add_field(name='`💮 | Nome`', value=self.bot.user.name)
        embed_bot.add_field(name='`◼ | Id bot`', value=self.bot.user.id)
        embed_bot.add_field(name='💠 | Criado em', value=self.bot.user.created_at.strftime("%d %b %Y %H:%M"))
        embed_bot.add_field(name='📛 | Tag', value=self.bot.user)
        embed_bot.add_field(name='‍💻 | Servidores', value=str(len(self.bot.guilds)))
        embed_bot.add_field(name='👥 | Usuarios', value='{} ({} online)'.format(total_members, total_online))
        embed_bot.add_field(name='‍⚙ | Programador', value=str(owner))
        embed_bot.add_field(name='🐍 Python  | Version', value="`3.6.6`")
        embed_bot.add_field(name='<:ashley:525348179734953995> Bot  | Version', value=str(ver_))
        embed_bot.add_field(name="<a:loading:520418506567843860> | Tempo Online",
                            value=f"{dt.utcnow() - self.bot.start_time}")
        embed_bot.add_field(name="<:bot:526147892919140371> | Me add em seu Servidor",
                            value="[Clique Aqui](https://discordapp.com/oauth2/authorize?client_id=478977311266570242&s"
                                  "cope=bot&permissions=8)")
        embed_bot.set_footer(text="Comando usado por {} as {} Hrs".format(ctx.author, datetime.now().hour),
                             icon_url=ctx.author.avatar_url)
        await ctx.send(delete_after=120, embed=embed_bot)


def setup(bot):
    bot.add_cog(BotInfo(bot))
    print('\033[1;32mO comando \033[1;34mBOTINFO\033[1;32m foi carregado com sucesso!\33[m')
