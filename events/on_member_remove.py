import json
import discord

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)

gif = ['https://media.giphy.com/media/fDO2Nk0ImzvvW/giphy.gif',
       'https://media.giphy.com/media/UrcXN0zTfzTPi/giphy.gif',
       'https://media.giphy.com/media/kGCuRgmbnO9EI/giphy.gif',
       'https://media.giphy.com/media/7DzlajZNY5D0I/giphy.gif',
       'https://media.giphy.com/media/KcHXmesyPXg6Q/giphy.gif']


class OnMemberRemove(object):
    def __init__(self, bot):
        self.bot = bot

    async def on_member_remove(self, member):

        data = self.bot.db.get_data("guild_id", member.guild.id, "guilds")
        if data is not None:

            try:
                if data['func_config']['member_remove']:
                    canal = self.bot.get_channel(data['func_config']['member_remove_id'])
                    msg = discord.Embed(title='O membro {} Saiu do servidor {}!'.format(member, member.guild),
                                        color=color, description="Adeus {}, qualquer coisa é a mesma coisa e "
                                                                 "tudo é nenhuma!".format(member.name))
                    msg.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                    msg.set_thumbnail(url="{}".format(member.avatar_url))
                    msg.set_footer(text="Ashley ® Todos os direitos reservados.")
                    await canal.send(embed=msg)
            except AttributeError:
                pass
            except discord.errors.Forbidden:
                pass

            if data['func_config']['cont_users']:
                numbers = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
                channel_ = self.bot.get_channel(data['func_config']['cont_users_id'])
                if channel_ is None:
                    return
                text = str(member.guild.member_count)
                for n in range(0, 10):
                    text = text.replace(str(n), numbers[n])
                await channel_.edit(topic="Membros: " + text)


def setup(bot):
    bot.add_cog(OnMemberRemove(bot))
    print('\033[1;32mO evento \033[1;34mMEMBER_REMOVE\033[1;32m foi carregado com sucesso!\33[m')
