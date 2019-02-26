import json
import discord

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class OnTypingClass(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_typing(channel, user, when):
        if channel.id == 546753700517904405:
            embed = discord.Embed(
                color=discord.Color.red(),
                description=f'Usuario: {user.mention}\n Quando: {when}')
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(OnTypingClass(bot))
    print('\033[1;32mO evento \033[1;34mON_TYPING\033[1;32m foi carregado com sucesso!\33[m')
