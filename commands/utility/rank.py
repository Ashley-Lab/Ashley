import re
import discord
import operator
import unicodedata

from discord.ext import commands
from resources.db import Database
from resources.check import check_it
from PIL import Image, ImageDraw, ImageFont
from resources.img_edit import get_avatar
from random import choice


class RankingClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def remove_acentos_e_caracteres_especiais(word):
        # Unicode normalize transforma um caracter em seu equivalente em latin.
        nfkd = unicodedata.normalize('NFKD', word)
        palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

        # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
        return re.sub('[^a-zA-Z \\\]', '', palavra_sem_acento)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='rank', aliases=['r'])
    async def rank(self, ctx, member: discord.Member = None):
        """Mostra seu rank da Ashley
        Use ash rank"""
        if member is None:
            member = ctx.author

        data = await self.bot.db.get_data("user_id", member.id, "users")
        if data is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)

        msg = await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU PROCESSANDO SEU PEDIDO!``")

        # load dashboard image base
        background = {
            "01": "background_1",
            "02": "background_2",
            "03": "background_3",
            "04": "background_4",
            "05": "background_5",
            "06": "background_6",
            "07": "background_7",
            "08": "background_8",
            "09": "background_9",
            "10": "staffer",
            "11": "vip",
        }

        key_bg = choice(["01", "02", "03", "04", "05", "06", "07", "08", "09"])

        if data['rpg']['vip']:
            key_bg = "11"

        if member.id in self.bot.team:
            key_bg = "10"

        image = Image.open(f"images/rank/background/{background[key_bg]}.png").convert('RGBA')
        show = ImageDraw.Draw(image)

        # Rank Position Member
        async def rank_position(bot, member_now):
            data_ = await bot.db.get_all_data("users")
            dict_ = dict()
            for _ in data_:
                dict_[str(_.get('user_id'))] = _['user'].get('experience', 0)
            sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
            rank = [int(sorted_x[x][0]) for x in range(len(data_))]
            _position = int(rank.index(member_now.id)) + 1
            return _position

        # load dashboard image detail
        star = data['user']['stars']
        if star > 20:
            star = 20
        position = str(await rank_position(self.bot, member))
        stars_dashboard = Image.open(f'images/rank/star/star_{star}.png').convert('RGBA')
        image.paste(stars_dashboard, (0, 0), stars_dashboard)

        # Text Align
        def text_align(box, text, font_t):
            nonlocal show
            x1, y1, x2, y2 = box
            w, h = show.textsize(text.upper(), font=font_t)
            x = (x2 - x1 - w) // 2 + x1
            y = (y2 - y1 - h) // 2 + y1
            return x, y

        # rectangles' texts
        rectangles = {
            "avatar": [9, 8, 119, 142],
            "patent": [149, 59, 239, 145],
            "num": [220, 126, 238, 144],
            "top": [327, 64, 388, 93],
            "title": [263, 113, 390, 142],
            "name": [0, 160, 399, 191],
        }

        # add text to img
        for k in rectangles.keys():
            if k == "avatar":
                # take name of member
                avatar = await get_avatar(member.avatar_url_as(format="png"), 111, 135, True)
                image.paste(avatar, (rectangles[k][0], rectangles[k][1]), avatar)

            if k == "patent":
                # patent image
                patent = data['user']['patent']
                patent_img = Image.open('images/patente/{}.png'.format(patent)).convert('RGBA')
                patent_img = patent_img.resize((80, 80))
                image.paste(patent_img, (rectangles[k][0] + 5, rectangles[k][1] - 10), patent_img)

            if k == "num":
                patent = str(data['user']['patent'])
                font = ImageFont.truetype("fonts/bot.otf", 12)
                x_, y_ = text_align(rectangles[k], patent, font)
                show.text(xy=(x_, y_), text=patent.upper(), fill=(255, 255, 255), font=font)

            if k == "top":
                font = ImageFont.truetype("fonts/bot.otf", 28)
                x_, y_ = text_align(rectangles[k], position, font)
                show.text(xy=(x_, y_), text=position.upper(), fill=(0, 0, 0), font=font)

            if k == "title":
                if member.id in self.bot.team:
                    title = str("STAFF")
                else:
                    title = str("PLAYER")
                font = ImageFont.truetype("fonts/bot.otf", 28)
                x_, y_ = text_align(rectangles[k], title, font)
                show.text(xy=(x_, y_), text=title.upper(), fill=(0, 0, 0), font=font)

            if k == "name":
                nome = self.remove_acentos_e_caracteres_especiais(str(member))
                font = ImageFont.truetype("fonts/bot.otf", 38)
                x_, y_ = text_align(rectangles[k], nome, font)
                show.text(xy=(x_ + 1, y_ + 1), text=nome.upper(), fill=(0, 0, 0), font=font)
                show.text(xy=(x_, y_), text=nome.upper(), fill=(255, 255, 255), font=font)

        image.save('rank.png')
        await msg.delete()
        await ctx.send(file=discord.File('rank.png'))


def setup(bot):
    bot.add_cog(RankingClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mRANKING\033[1;32m foi carregado com sucesso!\33[m')
