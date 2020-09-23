import discord

from discord.ext import commands


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @commands.Cog.listener()
    async def on_member_join(self, member):

        data = await self.bot.db.get_data("guild_id", member.guild.id, "guilds")
        if data is not None:
            if data['func_config']['member_join']:
                try:
                    to_send = discord.Embed(
                        title="SEJA MUITO BEM VINDO AO SERVIDOR {}:".format(member.guild),
                        color=self.color,
                        description="{}, Eu sou o BOT oficial do(a) {}, qualquer coisa "
                                    "digite ``ash.ajuda`` que eu irei ajudar você com "
                                    "muito prazer!".format(member.name, member.guild))
                    to_send.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                    to_send.set_thumbnail(url="{}".format(member.avatar_url))
                    to_send.set_footer(text="Ashley ® Todos os direitos reservados.")
                    channel_ = self.bot.get_channel(data['func_config']['member_join_id'])
                    if channel_ is None:
                        return
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
                    data = await self.bot.db.get_data("user_id", member.id, "users")
                    update = data
                    if data is not None:
                        if len(data['config']['roles']) != 0:
                            cargos = member.roles
                            for c in range(0, len(cargos)):
                                if cargos[c].name != "@everyone":
                                    await member.remove_roles(cargos[c])
                            role = discord.utils.find(lambda r: r.name == "👺Mobrau👺", member.guild.roles)
                            await member.add_roles(role)
                            channel_ = self.bot.get_channel(576795574783705104)
                            if channel_ is None:
                                return
                            return await channel_.send(f"<a:blue:525032762256785409>│{member.mention} ``SAIR SEM DAR "
                                                       f"RESPAWN NAO É A MANEIRA CORRETA DE SAIR DO SERVIDOR``")

                        if data['config']['provinces'] is not None:
                            update['config']['provinces'] = None
                            await self.bot.db.update_data(data, update, "users")

                        data = await self.bot.db.get_data("guild_id", member.guild.id, "guilds")
                        channel_ = self.bot.get_channel(data['func_config']['member_join_id'])
                        if channel_ is None:
                            return
                        t = f"<a:blue:525032762256785409>│**OBS:** {member.mention} ``PARA PEGAR SEU VIP USE O " \
                            f"COMANDO`` **ASH VIP**"
                        embed = discord.Embed(color=self.color, description=t)
                        await channel_.send(embed=embed)
            except discord.Forbidden:
                pass


def setup(bot):
    bot.add_cog(OnMemberJoin(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_JOIN\033[1;33m foi carregado com sucesso!\33[m')
