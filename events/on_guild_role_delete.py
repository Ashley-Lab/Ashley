import json
import discord

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class RoleDelete(object):
    def __init__(self, bot):
        self.bot = bot

    async def on_guild_role_delete(self, role):
        if role.guild is not None:
            data = self.bot.db.get_data("guild_id", role.guild.id, "guilds")
            if data is not None:
                try:
                    if data['log_config']['log'] and data['log_config']['role_deleted']:
                        canal = self.bot.get_channel(data['log_config']['log_channel_id'])
                        if canal is None:
                            return
                        to_send = discord.Embed(
                            title=":put_litter_in_its_place: **Cargo Deletado**",
                            color=color,
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
    bot.add_cog(RoleDelete(bot))
    print('\033[1;32mO evento \033[1;34mROLE_DELETE\033[1;32m foi carregado com sucesso!\33[m')
