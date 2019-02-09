import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


def perms_check(role):
    list_perms = ['empty']
    for perm in role:
        if perm[1] is True:
            if 'empty' in list_perms:
                list_perms = list()
            list_perms.append(perm[0])
    if 'empty' not in list_perms:
        all_perms = ", ".join(list_perms)
        return all_perms
    else:
        return "o cargo nao possui permissão"


class RoleInfo(object):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='roleinfo', aliases=['inforole'])
    async def roleinfo(self, ctx, *, role: commands.RoleConverter = None):
        if role is not None:
            embed = discord.Embed(color=color, description='**Informações do cargo:**')
            embed.add_field(name='`📋 | Nome:`', value=str(role))
            embed.add_field(name='`💻 | ID:`', value=str(role.id))
            embed.add_field(name='`🌈 | Cor:`', value=str(role.colour))
            embed.add_field(name='`📅 | Criado:`', value=str(role.created_at))
            embed.add_field(name='`🗃 | Permissões:`', value="```{}```".format(perms_check(role.permissions)))
            await ctx.send(embed=embed)
        else:
            await ctx.send('<:negate:520418505993093130>│``Você precisa colocar um cargo para ver as informações!``')


def setup(bot):
    bot.add_cog(RoleInfo(bot))
    print('\033[1;32mO comando \033[1;34mROLEINFO\033[1;32m foi carregado com sucesso!\33[m')
