import json
import discord

from discord.ext import commands

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class ChannelPinUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        if channel.guild is not None:
            data = self.bot.db.get_data("guild_id", channel.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['channel_edit']:
                        canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                        if canal is None:
                            return
                        if last_pin is not None:
                            fix_ = 'fixada'
                            time_ = '\n em: ' + str(last_pin)
                        else:
                            fix_ = 'desfixada'
                            time_ = '\n'
                        to_send = discord.Embed(
                            title=f":bangbang: **Uma mensagem foi {fix_}**",
                            color=color,
                            description=f"**Canal de texto:** {channel.name} {time_}")
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(ChannelPinUpdate(bot))
    print('\033[1;32mO evento \033[1;34mCHANNEL_PINS_UPDATE\033[1;32m foi carregado com sucesso!\33[m')
