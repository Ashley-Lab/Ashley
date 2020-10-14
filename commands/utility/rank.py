import re
import discord
import operator
import unicodedata

from aiohttp_requests import requests
from io import BytesIO
from discord.ext import commands
from asyncio import TimeoutError
from resources.db import Database
from resources.check import check_it
from PIL import Image, ImageDraw, ImageFont, ImageOps
from resources.check import validate_url


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
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` '
                                  '**COMANDO CANCELADO**')

        try:
            valor = int(answer.content)
            if valor > 20:
                valor = 20
        except ValueError:
            return await ctx.send("<:negate:721581573396496464>│``Digite apenas Números!``")

        data = await self.bot.db.get_data("user_id", user.id, "users")
        update = data
        if data is not None:
            update['user']['stars'] = valor
            await self.bot.db.update_data(data, update, "users")
            await ctx.send(f'<:confirmed:721581574461587496>│**{valor}** ``Estrelas Registradas!``',
                           delete_after=10.0)
        else:
            await ctx.send('<:negate:721581573396496464>│``Usuário não encontrado!``', delete_after=10.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='rank', aliases=['r'])
    async def rank(self, ctx, user: discord.Member = None):
        """Mostra seu rank da Ashley
        Use ash rank"""
        if user is None:
            user = ctx.author

        data = await self.bot.db.get_data("user_id", user.id, "users")

        if data is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)

        star_ = "star_default"
        medal = data['inventory']['medal']
        rank_point = data['inventory']['rank_point']
        data_ = await self.bot.db.get_all_data("users")

        dict_ = dict()
        for _ in data_:
            dict_[str(_.get('user_id'))] = _['user'].get('experience', 0)
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        rank = [int(sorted_x[x][0]) for x in range(len(data_))]

        position = int(rank.index(user.id)) + 1
        patent = data['user']['patent']

        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``")

        # take name of member
        nome = remove_acentos_e_caracteres_especiais(str(user))

        # take avatar member
        if validate_url(str(user.avatar_url_as(format="png"))):
            link = str(user.avatar_url_as(format="png"))
        else:
            link = "https://festsonho.com.br/images/sem_foto.png"
        url_avatar = await requests.get(link)
        avatar = Image.open(BytesIO(await url_avatar.read())).convert('RGBA')
        avatar = avatar.resize((250, 250))
        big_avatar = (avatar.size[0] * 3, avatar.size[1] * 3)
        mascara = Image.new('L', big_avatar, 0)
        trim = ImageDraw.Draw(mascara)
        trim.ellipse((0, 0) + big_avatar, fill=255)
        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mascara)
        exit_avatar = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
        exit_avatar.putalpha(mascara)
        avatar = exit_avatar

        # patent image
        patent_img = Image.open('images/patente/{}.png'.format(patent)).convert('RGBA')
        patent_img = patent_img.resize((205, 248))

        # champion image
        champion = dict()
        for n in range(1, 21):
            if data['user']['stars']:
                if data['user']['stars'] == 0:
                    star_ = 'star_default'
                    champion[n - 1] = Image.open(f'images/elements/{star_}.png').convert('RGBA')
                    champion[n - 1] = champion[n - 1].resize((130, 90))
                else:
                    if data['user']['ranking'] == "Bronze":
                        star_ = 'star_bronze'

                    if data['user']['ranking'] == "Silver":
                        star_ = 'star_silver'

                    if data['user']['ranking'] == "Gold":
                        star_ = 'star_gold'

                    if user == ctx.guild.owner:
                        star_ = "star_pink"

                    if position < 11:
                        star_ = "star_greem"

                    if user.id in self.bot.staff:
                        star_ = "star_blue"

                    if n <= data['user']['stars']:
                        star = star_
                    else:
                        star = 'star_default'
                    champion[n - 1] = Image.open(f'images/elements/{star}.png').convert('RGBA')
                    champion[n - 1] = champion[n - 1].resize((130, 90))
            else:
                star_ = 'star_default'
                champion[n - 1] = Image.open(f'images/elements/{star_}.png').convert('RGBA')
                champion[n - 1] = champion[n - 1].resize((130, 90))

        # guild image
        guild_ = self.bot.get_guild(data['guild_id'])
        if guild_ is not None:
            if validate_url(str(guild_.icon_url)):
                link = str(guild_.icon_url)
            else:
                link = "https://festsonho.com.br/images/sem_foto.png"
            url_guild = await requests.get(link)
            icon_guild = Image.open(BytesIO(await url_guild.read())).convert("RGBA")
            icon_guild = icon_guild.resize((190, 190))
        else:
            icon_guild = Image.open('images/elements/no_found.png').convert("RGBA")
            icon_guild = icon_guild.resize((190, 190))

        # load fonts
        font = ImageFont.truetype('fonts/bot.otf', 100)

        # User Align
        bounding_box = [150, 275, 2200, 375]
        x1, y1, x2, y2 = bounding_box
        img = Image.open('images/dashboards/rank.png').convert('RGBA')
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
        await ctx.send(file=discord.File('rank.png'))


def setup(bot):
    bot.add_cog(RankingClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mRANKING\033[1;32m foi carregado com sucesso!\33[m')
