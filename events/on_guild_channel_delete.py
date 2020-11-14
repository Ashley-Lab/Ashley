import discord

from discord.ext import commands


class ChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        data = await self.bot.db.get_data("guild_id", channel.guild.id, "guilds")

        if not data:
            return

        data = data['log_config']

        if data['log'] and data['channel_deleted']:
            canal = self.bot.get_channel(data['log_channel_id'])

            if not canal:
                return

            embed = discord.Embed(color=self.bot.color,
                                  title=":put_litter_in_its_place: **Canal de texto deletado**",
                                  description=f"**Canal de texto:** ``{channel.name}``")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")

            await canal.send(embed=embed)


def setup(bot):
    bot.add_cog(ChannelDelete(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mCHANNEL_DELETE\033[1;33m foi carregado com sucesso!\33[m')
