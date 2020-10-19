import discord

from datetime import datetime as dt
from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import parse_duration
from resources.img_edit import profile, remove_acentos_e_caracteres_especiais

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
        """Comando usado pra ver o seu perfil da ashley
        Use ash profile <@usuario em questão se não colocar vera seu proprio perfil>"""
        if member is None:
            member = ctx.author

        global time_left

        data = await self.bot.db.get_data("user_id", member.id, "users")
        if data is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)

        data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")

        try:
            epoch = dt.utcfromtimestamp(0)
            cooldown = data["cooldown"]["daily vip"]
            time_diff = cooldown - (dt.utcnow() - epoch).total_seconds()
            time_left = parse_duration(int(time_diff))
        except KeyError:
            time_left = None

        a = '{:,.2f}'.format(float(data['treasure']['money']))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        vip = [[], f"{time_left}"]

        if data['config']['vip']:
            vip[0].append(True)
        else:
            vip[0].append(False)

        if data_guild['vip']:
            vip[0].append(True)
        else:
            vip[0].append(False)

        if data['rpg']['vip']:
            vip[0].append(True)
        else:
            vip[0].append(False)

        if data['user']['married']:
            try:
                user = self.bot.get_user(data['user']['married_at'])
                married = user.avatar_url_as(format="png")
            except AttributeError:
                married = "https://w-dog.net/wallpapers/2/13/487318654230690/abandoned-church-the-altar-interior.jpg"
                """await ctx.send("<:alert:739251822920728708>│``VOCE TA CASADO COM ALGUEM QUE NAO EXISTE MAIS, "
                               "FAÇA UM FAVOR PRA VC MESMO E PEÇA O DIVORCIO!``")"""
        else:
            married = None

        try:
            coins = data['inventory']['coins']
        except KeyError:
            coins = 0

        data_profile = {
            "avatar_member": member.avatar_url_as(format="png"),
            "avatar_married": married,
            "name": remove_acentos_e_caracteres_especiais(member.display_name),
            "xp": data['user']['experience'],
            "level": str(data['user']['level']),
            "vip": vip,
            "rec": str(data['user']['rec']),
            "coin": str(self.number_convert(coins)),
            "commands": str(self.number_convert(data['user']['commands'])),
            "entitlement": str(data['user']['titling']),
            "about": remove_acentos_e_caracteres_especiais(data['user']['about']),
            "wallet": str(d),
            "pet": data['pet']['pet_equipped'],
            "artifacts": data['artifacts']
        }

        await profile(data_profile)
        await ctx.send("> ``CLIQUE NA IMAGEM PARA MAIORES DETALHES``")

        if discord.File('profile.png') is None:
            return await ctx.send("<:negate:721581573396496464>│``ERRO!``")
        await ctx.send(file=discord.File('profile.png'))

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='about', aliases=['sobre'])
    async def about(self, ctx, *, text: str = None):
        """Comando usado para alterar o 'about me' do ash perfil"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if text is None:
            return await ctx.send("<:alert:739251822920728708>│``DIGITE ALGO PARA COLOCAR NO SEU PERFIL, "
                                  "LOGO APÓS O COMANDO!``")

        text = remove_acentos_e_caracteres_especiais(text)
        if text == "":
            text = "PRECISO DIGITAR ALGO DESCENTE..."
        await ctx.send(f"<:alert:739251822920728708>│``SEU TEXTO VAI FICAR ASSIM:``\n{text}")

        if len(text) > 200:
            return await ctx.send("<:alert:739251822920728708>│``SEU TEXTO NAO PODE TER MAIS QUE 200 "
                                  "CARACTERES``")

        if data['user']['about'] and len(text) <= 200:
            update['user']['about'] = text
            await self.bot.db.update_data(data, update, 'users')
            await ctx.send("<:confirmed:721581574461587496>│``TEXTO SOBRE VOCÊ ATUALIZADO COM SUCESSO!``")
        else:
            return await ctx.send("<:alert:739251822920728708>│``TEXTO MUITO GRANDE``")


def setup(bot):
    bot.add_cog(ProfileSystem(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mPROFILE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
