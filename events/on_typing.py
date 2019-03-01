import json
import discord

from discord.ext import commands

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class OnTypingClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if channel.id == 546753700517904405:
            embed = discord.Embed(
                color=color,
                description=f'Usuario: {user.mention}\n Quando: {when}')
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(OnTypingClass(bot))
    print('\033[1;32mO evento \033[1;34mON_TYPING\033[1;32m foi carregado com sucesso!\33[m')
