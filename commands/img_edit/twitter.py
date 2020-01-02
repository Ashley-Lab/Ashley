import random
import discord
import requests

from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from resources.check import check_it
from resources.db import Database


class TwitterClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='twitter', aliases=['tt'])
    async def twitter(self, ctx, *, resp):
        if resp is None:
            return await ctx.send('<:negate:520418505993093130>│``DIGITE ALGO PARA EU POSTAR``')

        rede = [[23, (18, 15)], [(296, 149), (17, 120)],
                [['', (14, 48), 14], ['', (49, 16), 10], ['', (49, 29), 8]], 36, 3]

        msg = await ctx.send('<a:loading:520418506567843860>│``Processando...``')

        cont = 0
        list_ = resp.split()
        resp = ''
        for c in list_:
            if len(c)+cont >= rede[3]:
                cont = 0
                resp = '{}{}{}'.format(resp, '''
''', c)
                if len(c) > rede[3]:
                    resp = ' {}-{} {}'.format(c[:rede[3]], '''
''', c[rede[3]:])
                    cont = len(c)-rede[3]
            else:
                resp = '{} {}'.format(resp, c)
                cont += len(c)
        if resp.count('''
''') > rede[4]:
            await ctx.send('<:alert_status:519896811192844288>│``Sua mensagem foi muito grande!``')
        else:
            avatarurl = requests.get(ctx.author.avatar_url_as(format="png"))
            avatar = Image.open(BytesIO(avatarurl.content))
            avatar = avatar.resize((rede[0][0], rede[0][0]))
            big_avatar = (avatar.size[0] * 3, avatar.size[1] * 3)
            mascara = Image.new('L', big_avatar, 0)
            trim = ImageDraw.Draw(mascara)
            trim.ellipse((0, 0) + big_avatar, fill=255)  # opacidade
            mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mascara)
            exit_avatar = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
            exit_avatar.putalpha(mascara)
            avatar = exit_avatar

            imgurl = random.choice(['https://i.imgur.com/2Owhe1y.jpg',
                                    'https://i.imgur.com/pFuPCUE.jpg',
                                    'https://i.imgur.com/0lnhQR9.jpg',
                                    'https://i.imgur.com/mbigFXD.jpg',
                                    'https://i.imgur.com/SL0AZr3.jpg',
                                    'https://i.imgur.com/vj6hIvx.jpg',
                                    'https://i.imgur.com/wMjySPZ.png',
                                    'https://i.imgur.com/GCrHCm4.jpg',
                                    'https://i.imgur.com/caVly1I.jpg',
                                    'https://i.imgur.com/DI3MnVF.jpg',
                                    'https://i.imgur.com/I1oFR7s.jpg',
                                    'https://i.imgur.com/i1TjXts.jpg',
                                    'https://i.imgur.com/IVzCAgX.jpg',
                                    'https://i.imgur.com/AgX0ebq.jpg',
                                    'https://i.imgur.com/ZxUEnnm.jpg',
                                    'https://i.imgur.com/a34fK0P.jpg',
                                    'https://i.imgur.com/JdufgXh.jpg',
                                    'https://i.imgur.com/4bUx6IE.jpg',
                                    'https://i.imgur.com/VXxGrIT.jpg',
                                    'https://i.imgur.com/Kn1yIcC.jpg',
                                    'https://i.imgur.com/YllNI2J.jpg',
                                    'https://i.imgur.com/HI6Qmig.jpg',
                                    'https://i.imgur.com/Nmnx7E8.jpg',
                                    'https://i.imgur.com/A9ZvUzz.jpg',
                                    'https://i.imgur.com/mSPiRMA.jpg',
                                    'https://i.imgur.com/EQV5IS3.jpg',
                                    'https://i.imgur.com/sY76YYa.jpg',
                                    'https://i.imgur.com/jGtn5Q2.jpg',
                                    'https://i.imgur.com/ncgHAFi.jpg',
                                    'https://i.imgur.com/U4UW8Tn.jpg',
                                    'https://i.imgur.com/YpK2xua.jpg',
                                    'https://i.imgur.com/r5ttJuB.jpg',
                                    'https://i.imgur.com/8wbwwV9.jpg',
                                    'https://i.imgur.com/zRc0LtN.jpg',
                                    'https://i.imgur.com/Q5USYEZ.png',
                                    'https://i.imgur.com/XVhh7oO.jpg',
                                    'https://i.imgur.com/vm109nQ.jpg',
                                    'https://i.imgur.com/yMH2IN0.png',
                                    'https://i.imgur.com/6UT2wFZ.jpg',
                                    'https://i.imgur.com/yjSl9fs.jpg',
                                    'https://i.imgur.com/OkSXZst.jpg',
                                    'https://i.imgur.com/Wuad8Zw.jpg',
                                    'https://i.imgur.com/crBWwqo.jpg',
                                    'https://i.imgur.com/QGBSogM.jpg',
                                    'https://i.imgur.com/IKSvnoK.jpg',
                                    'https://i.imgur.com/MNHiUjf.jpg',
                                    'https://i.imgur.com/TpOtHY6.png',
                                    'https://i.imgur.com/mBsvITd.jpg',
                                    'https://i.imgur.com/69PudmI.jpg',
                                    'https://i.imgur.com/Le1XrNv.jpg',
                                    'https://i.imgur.com/I2eCtiW.jpg'])

            imgurl = requests.get(imgurl)
            img = Image.open(BytesIO(imgurl.content))
            img = img.resize(rede[1][0])
            big_img = (img.size[0] * 3, img.size[1] * 3)
            mascara = Image.new('L', big_img, 0)
            trim = ImageDraw.Draw(mascara)
            trim.rectangle((0, 0) + big_img, fill=255)  # opacidade
            mascara = mascara.resize(img.size, Image.ANTIALIAS)
            img.putalpha(mascara)
            exit_img = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
            exit_img.putalpha(mascara)
            exit_img.save('img.png')

            um = rede[2][0][0]
            dois = rede[2][1][0]
            tres = rede[2][2][0]
            if rede[2][0][0] == '':
                rede[2][0][0] = resp
            if rede[2][1][0] == '':
                rede[2][1][0] = ctx.author
            if rede[2][2][0] == '':
                rede[2][2][0] = '@{}'.format(ctx.author)

            image = Image.open('images/social/twitter.png')
            escrita = ImageDraw.Draw(image)
            for c in (rede[2]):
                font = ImageFont.truetype('fonts/Arial.ttf', c[2])
                texto = str(c[0])
                escrita.text(xy=c[1], text=texto, fill=(10, 10, 10), font=font)
            image.paste(avatar, rede[0][1], avatar)
            image.paste(img, rede[1][1], img)
            image.save('social.png')
            await ctx.send(file=discord.File('social.png'))
            await msg.delete()
            rede[2][0][0] = um
            rede[2][1][0] = dois
            rede[2][2][0] = tres


def setup(bot):
    bot.add_cog(TwitterClass(bot))
    print('\033[1;32mO comando \033[1;34mTWITTERCLASS\033[1;32m foi carregado com sucesso!\33[m')
