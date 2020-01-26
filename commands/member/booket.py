import discord
import requests

from random import choice
from io import BytesIO
from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from PIL import Image, ImageDraw, ImageOps


class Booket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True, is_nsfw=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='bok', aliases=['booket'])
    async def bok(self, ctx, member: discord.Member = None):
        if member is not None:
            data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
            data_member = self.bot.db.get_data("user_id", member.id, "users")
            if data_member is None:
                return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                      '``esse usuário não está cadastrado!``', delete_after=5.0)
            if member.id == ctx.author.id:
                return await ctx.send('<:negate:520418505993093130>│``VOCE NÃO PODE FAZER SEXO COM VOCÊ MESMO! ISSO '
                                      'SERIA MASTUBARÇÃO...``')

            if data_user['user']['married'] is True and data_member['user']['married'] is True:
                if data_user['user']['married_at'] == member.id and data_member['user']['married_at'] == ctx.author.id:
                    img_ = choice(['images/married/bokfb2.png', 'images/married/bokfb1.png'])
                    original = Image.open(img_).convert('RGBA')
                    original = original.resize((992, 1402))
                    original.save('marrysend.png')
                    mens = member
                    alvo = member.avatar_url
                    autor = ctx.author.avatar_url
                    lista = [[autor, alvo], [427, 290, 190, 208, 237, 200],
                             [(18, 98), (580, 142), (140, 744), (656, 753), (164, 1076), (652, 1078)]]
                    for c in range(6):
                        if c == 0:
                            avatarurl = requests.get(lista[0][0])
                        else:
                            avatarurl = requests.get(lista[0][1])
                        avatar = Image.open(BytesIO(avatarurl.content)).convert('RGBA')
                        avatar = avatar.resize((lista[1][c], lista[1][c]))
                        big_avatar = (avatar.size[0] * 3, avatar.size[1] * 3)
                        mascara = Image.new('L', big_avatar, 0)
                        trim = ImageDraw.Draw(mascara)
                        trim.ellipse((0, 0) + big_avatar, fill=255)
                        mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
                        avatar.putalpha(mascara)
                        exit_avatar = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
                        exit_avatar.putalpha(mascara)
                        exit_avatar.save('avatar.png')
                        img = Image.open('marrysend.png')
                        img.paste(avatar, lista[2][c], avatar)
                        img.save('marrysend.png')

                    await ctx.send('O casal {} e {} acabam de trocar alguns carinhos orais... '
                                   ':smirk: :flushed:'.format(ctx.author.mention, mens.mention),
                                   file=discord.File('marrysend.png'))
                else:
                    await ctx.send("<:negate:520418505993093130>│``VOCÊ NÃO ESTÁ CASADO COM ESSA PESSOA!``")
            elif data_member['user']['married'] is False:
                return await ctx.send('<:negate:520418505993093130>│``ELE(A) NÃO ESTA CASADO(A)!``')
            else:
                return await ctx.send('<:negate:520418505993093130>│``VOCE NÃO ESTA CASADO(A)!``')
        else:
            return await ctx.send('<:oc_status:519896814225457152>│``Você precisa mensionar alguem.``')


def setup(bot):
    bot.add_cog(Booket(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mBOOKET\033[1;32m foi carregado com sucesso!\33[m')
