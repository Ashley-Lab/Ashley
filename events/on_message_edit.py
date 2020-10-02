import discord

from discord.ext import commands


class OnMessageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.id == self.bot.user.id:
            return

        if after.guild is not None:
            data = await self.bot.db.get_data("guild_id", after.guild.id, "guilds")
            if data is not None:

                try:
                    if data['log_config']['log'] and data['log_config']['msg_edit']:
                        canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                        if canal is None:
                            return
                        if before.content == after.content:
                            return
                        if before.author.bot or after.author.bot:
                            return
                        to_send = discord.Embed(
                            title=f":pencil: {after.author} **editou uma mensagem de texto**",
                            color=self.color,
                            description=f"**Canal de texto:** {after.channel.mention}")
                        to_send.add_field(name="**Antiga mensagem:**", value=f"```{before.content}```")
                        to_send.add_field(name="**Nova mensagem:**", value=f"```{after.content}```")
                        to_send.set_author(name=after.author, icon_url=after.author.avatar_url)
                        to_send.set_thumbnail(url=after.author.avatar_url)
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except TypeError:
                    pass
                except discord.errors.NotFound:
                    pass
                except discord.errors.HTTPException:
                    pass


def setup(bot):
    bot.add_cog(OnMessageEdit(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_EDIT\033[1;33m foi carregado com sucesso!\33[m')
