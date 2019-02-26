import json
import discord

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class ChannelDelete(object):
    def __init__(self, bot):
        self.bot = bot

    async def on_guild_channel_delete(self, channel):
        if channel.guild is not None:
            data = self.bot.db.get_data("guild_id", channel.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['channel_deleted']:
                        canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                        if canal is None:
                            return
                        to_send = discord.Embed(
                            title=":put_litter_in_its_place: **Canal de texto deletado**",
                            color=color,
                            description=f"**Canal de texto:** ``{channel.name}``")
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(ChannelDelete(bot))
    print('\033[1;32mO evento \033[1;34mCHANNEL_DELETE\033[1;32m foi carregado com sucesso!\33[m')
