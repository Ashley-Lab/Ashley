import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import randint


with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)
money = 0


class DailyClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.st = []

    def status(self):
        for v in self.bot.data_cog.values():
            self.st.append(v)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.group(name='daily', aliases=['diario'])
    async def daily(self, ctx):
        if ctx.invoked_subcommand is None:
            self.status()
            daily = discord.Embed(title="Commands Status", color=color,
                                  description=f"<:on_status:519896814799945728>│On\n"
                                              f"<:alert_status:519896811192844288>│Alert\n"
                                              f"<:oc_status:519896814225457152>│Off\n"
                                              f"<:stream_status:519896814825242635>│Vip")
            daily.add_field(name="Daily Commands:",
                            value=f"``PREFIX:`` **daily** ``or`` **diario** ``+``\n"
                                  f"{self.st[66]}│**coin** ``or`` **ficha**\n"
                                  f"{self.st[66]}│**work** ``or`` **trabalho**\n"
                                  f"{self.st[66]}│**rec** ``or`` **recomendação**\n"
                                  f"{self.st[66]}│**vip**")
            daily.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            daily.set_thumbnail(url=self.bot.user.avatar_url)
            daily.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=daily)

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, cooldown=True, time=86400))
    @daily.group(name='coin', aliases=['ficha'])
    async def _coin(self, ctx):
        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        coin = randint(15, 35)
        update_user['inventory']['coins'] += coin
        self.bot.db.update_data(data_user, update_user, 'users')
        await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                       f'<:coin:519896843388452864> **{coin}** ``fichas!``')

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, cooldown=True, time=86400))
    @daily.group(name='work', aliases=['trabalho'])
    async def _work(self, ctx):
        if self.bot.guilds_commands[ctx.guild.id] > 50:
            if self.bot.user_commands[ctx.author.id] > 10:
                global money
                min_ = 0
                max_ = 0
                for n in range(self.bot.user_commands[ctx.author.id]):
                    min_ += 1
                    max_ += 1
                data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
                if data_user['user']['ranking'] == "Bronze":
                    money = randint(120 + min_, 1200 + max_)
                elif data_user['user']['ranking'] == "Silver":
                    money = randint(80 + min_, 800 + max_)
                elif data_user['user']['ranking'] == "Gold":
                    money = randint(40 + min_, 400 + max_)
                await self.bot.db.add_money(ctx, money)
                await ctx.send(f'<:on_status:519896814799945728>│``Você trabalhou duro e acabou de ganhar`` **{money}**'
                               f'`` em dinheiro do seu rank atual. Obs:`` **{max_}** ``de dinheiro a mais por usar '
                               f'essa mesma quantidade de comandos.``')
            else:
                try:
                    data_ = self.bot.db.get_data("user_id", ctx.author.id, "users")
                    update_ = data_
                    del data_['cooldown'][str(ctx.command)]
                    self.bot.db.update_data(data_, update_, 'users')
                except KeyError:
                    pass
                await ctx.send('<:negate:520418505993093130>│``VOCÊ AINDA NÃO USOU + DE 10 COMANDOS DA '
                               'ASHLEY DESDE A ULTIMA VEZ EM QUE ELA FICOU ONLINE!``')
        else:
            try:
                data_ = self.bot.db.get_data("user_id", ctx.author.id, "users")
                update_ = data_
                del data_['cooldown'][str(ctx.command)]
                self.bot.db.update_data(data_, update_, 'users')
            except KeyError:
                pass
            await ctx.send('<:negate:520418505993093130>│``O SERVIDOR ATUAL AINDA NÃO USOU + DE 50 COMANDOS DA '
                           'ASHLEY DESDE A ULTIMA VEZ EM QUE ELA FICOU ONLINE!``')

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, cooldown=True, time=86400))
    @daily.group(name='rec', aliases=['recomendação'])
    async def _rec(self, ctx, member: discord.Member = None):
        if member is None:
            data_ = self.bot.db.get_data("user_id", ctx.author.id, "users")
            update_ = data_
            del data_['cooldown'][str(ctx.command)]
            self.bot.db.update_data(data_, update_, 'users')
            return await ctx.send('<:oc_status:519896814225457152>│``Você precisa mensionar alguem!``')
        if member.id == ctx.author.id:
            data_ = self.bot.db.get_data("user_id", ctx.author.id, "users")
            update_ = data_
            del data_['cooldown'][str(ctx.command)]
            self.bot.db.update_data(data_, update_, 'users')
            return await ctx.send('<:oc_status:519896814225457152>│``Você não pode dar REC em si mesmo!``')
        data_user = self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        try:
            update_user['user']['rec'] += 1
        except KeyError:
            update_user['user']['rec'] = 1
        if (update_user['user']['rec'] % 20) == 0:
            chance = randint(1, 100)
            if chance >= 50:
                update_user['user']['winner'] += 1
        self.bot.db.update_data(data_user, update_user, 'users')
        await ctx.send(f'<:on_status:519896814799945728>│{member.mention} ``ACABOU DE RECEBER +1 REC DE `` '
                       f'{ctx.author.mention}')

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, cooldown=True, time=86400))
    @daily.group(name='vip')
    async def _vip(self, ctx):
        data_ = self.bot.db.get_data("user_id", ctx.author.id, "users")
        if data_['config']['vip']:
            await ctx.send('<:negate:520418505993093130>│``Você ja é vip e por isso não pode receber o prêmio de '
                           'VIP DIARIO``')
            data_ = self.bot.db.get_data("user_id", ctx.author.id, "users")
            update_ = data_
            del data_['cooldown'][str(ctx.command)]
            self.bot.db.update_data(data_, update_, 'users')
        else:
            if ctx.guild.id != _auth['default_guild']:
                await ctx.send('<:negate:520418505993093130>│``Você só pode pegar o premio de vip diario dentro do'
                               'meu servidor de suporte, para isso use o comando ASH INVITE para receber no seu'
                               'privado o link do meu servidor.``')
                data_ = self.bot.db.get_data("user_id", ctx.author.id, "users")
                update_ = data_
                del data_['cooldown'][str(ctx.command)]
                self.bot.db.update_data(data_, update_, 'users')
            else:
                data_ = self.bot.db.get_data("user_id", ctx.author.id, "users")
                update_ = data_
                update_['config']['vip'] = True
                self.bot.db.update_data(data_, update_, 'users')
                await ctx.send(f'<:on_status:519896814799945728>│{ctx.author.mention} ``ACABOU DE RECEBER 24 HORAS DE '
                               f'VIP!``\n **Aproveite seu tempo e venha buscar mais amanha!**')


def setup(bot):
    bot.add_cog(DailyClass(bot))
    print('\033[1;32mO comando \033[1;34mDAILYCLASS\033[1;32m foi carregado com sucesso!\33[m')
