import discord
import psutil

from discord.ext import commands
from resources.check import check_it
from datetime import datetime
from resources.db import Database
from collections import Counter
from datetime import datetime as dt


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='botinfo', aliases=['infobot', 'info', 'bi', 'ib'])
    async def botinfo(self, ctx):
        """Comando para ter informações sobre a Ashley
        Use ash botinfo"""
        total_members = sum(len(s.members) for s in self.bot.guilds)
        total_online = sum(1 for m in self.bot.get_all_members() if m.status != discord.Status.offline)
        channel_types = Counter(isinstance(c, discord.TextChannel) for c in self.bot.get_all_channels())
        ver_ = self.bot.version
        voice = channel_types[False]
        text = channel_types[True]
        owner = str(self.bot.get_user(self.bot.owner_id))

        embed_bot = discord.Embed(title='🤖 **Informações da Ashley**', color=self.color, description='\n')
        embed_bot.set_thumbnail(url=self.bot.user.avatar_url)
        embed_bot.add_field(name="📨 | Comandos Executados",
                            value='**{}** ``comandos``'.format(sum(self.bot.commands_used.values())))
        embed_bot.add_field(name="📖 | Canais de texto", value='**{}** ``canais de texto``'.format(text))
        embed_bot.add_field(name="🎤 | Canais de voz", value='**{}** ``canais de voz``'.format(voice))
        embed_bot.add_field(name="<:processor:522400972094308362> | Porcentagem da CPU",
                            value="**{}%**".format(psutil.cpu_percent()))
        embed_bot.add_field(name="<:memory:522400971406573578> | Memoria Usada", value=f'**{self.bot.get_ram()}**')
        embed_bot.add_field(name="<:mito:745375589145247804> | Entre no meu servidor",
                            value="[Clique Aqui](https://discord.gg/rYT6QrM)")
        embed_bot.add_field(name='`💮 | Nome`', value=self.bot.user.name)
        embed_bot.add_field(name='`◼ | Id bot`', value=self.bot.user.id)
        embed_bot.add_field(name='💠 | Criado em', value=self.bot.user.created_at.strftime("%d %b %Y %H:%M"))
        embed_bot.add_field(name='📛 | Tag', value=self.bot.user)
        embed_bot.add_field(name='‍💻 | Servidores', value=str(len(self.bot.guilds)))
        embed_bot.add_field(name='👥 | Usuarios', value='{} ({} online)'.format(total_members, total_online))
        embed_bot.add_field(name='‍⚙ | Programador', value=str(owner))
        embed_bot.add_field(name='🐍 Python  | Version', value=f"`{self.bot.python_version}`")
        embed_bot.add_field(name='<:cool:745375589245911190> Bot  | Version', value=str(ver_))
        embed_bot.add_field(name="<a:loading:520418506567843860> | Tempo Online",
                            value=f"{dt.utcnow() - self.bot.start_time}")
        embed_bot.add_field(name="<:yep:745375589564809216> | Me add em seu Servidor",
                            value="[Clique Aqui](https://discordapp.com/oauth2/authorize?client_id=478977311266570242&s"
                                  "cope=bot&permissions=8)")
        embed_bot.set_footer(text="Comando usado por {} as {} Hrs".format(ctx.author, datetime.now().hour),
                             icon_url=ctx.author.avatar_url)
        await ctx.send(delete_after=120, embed=embed_bot)


def setup(bot):
    bot.add_cog(BotInfo(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mBOTINFO\033[1;32m foi carregado com sucesso!\33[m')
