import re
import json
import pymongo
import discord
import requests
import unicodedata

from io import BytesIO
from discord.ext import commands
from asyncio import TimeoutError
from resources.db import Database
from resources.check import check_it
from PIL import Image, ImageDraw, ImageFont, ImageOps

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())


def remove_acentos_e_caracteres_especiais(word):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', word)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z \\\]', '', palavra_sem_acento)


class RankingClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='stars', aliases=['estrelas'])
    async def stars(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.author

        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        await ctx.send(f'<a:loading:520418506567843860>│``Quantas estrelas deseja registrar para`` **{user.name}?**',
                       delete_after=30.0)

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=30.0)
        except TimeoutError:
            return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` '
                                  '**COMANDO CANCELADO**')

        try:
            valor = int(answer.content)
            if valor > 20:
                valor = 20
        except ValueError:
            return await ctx.send("<:negate:520418505993093130>│``Digite apenas Números!``")

        data = self.bot.db.get_data("user_id", user.id, "users")
        update = data
        if data is not None:
            update['user']['winner'] = valor
            self.bot.db.update_data(data, update, "users")
            await ctx.send(f'<:confirmado:519896822072999937>│**{valor}** ``Estrelas Registradas!``', delete_after=10.0)
        else:
            await ctx.send('<:negate:520418505993093130>│``Usuário não encontrado!``', delete_after=10.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='rank', aliases=['r'])
    async def rank(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.author
        data = self.bot.db.get_data("user_id", user.id, "users")

        if data is None:
            return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)

        star_ = "star_default"
        medal = data['inventory']['medal']
        rank_point = data['inventory']['rank_point']
        data_ = self.bot.db.get_all_data("users")
        rank = [x.get("user_id") for x in data_.limit(int(data_.count())).sort("user", pymongo.DESCENDING)]

        position = int(rank.index(user.id)) + 1
        amount_rp = 200
        amount_medal = 0
        count_medal = 0
        count_patent = 0
        patent = 0

        if 100 < rank_point < 200:
            patent += 1
        elif rank_point > 200:
            while True:
                if rank_point >= amount_rp and medal >= amount_medal:
                    amount_medal += count_medal
                    amount_rp += 100
                    count_medal += 1
                    count_patent += 1
                else:
                    patent = count_patent
                    if patent >= 30:
                        patent = 30
                    break

        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``")

        # take name of member
        nome = remove_acentos_e_caracteres_especiais(str(user))

        # take avatar member
        url_avatar = requests.get(user.avatar_url)
        avatar = Image.open(BytesIO(url_avatar.content))
        avatar = avatar.resize((250, 250))
        big_avatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', big_avatar, 0)
        trim = ImageDraw.Draw(mascara)
        trim.ellipse((0, 0) + big_avatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)
        exit_avatar = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
        exit_avatar.putalpha(mascara)
        exit_avatar.save('avatar.png')

        # patent image
        patent_img = Image.open('images/patente/{}.png'.format(patent))
        patent_img = patent_img.resize((205, 248))

        # champion image
        champion = dict()
        for n in range(1, 21):
            if data['user']['winner']:
                if data['user']['winner'] == 0:
                    star_ = 'star_default'
                    champion[n - 1] = Image.open(f'images/elements/{star_}.png')
                    champion[n - 1] = champion[n - 1].resize((130, 90))
                else:
                    if data['user']['ranking'] == "Bronze":
                        star_ = 'star_bronze'
                    if data['user']['ranking'] == "Silver":
                        star_ = 'star_silver'
                    if data['user']['ranking'] == "Gold":
                        star_ = 'star_gold'
                    if data['config']['vip']:
                        star_ = "star_greem"
                    if user.id == ctx.guild.owner.id:
                        star_ = "star_pink"
                    if user.id in self.bot.staff:
                        star_ = "star_blue"
                    if n <= data['user']['winner']:
                        star = star_
                    else:
                        star = 'star_default'
                    champion[n - 1] = Image.open(f'images/elements/{star}.png')
                    champion[n - 1] = champion[n - 1].resize((130, 90))
            else:
                star_ = 'star_default'
                champion[n - 1] = Image.open(f'images/elements/{star_}.png')
                champion[n - 1] = champion[n - 1].resize((130, 90))

        # guild image
        guild_ = self.bot.get_guild(data['guild_id'])
        if guild_ is not None:
            url_guild = requests.get(guild_.icon_url)
            icon_guild = Image.open(BytesIO(url_guild.content)).convert("RGBA")
            icon_guild = icon_guild.resize((190, 190))
        else:
            icon_guild = Image.open('images/elements/no_found.png').convert("RGBA")
            icon_guild = icon_guild.resize((190, 190))

        # load fonts
        font = ImageFont.truetype('fonts/bot.otf', 100)

        # User Align
        bounding_box = [150, 275, 2200, 375]
        x1, y1, x2, y2 = bounding_box
        img = Image.open('images/dashboards/rank.png')
        show = ImageDraw.Draw(img)
        w, h = show.textsize(nome.upper(), font=font)
        x = (x2 - x1 - w) / 2 + x1
        y = (y2 - y1 - h) / 2 + y1
        top = 182

        # add text to img
        show = ImageDraw.Draw(img)
        show.text(xy=(x + 2, y + 2), text=nome.upper(), fill=(0, 0, 0), font=font)
        show.text(xy=(x, y), text=nome.upper(), fill=(255, 255, 255), font=font)
        show.text(xy=(792, 440), text=f'{medal}', fill=(0, 0, 0), font=font)
        show.text(xy=(790, 438), text=f'{medal}', fill=(128, 0, 128), font=font)
        show.text(xy=(1942, 440), text=f'{rank_point}', fill=(0, 0, 0), font=font)
        show.text(xy=(1940, 438), text=f'{rank_point}', fill=(128, 0, 128), font=font)
        show.text(xy=(1102, 440), text=f'#{position}', fill=(0, 0, 0), font=font)
        show.text(xy=(1100, 438), text=f'#{position}', fill=(255, 255, 255), font=font)

        # add img to main img
        img.paste(avatar, (1050, 600), avatar)
        img.paste(patent_img, (765, 595), patent_img)
        img.paste(icon_guild, (1373, 620), icon_guild)
        img.paste(champion[0], (130, top), champion[0])
        img.paste(champion[1], (230, top), champion[1])
        img.paste(champion[2], (330, top), champion[2])
        img.paste(champion[3], (430, top), champion[3])
        img.paste(champion[4], (530, top), champion[4])
        img.paste(champion[5], (630, top), champion[5])
        img.paste(champion[6], (730, top), champion[6])
        img.paste(champion[7], (830, top), champion[7])
        img.paste(champion[8], (930, top), champion[8])
        img.paste(champion[9], (1030, top), champion[9])
        img.paste(champion[10], (1130, top), champion[10])
        img.paste(champion[11], (1230, top), champion[11])
        img.paste(champion[12], (1330, top), champion[12])
        img.paste(champion[13], (1430, top), champion[13])
        img.paste(champion[14], (1530, top), champion[14])
        img.paste(champion[15], (1630, top), champion[15])
        img.paste(champion[16], (1730, top), champion[16])
        img.paste(champion[17], (1830, top), champion[17])
        img.paste(champion[18], (1930, top), champion[18])
        img.paste(champion[19], (2030, top), champion[19])
        img.save('rank.png')
        await msg.delete()
        await ctx.channel.send(file=discord.File('rank.png'))


def setup(bot):
    bot.add_cog(RankingClass(bot))
    print('\033[1;32mO comando \033[1;34mRANKING\033[1;32m foi carregado com sucesso!\33[m')
