import json
import discord
import asyncio

from resources.translation import t_

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


async def create_pages(ctx, items, lfmt, description=None, title=None, author=None, author_url=None,
                       emotes=("\u2B05", "\u27A1", "\u274C"), thumbnail=None, footer=None, chunk=25):

    embed = discord.Embed(description=description, title=title, color=color)
    embed.set_author(name=author, icon_url=author_url)

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if footer:
        embed.set_footer(text=footer)

    items = {k: lfmt(v) for k, v in items}
    ctr = 0

    while any(len(v) > 500 for v in items.values()) and ctr < 10:
        additions = {}
        for k, v in items.items():
            if len(v) > 500:
                count = 0
                start = ""
                end = ""
                for item in v.split("\n"):
                    if count + len(item) > 500:
                        end += item + "\n"
                    else:
                        start += item + "\n"
                        count += len(item) + 1
                additions[k] = start.strip()
                if end.strip():
                    additions[k + " continua"] = end.strip()
        items.update(additions)
        ctr += 1
    i = 0
    ditems = items
    items = list(items.items())
    items.sort()

    chunks = []
    for j in range(0, len(items), chunk):
        chunks.append(items[j:j + chunk])

    for item, value in chunks[i]:
        embed.add_field(name=item, value=ditems[item])

    end = len(chunks) - 1

    msg = await ctx.send(embed=embed)
    for emote in emotes:
        await msg.add_reaction(emote)

    while True:
        try:
            r, u = await ctx.bot.wait_for("reaction_add", check=lambda r_, u_: r_.message.id == msg.id, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send(await t_(ctx, "Tempo esgotado, tente novamente...", "guilds"))
            await msg.delete()
            return

        if u == ctx.guild.me:
            continue

        if u != ctx.author or r.emoji not in emotes:
            try:
                await msg.remove_reaction(r.emoji, u)
            except discord.Forbidden:
                pass
            continue

        if r.emoji == emotes[0]:
            if i == 0:
                pass
            else:
                embed.clear_fields()
                i -= 1
                for item, value in chunks[i]:
                    embed.add_field(name=item, value=ditems[item])

                await msg.edit(embed=embed)

        elif r.emoji == emotes[1]:
            if i == end:
                pass
            else:
                embed.clear_fields()
                i += 1
                for item, value in chunks[i]:
                    embed.add_field(name=item, value=ditems[item])

                await msg.edit(embed=embed)
        else:
            await msg.delete()
            await ctx.send(await t_(ctx, "Fechando...", "guilds"))
            return

        try:
            await msg.remove_reaction(r.emoji, u)
        except discord.Forbidden:
            pass
