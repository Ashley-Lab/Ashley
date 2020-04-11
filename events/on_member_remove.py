import discord

from discord.ext import commands

gif = ['https://media.giphy.com/media/fDO2Nk0ImzvvW/giphy.gif',
       'https://media.giphy.com/media/UrcXN0zTfzTPi/giphy.gif',
       'https://media.giphy.com/media/kGCuRgmbnO9EI/giphy.gif',
       'https://media.giphy.com/media/7DzlajZNY5D0I/giphy.gif',
       'https://media.giphy.com/media/KcHXmesyPXg6Q/giphy.gif']


class OnMemberRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        data = self.bot.db.get_data("guild_id", member.guild.id, "guilds")
        if data is not None:
            try:
                if data['func_config']['member_remove']:
                    canal = self.bot.get_channel(data['func_config']['member_remove_id'])
                    msg = discord.Embed(title='O membro {} Saiu do servidor {}!'.format(member, member.guild),
                                        color=self.color, description="Adeus {}, qualquer coisa é a mesma coisa e "
                                                                      "tudo é nenhuma!".format(member.name))
                    msg.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                    msg.set_thumbnail(url="{}".format(member.avatar_url))
                    msg.set_footer(text="Ashley ® Todos os direitos reservados.")
                    await canal.send(embed=msg)
            except AttributeError:
                pass
            except discord.errors.Forbidden:
                pass

            try:
                if data['func_config']['cont_users']:
                    numbers = ['<:0_:578615675182907402>', '<:1_:578615669487304704>', '<:2_:578615674109165568>',
                               '<:3_:578615683424976916>', '<:4_:578615679406833685>', '<:5_:578615684708171787>',
                               '<:6_:578617070309343281>', '<:7_:578615679041798144>', '<:8_:578617071521497088>',
                               '<:9_:578617070317469708>']
                    channel_ = self.bot.get_channel(data['func_config']['cont_users_id'])
                    if channel_ is None:
                        return
                    text = str(member.guild.member_count)
                    list_ = list()
                    for letter in text:
                        list_.append(numbers[int(letter)])
                    list_ = str(list_).replace('[', '').replace(']', '').replace(',', '.')
                    await channel_.edit(topic="<a:caralho:525105064873033764> **Membros:**  " + list_)
            except discord.Forbidden:
                pass

            try:
                if data['func_config']['join_system']:
                    pass
            except KeyError:
                data = self.bot.db.get_data("guild_id", member.guild.id, "guilds")
                update = data
                update['func_config']['join_system'] = False
                update['func_config']['join_system_id'] = None
                update['func_config']['join_system_role'] = None
                update['func_config']['join_system_member_state'] = dict()
                self.bot.db.update_data(data, update, 'guilds')


def setup(bot):
    bot.add_cog(OnMemberRemove(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_REMOVE\033[1;33m foi carregado com sucesso!\33[m')
