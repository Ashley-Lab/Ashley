import discord

from resources.img_edit import welcome
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

                    canal = self.bot.get_channel(data['func_config']['member_join_id'])
                    if canal is None:
                        return

                    data_welcome = {
                        "type": "welcome",
                        "name": str(member.name),
                        "avatar": member.avatar_url_as(format="png"),
                        "text": f"Seja bem vindo ao servidor {member.guild.name.upper()}, divirta-se!"
                    }

                    await welcome(data_welcome)

                    file = discord.File('welcome.png')
                    if file is not None:
                        ashley = canal.guild.get_member(self.bot.user.id)
                        perms = canal.permissions_for(ashley)
                        if perms.send_messages or perms.read_messages:
                            if not perms.embed_links or not perms.attach_files:
                                await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                 "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                 " CORRETAMENTE!**")
                            else:
                                await canal.send(file=file)
                    else:
                        embed = discord.Embed(
                            title=f"{member.name.upper()} Entrou!", color=self.bot.color,
                            description=f"Seja bem vindo ao servidor {member.guild.name.upper()}, divirta-se!")
                        userjoinedat = str(member.joined_at).split('.', 1)[0]
                        usercreatedat = str(member.created_at).split('.', 1)[0]
                        embed.add_field(name="Entrou no server em:", value=userjoinedat, inline=True)
                        embed.add_field(name="Conta criada em:", value=usercreatedat, inline=True)
                        embed.add_field(name="ID:", value=str(member.id), inline=True)
                        embed.set_thumbnail(url=member.avatar_url)
                        ashley = canal.guild.get_member(self.bot.user.id)
                        perms = canal.permissions_for(ashley)
                        if perms.send_messages or perms.read_messages:
                            if not perms.embed_links or not perms.attach_files:
                                await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                 "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                 " CORRETAMENTE!**")
                            else:
                                await canal.send(embed=embed)

                except discord.errors.Forbidden:
                    pass
                except AttributeError:
                    pass
                except discord.errors.NotFound:
                    pass

            if data['func_config']['cont_users']:
                try:
                    numbers = ['<:0_:578615675182907402>', '<:1_:578615669487304704>', '<:2_:578615674109165568>',
                               '<:3_:578615683424976916>', '<:4_:578615679406833685>', '<:5_:578615684708171787>',
                               '<:6_:578617070309343281>', '<:7_:578615679041798144>', '<:8_:578617071521497088>',
                               '<:9_:578617070317469708>']
                    canal = self.bot.get_channel(data['func_config']['cont_users_id'])
                    if canal is None:
                        return
                    text = str(member.guild.member_count)
                    list_ = list()
                    for letter in text:
                        list_.append(numbers[int(letter)])
                    list_ = str(list_).replace('[', '').replace(']', '').replace(',', '.')
                    ashley = canal.guild.get_member(self.bot.user.id)
                    perms = canal.permissions_for(ashley)
                    if perms.send_messages and perms.read_messages:
                        if not perms.embed_links or not perms.attach_files:
                            await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                             "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                             " CORRETAMENTE!**")
                        else:
                            await canal.edit(topic="<a:caralho:525105064873033764> **Membros:**  " + list_)
                except discord.errors.Forbidden:
                    pass
                except discord.errors.NotFound:
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
                            canal = self.bot.get_channel(576795574783705104)
                            if canal is None:
                                return
                            ashley = canal.guild.get_member(self.bot.user.id)
                            perms = canal.permissions_for(ashley)
                            if perms.send_messages or perms.read_messages:
                                if not perms.embed_links or not perms.attach_files:
                                    await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                     "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                     " CORRETAMENTE!**")
                                else:
                                    return await canal.send(f"<a:blue:525032762256785409>│{member.mention} ``SAIR SEM"
                                                            f" DAR RESPAWN NAO É A MANEIRA CORRETA DE SAIR DO "
                                                            f"SERVIDOR``")

                        if data['config']['provinces'] is not None:
                            update['config']['provinces'] = None
                            await self.bot.db.update_data(data, update, "users")

                        data = await self.bot.db.get_data("guild_id", member.guild.id, "guilds")
                        canal = self.bot.get_channel(data['func_config']['member_join_id'])
                        if canal is None:
                            return
                        t = f"<a:blue:525032762256785409>│**OBS:** {member.mention} ``PARA PEGAR SEU VIP USE O " \
                            f"COMANDO`` **ASH VIP**"
                        embed = discord.Embed(color=self.color, description=t)
                        ashley = canal.guild.get_member(self.bot.user.id)
                        perms = canal.permissions_for(ashley)
                        if perms.send_messages or perms.read_messages:
                            if not perms.embed_links or not perms.attach_files:
                                await canal.send("<:negate:721581573396496464>│``PRECISO DA PERMISSÃO DE:`` "
                                                 "**ADICIONAR LINKS E DE ADICIONAR IMAGENS, PARA PODER FUNCIONAR"
                                                 " CORRETAMENTE!**")
                            else:
                                await canal.send(embed=embed)
            except discord.Forbidden:
                pass
            except discord.errors.NotFound:
                pass


def setup(bot):
    bot.add_cog(OnMemberJoin(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mMEMBER_JOIN\033[1;33m foi carregado com sucesso!\33[m')
