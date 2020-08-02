import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import randint
from datetime import datetime

money = 0


class DailyClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.st = []
        self.color = self.bot.color

    def status(self):
        for v in self.bot.data_cog.values():
            self.st.append(v)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.group(name='daily', aliases=['diario', 'd'])
    async def daily(self, ctx):
        """Comando usado pra retornar uma lista de todos os subcomandos de daily
        Use ash daily"""
        if ctx.invoked_subcommand is None:
            self.status()
            daily = discord.Embed(title="Commands Status", color=self.color,
                                  description=f"<:on_status:519896814799945728>│On\n"
                                              f"<:alert_status:519896811192844288>│Alert\n"
                                              f"<:oc_status:519896814225457152>│Off\n"
                                              f"<:stream_status:519896814825242635>│Vip")
            daily.add_field(name="Daily Commands:",
                            value=f"``PREFIX:`` **daily** ``or`` **diario** ``+``\n"
                                  f"{self.st[66]}│**coin** ``or`` **ficha**\n"
                                  f"{self.st[66]}│**energy** ``or`` **energia**\n"
                                  f"{self.st[66]}│**work** ``or`` **trabalho**\n"
                                  f"{self.st[66]}│**vip**")
            daily.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            daily.set_thumbnail(url=self.bot.user.avatar_url)
            daily.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=daily)

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, cooldown=True, time=86400))
    @daily.group(name='coin', aliases=['ficha'])
    async def _coin(self, ctx):
        """Comando usado pra ganhar coins de jogo da Ashley
        Use ash daily coin"""
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        if not data_user['security']['status']:
            return await ctx.send("<:alert:739251822920728708>│'``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO "
                                  "DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**'")

        coin = randint(50, 100)
        update_user['inventory']['coins'] += coin
        await self.bot.db.update_data(data_user, update_user, 'users')
        await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                       f'<:coin:519896843388452864> **{coin}** ``fichas!``')

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, cooldown=True, time=86400))
    @daily.group(name='energy', aliases=['energia'])
    async def _energy(self, ctx):
        """Comando usado pra ganhar coins de jogo da Ashley
        Use ash daily energy"""
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        if not data_user['security']['status']:
            return await ctx.send("<:alert:739251822920728708>│'``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO "
                                  "DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**'")

        patent = update_user['user']['patent']
        energy = randint(5, 15)
        energy += patent * 2
        try:
            update_user['inventory']['Energy'] += energy
        except KeyError:
            update_user['inventory']['Energy'] = energy
        await self.bot.db.update_data(data_user, update_user, 'users')
        await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                       f'<:energy:546019943603503114> **{energy}** ``Energias!`` + **{patent * 2}** '
                       f'``pela sua patente. Olhe seu inventario usando o comando:`` **ash i**')

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, cooldown=True, time=86400))
    @daily.group(name='work', aliases=['trabalho'])
    async def _work(self, ctx):
        """Comando usado pra ganhar o dinheiro da Ashley diariamente
        Use ash daily work"""
        if self.bot.guilds_commands[ctx.guild.id] > 50:
            if self.bot.user_commands[ctx.author.id] > 20:
                global money
                min_ = 0
                max_ = 0
                for n in range(self.bot.user_commands[ctx.author.id]):
                    min_ += 1
                    max_ += randint(1, 3)
                data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")

                if not data_user['security']['status']:
                    return await ctx.send(
                        "<:alert:739251822920728708>│'``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO "
                        "DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**'")

                if data_user['user']['ranking'] == "Bronze":
                    money = randint(120 + min_, 1200 + max_)
                elif data_user['user']['ranking'] == "Silver":
                    money = randint(200 + min_, 2000 + max_)
                elif data_user['user']['ranking'] == "Gold":
                    money = randint(240 + min_, 2400 + max_)
                msg = await self.bot.db.add_money(ctx, money)
                await ctx.send(f'<:confirmed:721581574461587496>│``Você trabalhou duro e acabou de ganhar:`` \n'
                               f'{msg}\n'
                               f'``Obs:`` **{max_ + min_}** ``de ETHERNYAS a mais por usar {min_} comandos.``')
            else:
                try:
                    data_ = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                    update_ = data_
                    del data_['cooldown'][str(ctx.command)]
                    await self.bot.db.update_data(data_, update_, 'users')
                except KeyError:
                    pass
                await ctx.send('<:alert:739251822920728708>│``VOCÊ AINDA NÃO USOU + DE 20 COMANDOS DA '
                               'ASHLEY DESDE A ULTIMA VEZ EM QUE ELA FICOU ONLINE!``')
        else:
            try:
                data_ = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update_ = data_
                del data_['cooldown'][str(ctx.command)]
                await self.bot.db.update_data(data_, update_, 'users')
            except KeyError:
                pass
            await ctx.send('<:alert:739251822920728708>│``O SERVIDOR ATUAL AINDA NÃO USOU + DE 50 COMANDOS DA '
                           'ASHLEY DESDE A ULTIMA VEZ EM QUE ELA FICOU ONLINE!``')

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, cooldown=True, time=86400))
    @daily.group(name='vip')
    async def _vip(self, ctx):
        """Comando usado pra ganhar vip da Ashley diariamente(usavel somente no server da Ashley)
        Use ash daily vip"""
        if ctx.guild.id != self.bot.config['config']['default_guild']:
            try:
                data_ = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update_ = data_
                del data_['cooldown'][str(ctx.command)]
                await self.bot.db.update_data(data_, update_, 'users')
            except KeyError:
                pass

            return await ctx.send('<:alert:739251822920728708>│``Você só pode pegar o premio de vip diario dentro '
                                  'do meu servidor de suporte, para isso use o comando ASH INVITE para receber no '
                                  'seu privado o link do meu servidor.``')

        data_ = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_ = data_
        update_['config']['vip'] = True
        await self.bot.db.update_data(data_, update_, 'users')
        await ctx.send(f'<:confirmed:721581574461587496>│{ctx.author.mention} ``ACABOU DE RECEBER 24 HORAS DE '
                       f'VIP!``\n **Aproveite seu tempo e venha buscar mais amanha!**')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='rec', aliases=['recomendação'])
    async def rec(self, ctx, member: discord.Member = None):
        """Comando usado pra dar um rec da Ashley pra algum usuario
        Use ash rec <usuario desejado>"""
        if member is None:
            return await ctx.send('<:alert:739251822920728708>│``Você precisa mencionar alguem!``')

        data_user = await self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user

        if not data_user['security']['status']:
            return await ctx.send("<:alert:739251822920728708>│'``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO "
                                  "DEMAIS`` **ESSE TIPO DE USUARIO NAO PODE RECEBER RECOMENDAÇÃO...**'")

        if member.id == ctx.author.id:
            return await ctx.send('<:alert:739251822920728708>│``Você não pode dar REC em si mesmo!``')
        if data_user is None:
            return await ctx.send('<:alert:739251822920728708>│``Você precisa mencionar alguem cadastrado no meu '
                                  'banco de dados!``')

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        try:
            date_now = datetime.today()
            date_old = update['cooldown']['rec']['date']

            if update['cooldown']['rec']['cont'] < 6 and abs((date_old - date_now).days) < 2:
                if member.id in update['cooldown']['rec']['list']:
                    return await ctx.send(f"<:alert:739251822920728708>│``Você já deu REC nesse membro hoje!``")
                update['cooldown']['rec']['cont'] += 1
                update['cooldown']['rec']['list'].append(member.id)
                await self.bot.db.update_data(data, update, 'users')
            else:
                if abs((date_old - date_now).days) > 1:
                    update['cooldown']['rec'] = {"cont": 1, "date": datetime.today(), "list": [member.id]}
                    await self.bot.db.update_data(data, update, 'users')
                else:
                    return await ctx.send(f"<:alert:739251822920728708>│``Você ultrapassou suas "
                                          f"recomendações por hoje!``")
        except KeyError:
            update['cooldown']['rec'] = {"cont": 1, "date": datetime.today(), "list": [member.id]}
            await self.bot.db.update_data(data, update, 'users')

        update_user['user']['rec'] += 1

        if (update_user['user']['rec'] % 2) == 0:
            chance = randint(1, 100)
            if chance <= 25:
                update_user['user']['stars'] += 1
                await ctx.send(f'<:rank:519896825411665930>│{member.mention} ``GANHOU 1 ESTRELA!`` 🎊 **PARABENS** 🎉 '
                               f'**APROVEITE E OLHE SEU RANK PARA VER SUA ESTRELINHA NOVA COM O COMANDO:** '
                               f'``ASH RANK``')
                if update_user['user']['stars'] >= 10:
                    data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
                    update_guild = data_guild
                    if data_guild['vip'] is False and member.id == ctx.guild.owner.id:
                        update_guild['vip'] = True
                        await self.bot.db.update_data(data_guild, update_guild, 'guilds')
                        await ctx.send('<:rank:519896825411665930>│🎊 **PARABENS** 🎉 '
                                       '**O LIDER TORNOU SUA GUILDA COMUM EM UMA GUILDA VIP!** '
                                       '``AGORA VOCÊ É CAPAZ DE CADASTRAR ANUNCIOS NO MEU SISTEMA USANDO '
                                       '"ASH ANNOUNCE" E USAR O SISTEMA DE MUSICA!``')

        await self.bot.db.update_data(data_user, update_user, 'users')
        await ctx.send(f'<:confirmed:721581574461587496>│{member.mention} ``ACABOU DE RECEBER +1 REC DE `` '
                       f'{ctx.author.mention}')


def setup(bot):
    bot.add_cog(DailyClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDAILYCLASS\033[1;32m foi carregado com sucesso!\33[m')
