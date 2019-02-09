import discord
import textwrap

from discord.ext import commands
from random import choice
from resources.db import Database
from resources.ia_list import reflita, reflita_zueira
from PIL import Image, ImageDraw, ImageFont
from resources.check import check_it


class Reflection(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='reflect', aliases=['reflita'])
    async def reflect(self, ctx):
        image = Image.open('images/memes/reflita.png')
        draw = ImageDraw.Draw(image)
        message = choice(reflita)
        if 'zueira' in ctx.message.content:
            message = choice(reflita_zueira)
        msg = textwrap.wrap(message, width=25)
        font = ImageFont.truetype('fonts/text.ttf', 25)
        bounding_box = [310, 25, 620, 320]
        x1, y1, x2, y2 = bounding_box
        current_h = 250

        for line in msg:
            w, h = draw.textsize(line, font=font)
            x = (x2 - x1 - w) / 2 + x1
            y = (y2 - y1 - current_h) / 2 + y1
            draw.text((x, y), line, align='center', font=font)
            current_h -= h + 40

        draw.rectangle([x1, y1, x2, y2])
        image.save('reflita.png')
        await ctx.channel.send(file=discord.File('reflita.png'))


def setup(bot):
    bot.add_cog(Reflection(bot))
    print('\033[1;32mO comando \033[1;34mREFLITA\033[1;32m foi carregado com sucesso!\33[m')
