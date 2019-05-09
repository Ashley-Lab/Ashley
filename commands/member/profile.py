import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)
married, achievements, strikes = None, None, None


class ProfileSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            if data['user']['achievements'] is None:
                global achievements
                achievements = "```Sem Conquistas```"
            else:
                answer = "".join(data['user']['achievements'])
                achievements = f"```{answer}```"
        except KeyError:
            update['user']['achievements'] = None
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
            rec = f"{data['user']['rec']} recomendações & {data['user']['winner']} estrelas adiquidiras"
        except KeyError:
            rec = "0 recomendações & 0 estrelas adiquidiras"

        try:
            cmds = data['user']['commands']
        except KeyError:
            cmds = 0

        embed = discord.Embed(title='Perfil do(a): {}'.format(member.display_name), color=color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Relationship Status :heart_eyes: ', value=str(married), inline=True)
        embed.add_field(name='Wallet :moneybag:',  value="R$ " + str(d), inline=True)
        embed.add_field(name="Vip: ", value=status)
        embed.add_field(name="Entitulação: ", value=titling)
        embed.add_field(name="Recomendações: ", value=rec)
        embed.add_field(name="Total de Comandos: ", value=cmds)
        embed.add_field(name='Bot Staff Notes :notepad_spiral:', value=str(strikes), inline=True)
        embed.add_field(name='Fichas <:dinars:519896828930686977>', value=str(data['inventory']['coins']), inline=True)
        embed.add_field(name="Gold <:gold:540586811462778880>", value=str(data['treasure']['gold']), inline=True)
        embed.add_field(name="Silver <:silver:540586812154970133>", value=str(data['treasure']['silver']), inline=True)
        embed.add_field(name="Bronze <:bronze:540586812054437910>", value=str(data['treasure']['bronze']), inline=True)
        embed.add_field(name="XP <:check:519896827374338048>", value=str(data['user']['experience']), inline=True)
        embed.add_field(name="Level <:check:519896827374338048>", value=str(data['user']['level']), inline=True)
        embed.add_field(name="Ranking <:rank:519896825411665930>", value=str(data['user']['ranking']), inline=True)
        embed.add_field(name='About Me :pen_ballpoint:', value=str(data['user']['about']), inline=True)
        embed.add_field(name='Achievements :ribbon:', value=str(achievements), inline=True)
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
    print('\033[1;32mO comando \033[1;34mPROFILE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
