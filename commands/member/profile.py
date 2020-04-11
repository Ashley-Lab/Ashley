import discord

from datetime import datetime as dt
from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import parse_duration

married, achievements, strikes = None, None, None
time_left = None


class ProfileSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @staticmethod
    def number_convert(number):
        a = '{:,.0f}'.format(float(number))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')
        return d

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='profile', aliases=['perfil'])
    async def profile(self, ctx, member: discord.Member = None):

        if member is None:
            member = ctx.author

        data = self.bot.db.get_data("user_id", member.id, "users")
        update = data

        if data is None:
            return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)

        try:
            global married
            if data['user']['married'] is False:
                married = "Solteiro(a)"
            else:
                user = self.bot.get_user(data['user']['married_at'])
                married = "Casado(a) com: " + str(user.name)
        except KeyError:
            update['user']['married'] = False
            married = "Solteiro(a)"
        try:
            if len(data['user']['achievements']) <= 0:
                global achievements
                achievements = "```Sem Conquistas```"
            else:
                answer = "".join(data['user']['achievements'])
                achievements = f"```{answer}```"
        except KeyError:
            update['user']['achievements'] = list()
            achievements = "```Sem Conquistas```"
        try:
            if data['user']['strikes'] == 0:
                global strikes
                strikes = "Ficha Limpa"
        except KeyError:
            update['user']['strikes'] = 0
            strikes = "Ficha Limpa"
        try:
            if data['user']['about']:
                pass
        except KeyError:
            update['user']['about'] = "Sou um membro cadastrado"

        try:
            global time_left
            epoch = dt.utcfromtimestamp(0)
            cooldown = data["cooldown"]["daily vip"]
            time_diff = cooldown - (dt.utcnow() - epoch).total_seconds()
            time_left = parse_duration(int(time_diff))
        except KeyError:
            time_left = None

        self.bot.db.update_data(data, update, 'users')
        data = self.bot.db.get_data("user_id", member.id, "users")

        a = '{:,.2f}'.format(float(data['treasure']['money']))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        if data['config']['vip']:
            data_ = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            if data_['vip']:
                status = "<:vip_full:546020055478042644> - **VIP Diario Ativo + VIP do Servidor Ativo**"
            else:
                status = "<:vip_member:546020055478042647> - **VIP Diario Ativo** & " \
                         "**VIP do Servidor Inativo**"
            if time_left is not None:
                status += f"\n **Tempo restante para o fim do seu VIP:** {time_left}"
        else:
            data_ = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            if data_['vip']:
                status = "<:vip_guild:546020055440425016> - **VIP do Servidor Ativo** & " \
                         "<:negate:520418505993093130> - **Seu VIP Diário Acabou**"
            else:
                status = "<:negate:520418505993093130> - **Seu VIP Diário Acabou** & " \
                         "**VIP do Servidor Inativo**"
        if data['user']['titling'] is None:
            titling = 'Vagabond'
        else:
            titling = data['user']['titling']

        try:
            rec = f"{data['user']['rec']} recomendações & {data['user']['stars']} estrelas adiquidiras"
        except KeyError:
            rec = "0 recomendações & 0 estrelas adiquidiras"

        try:
            cmds = self.number_convert(data['user']['commands'])
        except KeyError:
            cmds = 0

        embed = discord.Embed(title='Perfil do(a): {}'.format(member.display_name), color=self.color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Relationship Status:', value=str(married), inline=True)
        embed.add_field(name='Wallet:',  value="R$ " + str(d), inline=True)
        embed.add_field(name="Entitulação:", value=titling)
        embed.add_field(name="Total de Comandos:", value=cmds)
        embed.add_field(name='Bot Staff Notes :notepad_spiral:', value=str(strikes), inline=True)
        embed.add_field(name='Fichas <:coin:546019942936608778>:', value=str(self.number_convert(data['inventory']['coins'])), inline=True)
        embed.add_field(name="Ethernya Black <:etherny_preto:691016493957251152>:", value=str(self.number_convert(data['treasure']['gold'])), inline=True)
        embed.add_field(name="Ethernya Purple <:etherny_roxo:691014717761781851>:", value=str(self.number_convert(data['treasure']['silver'])), inline=True)
        embed.add_field(name="Ethernya Yellow <:etherny_amarelo:691015381296480266>:", value=str(self.number_convert(data['treasure']['bronze'])), inline=True)
        embed.add_field(name="XP:", value=str(self.number_convert(data['user']['experience'])), inline=True)
        embed.add_field(name="Level:", value=str(data['user']['level']), inline=True)
        embed.add_field(name="Ranking <:rank:519896825411665930>:", value=str(data['user']['ranking']), inline=True)
        embed.add_field(name="Recomendações:", value=rec)
        embed.add_field(name="Vip:", value=status)
        embed.add_field(name='About Me:', value=str(data['user']['about']), inline=True)
        embed.add_field(name='Achievements:', value=str(achievements), inline=True)
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='about', aliases=['sobre'])
    async def about(self, ctx, *, text: str = None):
        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if text is None:
            return await ctx.send("<:alert_status:519896811192844288>│``DIGITE ALGO PARA COLOCAR NO SEU PERFIL, "
                                  "LOGO APÓS O COMANDO!``")
        if len(text) >= 201:
            return await ctx.send("<:alert_status:519896811192844288>│``SEU TEXTO NAO PODE TER MAIS QUE 200 "
                                  "CARACTERES``")
        try:
            if data['user']['about'] and len(text) < 2000:
                update['user']['about'] = text
                self.bot.db.update_data(data, update, 'users')
                await ctx.send("<:confirmado:519896822072999937>│``TEXTO SOBRE VOCÊ ATUALIZADO COM SUCESSO!``")
            else:
                return await ctx.send("<:alert_status:519896811192844288>│``TEXTO MUITO GRANDE``")
        except KeyError:
            return await ctx.send("<:alert_status:519896811192844288>│``OLHE SEU PERFIL PRIMEIRO!``")


def setup(bot):
    bot.add_cog(ProfileSystem(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPROFILE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
