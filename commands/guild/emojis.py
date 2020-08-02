import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class AllEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.command(name='emojis', aliases=['emoji'])
    async def emojis(self, ctx):
        """comando usado pra gerar uma lista dos emojis da sua guild
        Use ash emojis"""
        try:
            emojis_list = [str(x) for x in ctx.message.guild.emojis]
            num = len(emojis_list)
            if num <= 50:
                emojis_1 = ""
                for emoji in emojis_list[:int(num / 2)]:
                    emojis_1 += "".join(emoji)
                emojis_2 = ""
                for emoji in emojis_list[int(num / 2):]:
                    emojis_2 += "".join(emoji)
                embed1 = discord.Embed(colour=self.color)
                embed1.add_field(name="Emojis [ PARTE 1 ]", value=emojis_1)
                embed1.add_field(name="Emojis [ PARTE 2 ]", value=emojis_2)
                await ctx.send(embed=embed1)
            else:
                emojis_1 = ""
                for emoji in emojis_list[:int(num / 4)]:
                    emojis_1 += "".join(emoji)
                emojis_2 = ""
                for emoji in emojis_list[int(num / 4):int(num / 2)]:
                    emojis_2 += "".join(emoji)
                emojis_3 = ""
                for emoji in emojis_list[int(num / 2):int(num / 2)+int(num / 4)]:
                    emojis_3 += "".join(emoji)
                emojis_4 = ""
                for emoji in emojis_list[int(num / 2)+int(num / 4):]:
                    emojis_4 += "".join(emoji)
                embed1 = discord.Embed(colour=self.color)
                embed1.add_field(name="Emojis [ PARTE 1 ]", value=emojis_1)
                embed1.add_field(name="Emojis [ PARTE 2 ]", value=emojis_2)
                embed1.add_field(name="Emojis [ PARTE 3 ]", value=emojis_3)
                embed1.add_field(name="Emojis [ PARTE 4 ]", value=emojis_4)
                await ctx.send(embed=embed1)
        except discord.errors.HTTPException:
            await ctx.send('<:negate:721581573396496464>|``Você não tem emojis em seu servidor!``')


def setup(bot):
    bot.add_cog(AllEmoji(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mEMOJIS\033[1;32m foi carregado com sucesso!\33[m')
