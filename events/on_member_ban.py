import discord

from discord.ext import commands


class MemberBanClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        data = await self.bot.db.get_data("guild_id", guild.id, "guilds")

        if not data:
            return

        data = data["log_config"]

        if data['log'] and data['member_ban']:
            canal = self.bot.get_channel(data['log_channel_id'])

            if not canal:
                return

            embed = discord.Embed(color=self.color,
                                  title=":star2: **Membro Banido**",
                                  description=f"**Membro:** {user.name}")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")

            await canal.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberBanClass(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_BAN\033[1;33m foi carregado com sucesso!\33[m')
