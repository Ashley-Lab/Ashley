import discord

from random import choice
from discord.ext import commands

gif = ['https://media.giphy.com/media/bAmQn1R4V3owE/giphy.gif',
       'https://media.giphy.com/media/skVEP0BeduG4/giphy.gif',
       'https://media.giphy.com/media/3o7TKsJEd0lp7GNUpq/giphy.gif',
       'https://media.giphy.com/media/138CCLzEja7I3e/giphy.gif',
       'https://media.giphy.com/media/l3V0uEmPgKpjZH6ve/giphy.gif',
       'https://media.giphy.com/media/nRPxv0FVLQBJm/giphy.gif',
       'https://media.giphy.com/media/papraODOQ51yE/giphy.gif',
       'https://media.giphy.com/media/GncBDxr7YxsuQ/giphy.gif',
       'https://media.giphy.com/media/3ZZeiFwplAGlLxHNvQ/giphy.gif',
       'https://media.giphy.com/media/lq2WK9kzLTLos/giphy.gif']


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_member_join(self, member):

        data = self.bot.db.get_data("guild_id", member.guild.id, "guilds")
        if data is not None:
            if data['func_config']['member_join']:
                try:
                    if member.guild.system_channel is not None:
                        to_send = discord.Embed(
                            title="SEJA MUITO BEM VINDO AO SERVIDOR {}:".format(member.guild),
                            color=self.color,
                            description="{}, Eu sou o BOT oficial do(a) {}, qualquer coisa "
                                        "digite ``ash.ajuda`` que eu irei ajudar você com "
                                        "muito prazer!".format(member.name, member.guild))
                        to_send.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        to_send.set_thumbnail(url="{}".format(member.avatar_url))
                        to_send.set_image(url=choice(gif))
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        await member.guild.system_channel.send(embed=to_send)
                    else:
                        to_send = discord.Embed(
                            title="SEJA MUITO BEM VINDO AO SERVIDOR {}:".format(member.guild),
                            color=self.color,
                            description="{}, Eu sou o BOT oficial do(a) {}, qualquer coisa "
                                        "digite ``ash.ajuda`` que eu irei ajudar você com "
                                        "muito prazer!".format(member.name, member.guild))
                        to_send.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        to_send.set_thumbnail(url="{}".format(member.avatar_url))
                        to_send.set_image(url=choice(gif))
                        to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                        channel_ = self.bot.get_channel(data['func_config']['member_join_id'])
                        await channel_.send(embed=to_send)
                except discord.errors.Forbidden:
                    pass
                except AttributeError:
                    pass

            if data['func_config']['cont_users']:
                try:
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
                except discord.errors.Forbidden:
                    pass

            try:
                if self.bot.config['config']['default_guild'] == member.guild.id:
                    role = discord.utils.find(lambda r: r.name == "</Members>", member.guild.roles)
                    await member.add_roles(role)
                    channel_ = self.bot.get_channel(data['func_config']['member_join_id'])
                    embed = discord.Embed(
                        color=self.color,
                        description="<a:blue:525032762256785409>│``USE O COMANDO`` **ash cargos** ``PARA VOCE VER OS "
                                    "CARGOS DISPONIVEIS``")
                    await channel_.send(embed=embed)
                    await channel_.send(f"**OBS:** ``SE VOCÊ VEIO AQUI ATRAS DO VIP É SÓ USAR O COMANDO`` **ASH VIP**")
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
    bot.add_cog(OnMemberJoin(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_JOIN\033[1;33m foi carregado com sucesso!\33[m')
