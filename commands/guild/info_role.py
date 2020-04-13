import discord
import asyncio

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


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


class RoleInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='roleinfo', aliases=['inforole', 'ri', 'ir'])
    async def roleinfo(self, ctx, *, role: commands.RoleConverter = None):
        if not role:
            await ctx.send('<:negate:520418505993093130>│``Você precisa colocar um cargo para ver as informações!``')

        created_at = role.created_at.strftime("%d %b %Y %H:%M")
        perms_channel = perms_check(role.permissions)
        _bool = {True: "Sim", False: "Não"}
        color_hex = "#{:02x}{:02x}{:02x}".format(role.colour.r, role.colour.g, role.colour.b)

        role_txt = f"▫**ID:** {role.id}\n" \
                   f"▫**Número de membros:** {len(role.members)}\n" \
                   f'▫**Criado em:** {role.created_at.strftime("%d de %B de %Y às %H:%M")} ({created_at})\n' \
                   f"▫**Posição:** {ctx.guild.roles[::-1].index(role) + 1}º / {len(ctx.guild.roles)}\n" \
                   f"▫**Separado?** {_bool[role.hoist]}\n" \
                   f"▫**Mencionável?** {_bool[role.mentionable]}\n" \
                   f"▫**Cor (rgb):** {role.colour.to_rgb()}\n" \
                   f"▫**Cor (hex):** {color_hex.upper()}\n" \
                   f"▫**Gerenciado?** {_bool[role.managed]}\n" \
                   f"\n▫**Permissões no servidor:**\n`{perms_channel}`\n"

        members_list = []
        list_ = ['']
        count = 0

        for member in ctx.guild.members:
            if role.id in [role.id for role in member.roles]:
                if not list_[0]:
                    if str(member.status) == "offline":
                        list_[0] = f"\n{member.name}#{member.discriminator}\n"
                    else:
                        list_[0] = f"\n{member.mention} \n"
                else:
                    if str(member.status) == "offline":
                        list_[0] = f"{list_[0]}{member.name}#{member.discriminator} \n"
                    else:
                        list_[0] = f"{list_[0]}{member.mention} \n"
                if not count == 20:
                    count += 1
                else:
                    count -= count
                    members_list.append(list_[0])
                    list_[0] = ''

        if list_[0]:
            members_list.append(list_[0])

        members_list.insert(0, role_txt)
        index = 0

        def embed_content():
            if index:
                embed_msg = discord.Embed(description=f'membros com o cargo {role.mention}\n{members_list[index]}',
                                          color=role.colour)
            else:
                embed_msg = discord.Embed(
                    description=f"__**Informações do cargo:**__ **{role.mention}**\n\n{members_list[0]}",
                    color=role.colour)
            embed_msg.set_author(name=f"Página {index + 1}/{len(members_list)}", icon_url=ctx.guild.icon_url)
            return embed_msg

        msg = await ctx.send(embed=embed_content())

        if len(members_list) == 1:
            return

        await msg.add_reaction('⬅')
        await msg.add_reaction('➡')

        try:
            while True:

                def check_reaction(r, u):
                    return r.message.id == msg.id and u.id == ctx.author.id

                done, pending = await asyncio.wait([
                    ctx.bot.wait_for('reaction_remove', check=check_reaction),
                    ctx.bot.wait_for('reaction_add', check=check_reaction)],
                    return_when=asyncio.FIRST_COMPLETED, timeout=60)

                if not done:
                    break

                reaction, user = done.pop().result()

                for future in pending:
                    future.cancel()

                if reaction.emoji == '⬅':
                    if index == 0:
                        index += len(members_list) - 1
                    else:
                        index -= 1
                    await msg.edit(embed=embed_content())

                elif reaction.emoji == '➡':
                    if index == len(members_list) - 1:
                        index -= len(members_list) - 1
                    else:
                        index += 1
                    await msg.edit(embed=embed_content())
                else:
                    try:
                        await msg.remove_reaction(reaction.emoji, member=user)
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
                    except discord.HTTPException:
                        pass
        except asyncio.TimeoutError:
            return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                  ' CANCELADO**')


def setup(bot):
    bot.add_cog(RoleInfo(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mROLEINFO\033[1;32m foi carregado com sucesso!\33[m')
