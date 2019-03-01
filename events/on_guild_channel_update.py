import json
import discord

from discord.ext import commands

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class ChannelUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.guild is not None:
            data = self.bot.db.get_data("guild_id", before.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['channel_edit_name']:
                        if before.name != after.name:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send = discord.Embed(
                                title=":star2: **Canal de Texto Editado**",
                                color=color,
                                description=f"**Canal de texto:** {before.name}")
                            to_send.add_field(name='Nome Antigo', value=f'**{before.name}**')
                            to_send.add_field(name='Nome Novo', value=f'**{after.name}**')
                            to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                            await canal.send(embed=to_send)
                    if data['log_config']['log'] and data['log_config']['channel_edit_topic']:
                        if before.topic != after.topic:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send = discord.Embed(
                                title=":star2: **Canal de Texto Editado**",
                                color=color,
                                description=f"**Canal de texto:** {before.name}")
                            to_send.add_field(name='Tópico Antigo', value=f'**{before.topic}**')
                            to_send.add_field(name='Tópico Novo', value=f'**{after.topic}**')
                            to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                            await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(ChannelUpdate(bot))
    print('\033[1;32mO evento \033[1;34mCHANNEL_UPDATE\033[1;32m foi carregado com sucesso!\33[m')
