import re
import json
import pymongo
import discord
import requests
import unicodedata

from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from asyncio import TimeoutError
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())


def remove_acentos_e_caracteres_especiais(word):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', word)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z \\\]', '', palavra_sem_acento)


class RankingClass(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='winner', aliases=['vencedor'])
    async def winner(self, ctx):
        try:
            data = self.bot.db.get_data("user_id", ctx.message.mentions[0].id, "users")
        except IndexError:
            data = self.bot.db.get_data("user_id", ctx.author.id, "users")

        update = data

        def check(m):
            return m.author == ctx.author

        await ctx.channel.send('Quantas vezes campeão?', delete_after=10.0)

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=10.0)
        except TimeoutError:
            return await  ctx.channel.send('Desculpe, você demorou muito, Comando cancelado!')

        valor = int(answer.content)

        try:
            update.delete(data['user']["winner"])
            update['user']['winner'] = valor
        except IndexError:
            update['user']['winner'] = valor
            self.bot.db.push_data(data, update, "users")

        await ctx.channel.send('Registrado!', delete_after=3.0)

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

        medal = data['inventory']['medal']
        rank_point = data['inventory']['rank_point']
        data_ = self.bot.db.get_all_data("users")

        rank = [x.get("user_id") for x in data_.limit(int(data_.count())).sort("user", pymongo.DESCENDING)]

        position = int(rank.index(user.id)) + 1
        amount_rp = 200
        amount_medal = 0
        count_medal = 1
        count_patent = 1
        patent = 1

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
        avatar = avatar.resize((270, 270))
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

        # champion image
        champion = Image.open('images/elements/campeao.png')
        champion = champion.resize((130, 90))
        # guild image
        url_guild = requests.get(data['guild_icon_url'])
        icon_guild = Image.open(BytesIO(url_guild.content))
        icon_guild = icon_guild.resize((170, 170))
        big_icon_guild = (icon_guild.size[0] * 3, icon_guild.size[1] * 3)
        mascara_guild = Image.new('L', big_icon_guild, 0)
        trim_guild = ImageDraw.Draw(mascara_guild)
        trim_guild.ellipse((0, 0) + big_icon_guild, fill=255)
        mascara_guild = mascara_guild.resize(icon_guild.size, Image.ANTIALIAS)
        icon_guild.putalpha(mascara_guild)
        exit_icon_guild = ImageOps.fit(icon_guild, mascara_guild.size, centering=(0.5, 0.5))
        exit_icon_guild.putalpha(mascara_guild)
        exit_icon_guild.save('icon_guild.png')

        # load fonts
        font = ImageFont.truetype('fonts/bot.otf', 100)
        font_2 = ImageFont.truetype('fonts/bot.otf', 80)

        # img
        img = Image.open('images/dashboards/rank.png')

        # add text to img
        show = ImageDraw.Draw(img)
        show.text(xy=(700, 320), text=nome.upper(), fill=(255, 255, 255), font=font)
        show.text(xy=(730, 573), text=f'{medal}', fill=(255, 90, 0), font=font_2)
        show.text(xy=(1840, 570), text=f'{rank_point}', fill=(255, 90, 0), font=font_2)
        show.text(xy=(450, 324), text=f'#{position}', fill=(255, 255, 255), font=font_2)

        # add img to main img
        img.paste(avatar, (1030, 550), avatar)
        img.paste(patent_img, (2055, 300), patent_img)
        # img.paste(rank, (712, 684), rank)
        img.paste(icon_guild, (1400, 710), icon_guild)

        try:
            if data['user']['winner'] == 1:
                img.paste(champion, (800, 435), champion)
            elif data['user']['winner'] == 2:
                img.paste(champion, (800, 435), champion)
                img.paste(champion, (900, 435), champion)
            elif data['user']['winner'] == 3:
                img.paste(champion, (800, 435), champion)
                img.paste(champion, (900, 435), champion)
                img.paste(champion, (1000, 435), champion)
            img.save('rank.png')
        except IndexError:
            img.save('rank.png')

        await msg.delete()
        await ctx.channel.send(file=discord.File('rank.png'))


def setup(bot):
    bot.add_cog(RankingClass(bot))
    print('\033[1;32mO comando \033[1;34mRANKING\033[1;32m foi carregado com sucesso!\33[m')
