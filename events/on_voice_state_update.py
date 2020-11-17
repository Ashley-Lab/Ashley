import discord

from discord.ext import commands


class VoiceClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild is not None:
            data = await self.bot.db.get_data("guild_id", member.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['member_voice_entered']:
                        if before.channel is None and after.channel is not None:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send = discord.Embed(
                                title=":point_right::microphone: **Membro entrou em um canal de voz**",
                                color=self.color,
                                description=f"**Membro:** {member.name} entrou no canal {after.channel.mention}")
                            to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                            ashley = canal.guild.get_member(self.bot.user.id)
                            perms = canal.permissions_for(ashley)
                            if perms.send_messages and perms.read_messages:
                                if not perms.embed_links or not perms.attach_files:
                                    await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                     "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                     " CORRETAMENTE!**")
                                else:
                                    await canal.send(embed=to_send)
                    if data['log_config']['log'] and data['log_config']['member_voice_exit']:
                        if before.channel is not None and after.channel is None:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send_ = discord.Embed(
                                title=":point_left::microphone: **Membro saiu de um canal de voz**",
                                color=self.color,
                                description=f"**Membro:** {member.name} saiu do canal {before.channel.mention}")
                            to_send_.set_footer(text="Ashley ® Todos os direitos reservados.")
                            ashley = canal.guild.get_member(self.bot.user.id)
                            perms = canal.permissions_for(ashley)
                            if perms.send_messages and perms.read_messages:
                                if not perms.embed_links or not perms.attach_files:
                                    await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                     "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                     " CORRETAMENTE!**")
                                else:
                                    await canal.send(embed=to_send_)
                    if data['log_config']['log'] and data['log_config']['member_voice_entered']:
                        if data['log_config']['log'] and data['log_config']['member_voice_exit']:
                            if before.channel is not None and after.channel is not None:
                                if before.channel != after.channel:
                                    canal_ = self.bot.get_channel(data['log_config']['log_channel_id'])
                                    if canal_ is None:
                                        return
                                    to_send_ = discord.Embed(
                                        title=":point_left::microphone: **Membro trocou de um canal de voz**",
                                        color=self.color,
                                        description=f"**Membro:** {member.name} saiu do canal {before.channel.mention}"
                                        f" e entrou no canal {after.channel.mention}")
                                    to_send_.set_footer(text="Ashley ® Todos os direitos reservados.")
                                    ashley = canal_.guild.get_member(self.bot.user.id)
                                    perms = canal_.permissions_for(ashley)
                                    if perms.send_messages and perms.read_messages:
                                        if not perms.embed_links or not perms.attach_files:
                                            await canal_.send(
                                                "<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                " CORRETAMENTE!**")
                                        else:
                                            await canal_.send(embed=to_send_)
                except AttributeError:
                    pass
                except discord.errors.NotFound:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(VoiceClass(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mVOICE_CLASS\033[1;33m foi carregado com sucesso!\33[m')
