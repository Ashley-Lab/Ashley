import discord

from datetime import datetime as dt
from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import parse_duration
from resources.img_edit import profile, remove_acentos_e_caracteres_especiais

user = None
time_left = None
rec = 0


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
        """Comando usado pra ver o seu perfil da ashley
        Use ash profile <@usuario em questão se não colocar vera seu proprio perfil>"""
        if member is None:
            member = ctx.author

        global time_left, user, rec

        data = await self.bot.db.get_data("user_id", member.id, "users")
        update = data

        if data is None:
            return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)

        try:
            epoch = dt.utcfromtimestamp(0)
            cooldown = data["cooldown"]["daily vip"]
            time_diff = cooldown - (dt.utcnow() - epoch).total_seconds()
            time_left = parse_duration(int(time_diff))
        except KeyError:
            time_left = None

        await self.bot.db.update_data(data, update, 'users')
        n_data = await self.bot.db.get_data("user_id", member.id, "users")

        a = '{:,.2f}'.format(float(n_data['treasure']['money']))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        vip = [[], f"{time_left}"]
        if n_data['config']['vip']:
            vip[0].append(True)
        else:
            vip[0].append(False)
        data_ = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        if data_['vip']:
            vip[0].append(True)
        else:
            vip[0].append(False)
        vip[0].append(False)

        if n_data['user']['married']:
            user = self.bot.get_user(data['user']['married_at'])
            married = user.avatar_url_as(format="png")
        else:
            married = None

        data_profile = {
            "avatar_member": member.avatar_url_as(format="png"),
            "avatar_married": married,
            "name": remove_acentos_e_caracteres_especiais(member.display_name),
            "xp": n_data['user']['experience'],
            "level": str(n_data['user']['level']),
            "vip": vip,
            "rec": str(n_data['user']['rec']),
            "coin": str(self.number_convert(n_data['inventory']['coins'])),
            "commands": str(self.number_convert(n_data['user']['commands'])),
            "entitlement": str(n_data['user']['titling']),
            "about": remove_acentos_e_caracteres_especiais(n_data['user']['about']),
            "wallet": str(d),
            "pet": n_data['pet']['pet_equipped'],
            "artifacts": n_data['artifacts']
        }

        profile(data_profile)
        await ctx.send("> ``CLIQUE NA IMAGEM PARA MAIORES DETALHES``")
        try:
            await ctx.send(file=discord.File('profile.png'))
        except discord.HTTPException:
            pass

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='about', aliases=['sobre'])
    async def about(self, ctx, *, text: str = None):
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if text is None:
            return await ctx.send("<:alert_status:519896811192844288>│``DIGITE ALGO PARA COLOCAR NO SEU PERFIL, "
                                  "LOGO APÓS O COMANDO!``")

        text = remove_acentos_e_caracteres_especiais(text)
        if text == "":
            text = "PRECISO DIGITAR ALGO DESCENTE..."
        await ctx.send(f"<:alert_status:519896811192844288>│``SEU TEXTO VAI FICAR ASSIM:``\n{text}")

        if len(text) > 200:
            return await ctx.send("<:alert_status:519896811192844288>│``SEU TEXTO NAO PODE TER MAIS QUE 200 "
                                  "CARACTERES``")

        if data['user']['about'] and len(text) <= 200:
            update['user']['about'] = text
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send("<:confirmado:519896822072999937>│``TEXTO SOBRE VOCÊ ATUALIZADO COM SUCESSO!``")
        else:
            return await ctx.send("<:alert_status:519896811192844288>│``TEXTO MUITO GRANDE``")


def setup(bot):
    bot.add_cog(ProfileSystem(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPROFILE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
