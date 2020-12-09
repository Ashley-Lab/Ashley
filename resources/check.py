import re
import discord.utils

from config import data
from discord.ext import commands


def check_it(**kwargs):
    permissions = ('add_reactions', 'administrator', 'attach_files',
                   'ban_members', 'change_nickname' 'connect',
                   'create_instant_invite' 'deafen_members', 'embed_links',
                   'external_emojis', 'kick_members',
                   'manage_channels', 'manage_emojis', 'manage_guild',
                   'manage_messages', 'manage_nicknames',
                   'manage_roles', 'manage_webhooks', 'mention_everyone',
                   'move_members', 'mute_members',
                   'priority_speaker', 'read_message_history', 'read_messages',
                   'send_messages', 'send_tts_messages',
                   'speak', 'use_voice_activation', 'view_audit_log')

    async def check_permissions(ctx, perms_, *, check=all):
        r = ctx.author.guild_permissions
        return check(getattr(r, k, False) == v for k, v in perms_.items())

    def predicate(ctx):
        if ctx.message.webhook_id:
            return True

        if isinstance(ctx.message.channel, discord.DMChannel):
            if ctx.command.name in ["help", "ajuda"]:
                return True
            raise commands.NoPrivateMessage(
                '<:alert:739251822920728708>│``Você não pode mandar comandos em mensagens privadas!``')

        if not isinstance(ctx.channel, discord.DMChannel) and \
            kwargs.get('is_nsfw', False) == ctx.channel.is_nsfw():

            raise commands.CheckFailure("<:alert:739251822920728708>│``Esse comando apenas pode ser usado"
                                            " em um canal`` **nsfw!!**")

        if ctx.author.id not in ctx.bot.staff and kwargs.get("is_owner", False):
            raise commands.CheckFailure("<:alert:739251822920728708>│``Apenas meu criador pode usar esse comando!``")

        if kwargs.get("check_role", False):
            roles = [r.name for r in ctx.author.roles]
            for role in kwargs.get("roles", []):
                if role not in roles:
                    raise commands.CheckFailure(
                        "<:alert:739251822920728708>│``Você precisa de um cargo "
                        "específico para usar esse comando!``")

        if kwargs.get('no_pm', False) or \
            kwargs.get('is_owner', False) or \
                kwargs.get('is_nsfw', False):

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
