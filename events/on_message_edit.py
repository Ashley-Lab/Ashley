import discord

from discord.ext import commands


class OnMessageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        if before.content == after.content:
            return

        data = await self.bot.db.get_data("guild_id", after.guild.id, "guilds")

        if not data:
            return

        data = data['log_config']

        if data['log'] and data['msg_edit']:
            canal = self.bot.get_channel(data['log_channel_id'])

            if not canal:
                return

            embed = discord.Embed(color=self.color, title=f":pencil: {after.author} **editou uma mensagem de texto**",
                                  description=f"**Canal de texto:** {after.channel.mention}")

            embed.add_field(name="**Antiga mensagem:**",
                            value=f"```{before.content}```")
            embed.add_field(name="**Nova mensagem:**",
                            value=f"```{after.content}```")

            embed.set_author(name=after.author, icon_url=after.author.avatar_url)
            embed.set_thumbnail(url=after.author.avatar_url)
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")

            ashley = canal.guild.get_member(self.bot.user.id)
            perms = canal.permissions_for(ashley)
            if perms.send_messages or perms.read_messages:
                if not perms.embed_links or not perms.attach_files:
                    await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                     "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                     " CORRETAMENTE!**")
                else:
                    await canal.send(embed=embed)


def setup(bot):
    bot.add_cog(OnMessageEdit(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_EDIT\033[1;33m foi carregado com sucesso!\33[m')
