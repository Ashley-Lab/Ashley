import discord

from discord.ext import commands


class RoleCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        data = await self.bot.db.get_data("guild_id", role.guild.id, "guilds")

        if not data:
            return

        data = data['log_config']

        if data['log'] and data['role_created']:
            canal = self.bot.get_channel(data['log_channel_id'])

            if not canal:
                return

            embed = discord.Embed(color=self.bot.color,
                                  title=":star2: **Cargo Criado**",
                                  description=f"**Cargo:** {role.mention}")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")

            await canal.send(embed=embed)


def setup(bot):
    bot.add_cog(RoleCreate(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mROLE_CREATE\033[1;33m foi carregado com sucesso!\33[m')
