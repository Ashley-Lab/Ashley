import discord

from discord.ext import commands


class OnTypingClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if channel.id == 546753700517904405:
            embed = discord.Embed(
                color=self.color,
                description=f'Usuario: {user.mention}\n Quando: {when}')
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(OnTypingClass(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mON_TYPING\033[1;33m foi carregado com sucesso!\33[m')
