import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class VoteClass(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='vote', aliases=['voto'])
    async def vote(self, ctx, *, msg: str = None):
        if msg is None:
            return await ctx.send('<:negate:520418505993093130>│``Você precisa falar o motivo da enquete de votação!``')
        vote = discord.Embed(
            title="Votação",
            color=color,
            description='O que vocês acham sobre: {} '.format(msg)
        )
        vote.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        vote.set_footer(text="Ashley ® Todos os direitos reservados.")
        vote = await ctx.channel.send(embed=vote)
        await vote.add_reaction("✅")
        await vote.add_reaction("❎")


def setup(bot):
    bot.add_cog(VoteClass(bot))
    print('\033[1;32mO comando \033[1;34mVOTECLASS\033[1;32m foi carregado com sucesso!\33[m')
