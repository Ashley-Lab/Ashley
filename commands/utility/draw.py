import discord

from random import choice
from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class DrawUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.command(name='draw', aliases=['sorteio'])
    async def draw(self, ctx):
        draw_member = choice(list(ctx.guild.members))
        member = discord.utils.get(ctx.guild.members, name="{}".format(draw_member.name))
        embed = discord.Embed(
            title="``Fiz o sorteio de um membro``",
            colour=self.color,
            description="Membro sorteado foi **{}**\n <a:palmas:520418512011788309>│``Parabens!!``".format(member)
        )
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DrawUsers(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mSORTEIO\033[1;32m foi carregado com sucesso!\33[m')
