import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color_ = int(_auth['default_embed'], 16)

botmsg = {}


class Helper(object):
    def __init__(self, bot):
        self.bot = bot
        self.st = []

    def status(self):
        for v in self.bot.data_cog.values():
            self.st.append(v)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='help', aliases=['ajuda'])
    async def help(self, ctx):
        self.status()
        embed = discord.Embed(
            title="Choice Area:",
            color=color_,
            description=f"- For **Main**: click in :classical_building:\n"
                        f"- For **Music**: click in :musical_note:\n"
                        f"- For **Iterations IA**: click in :microphone2:\n"
                        f"- For **Games**: click in :game_die:\n"
                        f"- For **General Pt1**: click in :earth_americas:\n"
                        f"- For **General Pt2**: click in :earth_asia:\n"
                        f"- For **General Pt3**: click in :earth_africa:\n"
                        f"- For **Economy**: click in :moneybag:\n"
                        f"- For **Staffs**: click in :police_car:\n"
                        f"- For **Owner**: click in :shield:")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="http://sisadm2.pjf.mg.gov.br/imagem/ajuda.png")
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        global botmsg
        try:
            botmsg[ctx.author.id] = await ctx.author.send(embed=embed)
            if ctx.message.guild is not None:
                await ctx.send('<:send:519896817320591385>│``ENVIADO PARA O SEU PRIVADO!``')
            await botmsg[ctx.author.id].add_reaction('🏛')
            await botmsg[ctx.author.id].add_reaction('🎵')
            await botmsg[ctx.author.id].add_reaction('🎙')
            await botmsg[ctx.author.id].add_reaction('🎲')
            await botmsg[ctx.author.id].add_reaction('🌎')
            await botmsg[ctx.author.id].add_reaction('🌏')
            await botmsg[ctx.author.id].add_reaction('🌍')
            await botmsg[ctx.author.id].add_reaction('💰')
            await botmsg[ctx.author.id].add_reaction('🚓')
            await botmsg[ctx.author.id].add_reaction('🛡')
        except discord.errors.Forbidden:
            botmsg[ctx.author.id] = await ctx.send(embed=embed)
            await botmsg[ctx.author.id].add_reaction('🏛')
            await botmsg[ctx.author.id].add_reaction('🎵')
            await botmsg[ctx.author.id].add_reaction('🎙')
            await botmsg[ctx.author.id].add_reaction('🎲')
            await botmsg[ctx.author.id].add_reaction('🌎')
            await botmsg[ctx.author.id].add_reaction('🌏')
            await botmsg[ctx.author.id].add_reaction('🌍')
            await botmsg[ctx.author.id].add_reaction('💰')
            await botmsg[ctx.author.id].add_reaction('🚓')
            await botmsg[ctx.author.id].add_reaction('🛡')

    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        try:
            if botmsg[user.id]:
                pass
        except KeyError:
            return

        if reaction.emoji == "🏛" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Choice Area:",
                color=color_,
                description=f"- For **Main**: click in :classical_building:\n"
                            f"- For **Music**: click in :musical_note:\n"
                            f"- For **Iterations IA**: click in :microphone2:\n"
                            f"- For **Games**: click in :game_die:\n"
                            f"- For **General Pt1**: click in :earth_americas:\n"
                            f"- For **General Pt2**: click in :earth_asia:\n"
                            f"- For **General Pt3**: click in :earth_africa:\n"
                            f"- For **Economy**: click in :moneybag:\n"
                            f"- For **Staffs**: click in :police_car:\n"
                            f"- For **Owner**: click in :shield:")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(url="http://sisadm2.pjf.mg.gov.br/imagem/ajuda.png")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🎵" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                            f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(
                url="http://icons.iconarchive.com/icons/raindropmemory/summer-love-cicadas/256/Music-1-icon.png")
            ajuda.add_field(name="Music Commands:",
                            value=f"{self.st[31]}│**join** ``or`` **entrar**\n"
                                  f"{self.st[31]}│**play** ``or`` **tocar**\n"
                                  f"{self.st[31]}│**pause** ``or`` **pausar**\n"
                                  f"{self.st[31]}│**resume** ``or`` **retornar**\n"
                                  f"{self.st[31]}│**skip** ``or`` **pular**\n"
                                  f"{self.st[31]}│**playlist** ``or`` **lista**\n"
                                  f"{self.st[31]}│**current** ``or`` **tocando**\n"
                                  f"{self.st[31]}│**volume** ``or`` **vol**\n"
                                  f"{self.st[31]}│**stop** ``or`` **parar**\n"
                                  f"{self.st[31]}│**shuffle** ``or`` **embaralhar**\n"
                                  f"{self.st[31]}│**clear** ``or`` **limpar**\n"
                                  f"{self.st[31]}│**remove** ``or`` **remover**\n"
                                  f"{self.st[31]}│**repeat** ``or`` **repetir**")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🎙" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(
                url="https://res.cloudinary.com/hrscywv4p/image/upload/c_limit,fl_lossy,h_630,w_1200,f_auto,"
                    "q_auto/v1/82571/2016-11-ia-logo-circle_ofybij.png")
            ajuda.add_field(name="IA Iterations:",
                            value=f"{self.st[61]}│**Pergunte Algo** : "
                                  f"``Respondo a mensagens que tenha uma interrogação e meu nome!``\n"
                                  f"{self.st[61]}│**Bom dia** : "
                                  f"``Respondo a mensagens que tenham: bom dia e meu nome``\n"
                                  f"{self.st[61]}│**Boa Noite** : "
                                  f"``Respondo a mensagens que tenham: boa tarde e meu nome``\n"
                                  f"{self.st[61]}│**Converse Comigo** : "
                                  f"``Para isso basta me marcar e digitar`` **vamos conversar**\n"
                                  f"{self.st[61]}│**Marcação** : ``há quase ia me esquecendo, "
                                  f"por favor não fique me `` **marcando**\n"
                                  f"{self.st[61]}│**Meu Pai** : "
                                  f"``Se você ofender meu pai eu vou dizer tudo pra ele!``")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🎲" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(url="https://cdn.icon-icons.com/icons2/897/PNG/512/1-03_icon-icons.com_69189.png")
            ajuda.add_field(name="Games Commands:",
                            value=f"{self.st[18]}│**advinhe** ``or`` **guess**\n"
                                  f"{self.st[19]}│**jokenpo** ``or`` **jkp**\n"
                                  f"{self.st[17]}│**moeda** ``or`` **hot**\n"
                                  f"{self.st[68]}│**card** ``or`` **carta**\n"
                                  f"{self.st[69]}│**whats** ``or`` **charada**\n"
                                  f"{self.st[81]}│**pokemon** ``or`` **poke**\n"
                                  f"{self.st[77]}│**hangman** ``or`` **forca**\n")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🌎" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(url="http://www.pngall.com/wp-content/uploads/2016/06/Earth-Free-PNG-Image-180x180.png")
            ajuda.add_field(name="General Commands:\n",
                            value=f"{self.st[24]}│**reflita** ``or`` **reflect**\n"
                                  f"{self.st[16]}│**pensador** ``or`` **thinker**\n"
                                  f"{self.st[20]}│**emojis** ``or`` **emoji**\n"
                                  f"{self.st[44]}│**avatar** ``or`` **a**\n"
                                  f"{self.st[4]}│**online** ``or`` **uptime**\n"
                                  f"{self.st[15]}│**diga** ``or`` **say**\n"
                                  f"{self.st[21]}│**serverinfo** ``or`` **infoserver**\n"
                                  f"{self.st[26]}│**userinfo** ``or`` **infouser**\n"
                                  f"{self.st[22]}│**roleinfo** ``or`` **inforole**\n"
                                  f"{self.st[3]}│**botinfo** ``or`` **infobot**\n"
                                  f"{self.st[13]}│**abraço** ``or`` **hug**\n"
                                  f"{self.st[25]}│**entrou** ``or`` **entered**\n"
                                  f"{self.st[70]}│**kick** ``or`` **chute**\n"
                                  f"{self.st[71]}│**kiss** ``or`` **beijo**\n"
                                  f"{self.st[72]}│**lick** ``or`` **lambida**\n"
                                  f"{self.st[73]}│**punch** ``or`` **soco**\n")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🌏" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(url="http://www.pngall.com/wp-content/uploads/2016/06/Earth-Free-PNG-Image-180x180.png")
            ajuda.add_field(name="General Commands:\n",
                            value=f"{self.st[12]}│**fofoca** ``or`` **gossip**\n"
                                  f"{self.st[11]}│**gif** ``or`` **giphy**\n"
                                  f"{self.st[5]}│**ping** ``or`` **latency**\n"
                                  f"{self.st[48]}│**vote** ``or`` **voto**\n"
                                  f"{self.st[47]}│**rolar** ``or`` **roll**\n"
                                  f"{self.st[2]}│**feedback** ``or`` **sugestao**\n"
                                  f"{self.st[10]}│**textao** ``or`` **ascii**\n"
                                  f"{self.st[45]}│**sorteio** ``or`` **draw**\n"
                                  f"{self.st[27]}│**skin** ``or`` **mine**\n"
                                  f"{self.st[8]}│**convite** ``or`` **invite**\n"
                                  f"{self.st[14]}│**palin** ``or`` **palindromo**\n"
                                  f"{self.st[43]}│**status** ``or`` **habilidades**\n"
                                  f"{self.st[43]}│**status** + ``add`` **or** ``adicionar``\n"
                                  f"{self.st[74]}│**push** ``or`` **empurrao**\n"
                                  f"{self.st[75]}│**slap** ``or`` **tapa**\n"
                                  f"{self.st[67]}│**top**")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🌍" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(url="http://www.pngall.com/wp-content/uploads/2016/06/Earth-Free-PNG-Image-180x180.png")
            ajuda.add_field(name="FP Commands:",
                            value=f"{self.st[9]}│**cargos** ``or`` **roles**\n"
                                  f"{self.st[7]}│**teleport** ``or`` **teletransportar**\n"
                                  f"{self.st[7]}│**respawn** ``or`` **return**\n"
                                  f"{self.st[42]}│**combate** ``or`` **battle**\n"
                                  f"{self.st[42]}│**reset** ``or`` **resetar**\n"
                                  f"{self.st[79]}│**marry** ``or`` **casar**\n"
                                  f"{self.st[79]}│**divorce** ``or`` **separar**\n"
                                  f"{self.st[80]}│**dance** ``or`` **dançar**\n"
                                  f"{self.st[78]}│**profile** ``or`` **perfil**\n"
                                  f"{self.st[46]}│**rank** ``or`` **r**\n")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "💰" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(url="http://www.pngmart.com/files/7/Money-PNG-Transparent-Image.png")
            ajuda.add_field(name="Economy Commands:",
                            value=f"{self.st[28]}│**economia**\n"
                                  f"{self.st[29]}│**tesouro**\n"
                                  f"{self.st[30]}│**carteira**\n"
                                  f"{self.st[66]}│**daily** ``or`` **diario**")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🚓" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(url="http://mieinfo.com/wp-content/uploads/2013/08/policia-mie.png")
            ajuda.add_field(name="Staffs Commands:",
                            value=f"{self.st[1]}│**staff**\n"
                                  f"{self.st[1]}│**staff** ``delete``\n"
                                  f"{self.st[1]}│**staff** ``language``\n"
                                  f"{self.st[1]}│**staff** ``ban``\n"
                                  f"{self.st[1]}│**staff** ``kick``\n"
                                  f"{self.st[1]}│**staff** ``slowmode``\n"
                                  f"{self.st[1]}│**staff** ``report``")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🛡" and reaction.message.id == botmsg[user.id].id:
            ajuda = discord.Embed(
                title="Commands Status",
                color=color_,
                description=f"<:on_status:519896814799945728>│On\n<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n<:stream_status:519896814825242635>│Vip")
            ajuda.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            ajuda.set_thumbnail(url="http://www.creativemultimediainstitute.in/images/pages/computer-programming-"
                                    "language-classes.png")
            ajuda.add_field(name="Owner Commands:",
                            value=f"{self.st[33]}│**make_doc**\n"
                                  f"{self.st[40]}│**total_de_comandos**\n"
                                  f"{self.st[39]}│**source**\n"
                                  f"{self.st[34]}│**eval**\n"
                                  f"{self.st[38]}│**repeat_command**\n"
                                  f"{self.st[32]}│**announce**\n"
                                  f"{self.st[32]}│**announce** ``add``\n"
                                  f"{self.st[35]}│**load**\n"
                                  f"{self.st[41]}│**unload**\n"
                                  f"{self.st[37]}│**reload**\n"
                                  f"{self.st[36]}│**logout**\n")
            ajuda.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=ajuda)
            await botmsg[user.id].add_reaction('🏛')
            await botmsg[user.id].add_reaction('🎵')
            await botmsg[user.id].add_reaction('🎙')
            await botmsg[user.id].add_reaction('🎲')
            await botmsg[user.id].add_reaction('🌎')
            await botmsg[user.id].add_reaction('🌏')
            await botmsg[user.id].add_reaction('🌍')
            await botmsg[user.id].add_reaction('💰')
            await botmsg[user.id].add_reaction('🚓')
            await botmsg[user.id].add_reaction('🛡')


def setup(bot):
    bot.add_cog(Helper(bot))
    print('\033[1;32mO comando \033[1;34mAJUDA\033[1;32m foi carregado com sucesso!\33[m')
