import discord

from discord.ext import commands


class ChannelUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.guild is not None:
            data = await self.bot.db.get_data("guild_id", before.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['channel_edit_name']:
                        if before.name != after.name:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send = discord.Embed(
                                title=":star2: **Canal de Texto Editado**",
                                color=self.color,
                                description=f"**Canal de texto:** {before.name}")
                            to_send.add_field(name='Nome Antigo', value=f'**{before.name}**')
                            to_send.add_field(name='Nome Novo', value=f'**{after.name}**')
                            to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                            ashley = canal.guild.get_member(self.bot.user.id)
                            perms = canal.permissions_for(ashley)
                            if perms.send_messages or perms.read_messages:
                                if not perms.embed_links or not perms.attach_files:
                                    await ctx.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                   "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                   " CORRETAMENTE!**")
                                else:
                                    await canal.send(embed=to_send)
                    if data['log_config']['log'] and data['log_config']['channel_edit_topic']:
                        if before.topic != after.topic:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send = discord.Embed(
                                title=":star2: **Canal de Texto Editado**",
                                color=self.color,
                                description=f"**Canal de texto:** {before.name}")
                            to_send.add_field(name='Tópico Antigo', value=f'**{before.topic}**')
                            to_send.add_field(name='Tópico Novo', value=f'**{after.topic}**')
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
    bot.add_cog(ChannelUpdate(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mCHANNEL_UPDATE\033[1;33m foi carregado com sucesso!\33[m')
