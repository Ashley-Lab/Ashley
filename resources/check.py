import re
import json
import discord.utils

from discord.ext import commands
from .translation import t_

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

staff = [235937029106434048, 300592580381376513]


class NumberConverter(commands.Converter):
    async def convert(self, ctx, argument):
        argument = argument.replace(",", "").strip("$")
        if not argument.strip("-").replace(".", "").isdigit():
            raise commands.BadArgument(t_(ctx, "That is not a number!", "guilds"))
        if len(argument) > 10:
            raise commands.BadArgument(t_(ctx, "That number is much too big! Must be less than 999,999,999", "guilds"))
        return round(float(argument), 2)


class IntConverter(commands.Converter):
    async def convert(self, ctx, argument):
        argument = argument.replace(",", "").strip("$")
        if not argument.strip("-").replace(".", "").isdigit():
            raise commands.BadArgument(t_(ctx, "That is not a number!", "guilds"))
        if len(argument) > 10:
            raise commands.BadArgument(t_(ctx, "That number is much too big! Must be less than 999,999,999", "guilds"))
        return int(argument)


class ItemOrNumber(commands.Converter):
    async def convert(self, ctx, argument):
        f_argument = argument.replace(",", "").strip("$")
        if not f_argument.strip("-").replace(".", "").isdigit():
            if "x" in argument:
                item, n = argument.split("x")
                if n.isdigit():
                    return item, int(n)
            return argument
        if len(f_argument) > 10:
            raise commands.BadArgument(t_(ctx, "That number is much too big! Must be less than 999,999,999", "guilds"))
        return round(float(f_argument), 2)


def check_it(**kwargs):

    permissions = ('add_reactions', 'administrator', 'attach_files', 'ban_members', 'change_nickname' 'connect',
                   'create_instant_invite' 'deafen_members', 'embed_links', 'external_emojis', 'kick_members',
                   'manage_channels', 'manage_emojis', 'manage_guild', 'manage_messages', 'manage_nicknames',
                   'manage_roles', 'manage_webhooks', 'mention_everyone', 'move_members', 'mute_members',
                   'priority_speaker', 'read_message_history', 'read_messages', 'send_messages', 'send_tts_messages',
                   'speak', 'use_voice_activation', 'view_audit_log')

    async def check_permissions(ctx, perms_, *, check=all):
        resolved = ctx.author.guild_permissions
        return check(getattr(resolved, name, None) == value for name, value in perms_.items())

    def predicate(ctx):

        if isinstance(ctx.message.channel, (discord.DMChannel, discord.GroupChannel)):
            if ctx.command.name == "help" or ctx.command.name == "ajuda":
                return True
            else:
                raise commands.NoPrivateMessage(
                    t_(ctx, '<:negate:520418505993093130>│``Você não pode mandar comandos em '
                            'mensagens privadas!``', "guilds"))

        if not (isinstance(ctx.channel, (discord.DMChannel, discord.GroupChannel))) and kwargs.get('is_nsfw', False):
            if "nsfw" not in ctx.channel.name.casefold():
                raise commands.CheckFailure(t_(ctx, "<:negate:520418505993093130>│``Esse comando apenas pode ser usado"
                                                    " em um canal`` **nsfw!!**", "guilds"))

        if ctx.message.author.id == _auth['owner_id'] and kwargs.get('is_owner', False):
            pass
        elif ctx.message.author.id in staff and kwargs.get('is_owner', False):
            pass
        elif ctx.message.author.id != _auth['owner_id'] and kwargs.get('is_owner', False):
            raise commands.CheckFailure(t_(ctx, "<:negate:520418505993093130>│``Apenas meu criador pode usar esse "
                                                "comando!``", "guilds"))

        if kwargs.get("check_role", False):
            role = discord.utils.find(lambda r: r.name in kwargs.get("roles", []), ctx.author.roles)
            if role is None:
                raise commands.CheckFailure(t_(ctx, "<:negate:520418505993093130>│``Você precisa de um cargo "
                                                    "específico para usar esse comando!``", "guilds"))

        if kwargs.get('no_pm', False) or kwargs.get('is_owner', False) or kwargs.get('is_nsfw', False):
            perms = dict()
            for perm_ in kwargs.keys():
                if perm_ in permissions:
                    perms[perm_] = kwargs[perm_]
            return check_permissions(ctx, perms)
        return True

    return commands.check(predicate)


regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def validate_url(url):
    return bool(regex.fullmatch(url))
