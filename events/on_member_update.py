import json
import discord

from discord.ext import commands

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class MemberUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild is not None:
            data = self.bot.db.get_data("guild_id", before.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['member_edit_nickname']:
                        if before.name != after.name:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send = discord.Embed(
                                title=":star2: **Nome de usuário alterado**",
                                color=color,
                                description=f"**membro:** {before.name}")
                            to_send.add_field(name='Nome Antigo', value=f'**{before.name}**')
                            to_send.add_field(name='Nome Novo', value=f'**{after.name}**')
                            to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                            await canal.send(embed=to_send)
                    if data['log_config']['log'] and data['log_config']['member_edit_avatar']:
                        if before.avatar != after.avatar:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            if 'a_' in before.avatar:
                                format_1 = '.gif'
                            else:
                                format_1 = '.webp'
                            if 'a_' in after.avatar:
                                format_2 = '.gif'
                            else:
                                format_2 = '.webp'
                            to_send = discord.Embed(
                                title=":star2: **Avatar de usuário alterado**",
                                color=color,
                                description=f"**Membro:** {before.name}")
                            to_send.set_thumbnail(url=f'https://cdn.discordapp.com/avatars/{before.id}/{before.avatar}'
                                                      f'{format_1}?size=1024')
                            to_send.set_image(url=f'https://cdn.discordapp.com/avatars/{after.id}/{after.avatar}'
                                                  f'{format_2}?size=1024')
                            to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                            await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(MemberUpdate(bot))
    print('\033[1;32mO evento \033[1;34mMEMBER_UPDATE\033[1;32m foi carregado com sucesso!\33[m')
