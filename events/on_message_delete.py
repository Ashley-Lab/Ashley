import json
import discord

from discord.ext import commands

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class OnMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id:
            return

        if message.guild is not None:
            data = self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            if data is not None:

                try:
                    if data['log_config']['log'] and data['log_config']['msg_delete']:
                        canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                        if canal is None:
                            return
                        if message.author.bot:
                            return
                        to_send = discord.Embed(
                            title=":pencil: **Mensagem de texto deletada**",
                            color=color,
                            description=f"**Canal de texto:** {message.channel.mention}")
                        to_send.add_field(name="**Messagem**", value=f"```{message.content}```")
                        to_send.set_author(name=message.author, icon_url=message.author.avatar_url)
                        to_send.set_thumbnail(url=message.author.avatar_url)
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(OnMessageDelete(bot))
    print('\033[1;32mO evento \033[1;34mMEMBER_DELETE\033[1;32m foi carregado com sucesso!\33[m')
