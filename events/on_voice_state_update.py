import json
import discord

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class VoiceClass(object):
    def __init__(self, bot):
        self.bot = bot

    async def on_voice_state_update(self, member, before, after):
        if member.guild is not None:
            data = self.bot.db.get_data("guild_id", member.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['member_voice_entered']:
                        if before.channel is None and after.channel is not None:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send = discord.Embed(
                                title=":star2: **Membro entrou em um canal de voz**",
                                color=color,
                                description=f"**Membro:** {member.name} entrou no canal {after.channel.mention}")
                            to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                            await canal.send(embed=to_send)
                    if data['log_config']['log'] and data['log_config']['member_voice_exit']:
                        if before.channel is not None and after.channel is None:
                            canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                            if canal is None:
                                return
                            to_send = discord.Embed(
                                title=":star2: **Membro saiu de um canal de voz**",
                                color=color,
                                description=f"**Membro:** {member.name} saiu do canal {after.channel.mention}")
                            to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                            await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(VoiceClass(bot))
    print('\033[1;32mO evento \033[1;34mVOICE_CLASS\033[1;32m foi carregado com sucesso!\33[m')
