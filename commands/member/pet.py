import discord

from resources.color import random_color
from discord import Embed
from discord.ext import commands
from resources.webhook import WebHook
from datetime import datetime
from resources.check import check_it
from resources.db import Database
from random import choice
from resources.utility import get_content


class Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='pet', aliases=['p'])
    async def pet(self, ctx, *, msg: str = "Oiiiii"):
        """Comando usado pra se comunicar com pet
        Use ash pet <pergunta ou qualquer besteira>"""
        try:
            pet_n = choice(list(self.bot.pets.keys()))
            pet = self.bot.pets[pet_n]
            if pet['colour'][0] is True:
                pet_c = choice(pet['colour'][2])
                indice = pet['colour'][2].index(pet_c)
                mask = choice(self.letters[:pet['mask'][indice]])
                link_ = f'images/pet/{pet_n}/{pet_c}/mask_{mask}.png'
            else:
                mask = choice(self.letters[:pet['mask'][0]])
                link_ = f'images/pet/{pet_n}/mask_{mask}.png'

            avatar = open(link_, 'rb')
            web_hook_ = await ctx.channel.create_webhook(name=pet_n, avatar=avatar.read())
            if 'a_' in web_hook_.avatar:
                format_1 = '.gif'
            else:
                format_1 = '.webp'
            web_hook = WebHook(url=web_hook_.url)
            web_hook.embed = Embed(
                colour=random_color(),
                description=f"```{get_content(msg.lower())}```",
                timestamp=datetime.utcnow()
            ).set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url
            ).set_thumbnail(
                url=f'https://cdn.discordapp.com/avatars/{web_hook_.id}/{web_hook_.avatar}{format_1}?size=1024'
            ).to_dict()
            web_hook.send_()
            await web_hook_.delete()
        except discord.Forbidden:
            await ctx.send("<:oc_status:519896814225457152>│``Não tenho permissão de gerenciar WEBHOOKS nesse "
                           "servidor.``")


def setup(bot):
    bot.add_cog(Pet(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPET\033[1;32m foi carregado com sucesso!\33[m')
