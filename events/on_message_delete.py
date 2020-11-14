import discord

from discord.ext import commands


class OnMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id:
            return

        if message.guild is not None:
            data = await self.bot.db.get_data("guild_id", message.guild.id, "guilds")
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
                            color=self.color,
                            description=f"**Canal de texto:** {message.channel.mention}")
                        to_send.add_field(name="**Messagem**", value=f"```{message.content}```")
                        to_send.set_author(name=message.author, icon_url=message.author.avatar_url)
                        to_send.set_thumbnail(url=message.author.avatar_url)
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        ashley = canal.guild.get_member(self.bot.user.id)
                        perms = canal.permissions_for(ashley)
                        if perms.send_messages or perms.read_messages:
                            if not perms.embed_links or not perms.attach_files:
                                await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                 "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                 " CORRETAMENTE!**")
                            else:
                                await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except discord.errors.NotFound:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(OnMessageDelete(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_DELETE\033[1;33m foi carregado com sucesso!\33[m')
