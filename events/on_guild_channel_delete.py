import discord

from discord.ext import commands


class ChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if channel.guild is not None:
            data = await self.bot.db.get_data("guild_id", channel.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['channel_deleted']:
                        canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                        if canal is None:
                            return
                        to_send = discord.Embed(
                            title=":put_litter_in_its_place: **Canal de texto deletado**",
                            color=self.color,
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
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mCHANNEL_DELETE\033[1;33m foi carregado com sucesso!\33[m')
