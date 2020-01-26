import discord

from discord.ext import commands


class RoleCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if role.guild is not None:
            data = self.bot.db.get_data("guild_id", role.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['role_created']:
                        canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                        if canal is None:
                            return
                        to_send = discord.Embed(
                            title=":star2: **Cargo Criado**",
                            color=self.color,
                            description=f"**Cargo:** {role.mention}")
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        await canal.send(embed=to_send)
                except AttributeError:
                    pass
                except discord.errors.HTTPException:
                    pass
                except TypeError:
                    pass


def setup(bot):
    bot.add_cog(RoleCreate(bot))
    print('\033[1;33m( * ) | O evento \033[1;34mROLE_CREATE\033[1;33m foi carregado com sucesso!\33[m')
