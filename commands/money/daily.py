import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import parse_duration as pd
from random import randint
from datetime import datetime

m = 0
money = 0
epoch = datetime.utcfromtimestamp(0)


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
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='daily', aliases=['diario', 'd'])
    async def daily(self, ctx):
        """Comando usado pra retornar uma lista de todos os subcomandos de daily
        Use ash daily"""
        if ctx.invoked_subcommand is None:
            self.status()
            daily = discord.Embed(color=self.color)
            daily.add_field(name="Daily Commands:",
                            value=f"{self.st[66]} `daily coin` Receba suas fichas diarias.\n"
                                  f"{self.st[66]} `daily energy` Receba suas energias diarias.\n"
                                  f"{self.st[66]} `daily work` Trabalhe duro e receba seu salario.\n"
                                  f"{self.st[66]} `daily vip` Receba seu vip diario.")
            daily.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            daily.set_thumbnail(url=self.bot.user.avatar_url)
            daily.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=daily)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True, cooldown=True, time=86400))
    @daily.group(name='coin', aliases=['ficha'])
    async def _coin(self, ctx):
        """Comando usado pra ganhar coins de jogo da Ashley
        Use ash daily coin"""
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        if not data_user['security']['status']:
            return await ctx.send("<:alert:739251822920728708>│``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO "
                                  "DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**")

        coin = randint(250, 500)
        try:
            update_user['inventory']['coins'] += coin
        except KeyError:
            update_user['inventory']['coins'] = coin
        await self.bot.db.update_data(data_user, update_user, 'users')
        await ctx.send(f'<:rank:519896825411665930>│🎊 **PARABENS** 🎉 : ``Você acabou de ganhar`` '
                       f'<:coin:519896843388452864> **{coin}** ``fichas!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True, cooldown=True, time=86400))
    @daily.group(name='energy', aliases=['energia'])
    async def _energy(self, ctx):
        """Comando usado pra ganhar coins de jogo da Ashley
        Use ash daily energy"""
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        if not data_user['security']['status']:
            return await ctx.send("<:alert:739251822920728708>│``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO "
                                  "DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**")

        patent = update_user['user']['patent']
        energy = randint(25, 50)
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
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True, cooldown=True, time=86400))
    @daily.group(name='work', aliases=['trabalho', 'trabalhar'])
    async def _work(self, ctx):
        """Comando usado pra ganhar o dinheiro da Ashley diariamente
        Use ash daily work"""
        if self.bot.guilds_commands[ctx.guild.id] > 50:
            if self.bot.user_commands[ctx.author.id] > 20:
                global money, m
                data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                if not data_user['security']['status']:
                    return await ctx.send("<:alert:739251822920728708>│``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO"
                                          " DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**")

                if data_user['user']['ranking'] == "Bronze":
                    money = randint(100, 500) + self.bot.user_commands[ctx.author.id] * 2
                    m = 2
                elif data_user['user']['ranking'] == "Silver":
                    money = randint(200, 1000) + self.bot.user_commands[ctx.author.id] * 4
                    m = 4
                elif data_user['user']['ranking'] == "Gold":
                    money = randint(300, 1500) + self.bot.user_commands[ctx.author.id] * 6
                    m = 6

                msg = await self.bot.db.add_money(ctx, money)
                await ctx.send(f'<:confirmed:721581574461587496>│``Você trabalhou duro e acabou de ganhar:`` \n'
                               f'{msg}\n``Obs:`` **{self.bot.user_commands[ctx.author.id] * m}** '
                               f'``de ETHERNYAS a mais por usar {self.bot.user_commands[ctx.author.id]} comandos.``')
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
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True, cooldown=True, time=86400))
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
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='rec', aliases=['recomendação', 'rep', 'reputação'])
    async def rec(self, ctx, member: discord.Member = None):
        """Comando usado pra dar um rec da Ashley pra algum usuario
        Use ash rec <usuario desejado>"""
        if member is None:
            return await ctx.send('<:alert:739251822920728708>│``Você precisa mencionar alguem!``')

        data_user = await self.bot.db.get_data("user_id", member.id, "users")
        update_user = data_user
        data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_guild = data_guild
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        chance = randint(1, 100)
        reward = False

        if member.id == ctx.author.id:
            return await ctx.send('<:alert:739251822920728708>│``Você não pode dar REC em si mesmo!``')
        if data_user is None:
            return await ctx.send('<:alert:739251822920728708>│``Você precisa mencionar alguem cadastrado no meu '
                                  'banco de dados!``')
        if not data_user['security']['status']:
            return await ctx.send("<:alert:739251822920728708>│``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO "
                                  "DEMAIS`` **ESSE TIPO DE USUARIO NAO PODE RECEBER RECOMENDAÇÃO...**")

        try:
            time_diff = (datetime.utcnow() - epoch).total_seconds() - update['cooldown']['rec']['date']
            if time_diff < 86400:
                if update['cooldown']['rec']['cont'] > 5:
                    time_ = pd(int(86400 - time_diff))
                    return await ctx.send(f"<:alert:739251822920728708>│``Você ultrapassou suas recomendações diarias,"
                                          f" então deve esperar`` **{time_}** ``para usar esse comando novamente!``")
                if member.id in update['cooldown']['rec']['list']:
                    return await ctx.send(f"<:alert:739251822920728708>│``Você já deu REC nesse membro hoje!``")

                update['cooldown']['rec']['cont'] += 1
                update['cooldown']['rec']['date'] = (datetime.utcnow() - epoch).total_seconds()
                update['cooldown']['rec']['list'].append(member.id)

            else:
                update['cooldown']['rec'] = {"cont": 1, "date": (datetime.utcnow() - epoch).total_seconds(),
                                             "list": [member.id]}
        except KeyError:
            update['cooldown']['rec'] = {"cont": 1, "date": (datetime.utcnow() - epoch).total_seconds(),
                                         "list": [member.id]}

        # o rec é dado aqui (acima é apenas testes, e abaixo as premiações.)
        update_user['user']['rec'] += 1

        if (update_user['user']['rec'] % 2) == 0:
            if chance <= 25:
                if update_user['user']['stars'] < 20:
                    update_user['user']['stars'] += 1
                    await ctx.send(f'<:rank:519896825411665930>│{member.mention} ``GANHOU 1 ESTRELA!`` '
                                   f'🎊 **PARABENS** 🎉 **APROVEITE E OLHE SEU RANK PARA VER SUA ESTRELINHA NOVA COM '
                                   f'O COMANDO:** ``ASH RANK``')
                    if update_user['user']['stars'] >= 10:
                        if data_guild['vip'] is False and member.id == ctx.guild.owner.id:
                            update_guild['vip'] = True
                            await ctx.send('<:rank:519896825411665930>│🎊 **PARABENS** 🎉 '
                                           '**O LIDER TORNOU SUA GUILDA COMUM EM UMA GUILDA VIP!** '
                                           '``AGORA VOCÊ É CAPAZ DE CADASTRAR ANUNCIOS NO MEU SISTEMA USANDO '
                                           '"ASH ANNOUNCE" E USAR O SISTEMA DE MUSICA!``')
                    if chance < 6:
                        if update['user']['stars'] < 21:
                            update['user']['stars'] += 1
                            await ctx.send(f'<:rank:519896825411665930>│{ctx.author.mention} ``TAMBEM GANHOU 1 '
                                           f'ESTRELA!`` 🎊 **PARABENS** 🎉 **APROVEITE E OLHE SEU RANK PARA VER SUA '
                                           f'ESTRELINHA NOVA COM O COMANDO:** ``ASH RANK``')
                        else:
                            reward = True
                else:
                    if update['user']['stars'] < 21:
                        update['user']['stars'] += 1
                        await ctx.send(f'<:rank:519896825411665930>│{ctx.author.mention} ``GANHOU 1 ESTRELA, PORQUE`` '
                                       f'{member.mention} ``JA TEM TODAS AS 20 ESTRELAS DISPONIVEIS``'
                                       f'🎊 **PARABENS** 🎉 **APROVEITE E OLHE SEU RANK PARA VER SUA ESTRELINHA NOVA '
                                       f'COM O COMANDO:** ``ASH RANK``')

        await ctx.send(f'<:confirmed:721581574461587496>│{member.mention} ``ACABOU DE RECEBER +1 REC DE `` '
                       f'{ctx.author.mention}``, QUE DEU SEUS `` **{update["cooldown"]["rec"]["cont"]}**``/6 '
                       f'RECS DISPONIVEIS``')

        await self.bot.db.update_data(data, update, 'users')
        await self.bot.db.update_data(data_user, update_user, 'users')
        await self.bot.db.update_data(data_guild, update_guild, 'guilds')

        if reward:
            response = await self.bot.db.add_reward(ctx, ['?-Bollash'])
            await ctx.send(f'<a:fofo:524950742487007233>│{ctx.author.mention} ``COMO VOCE NAO PODE MAIS GANHAR '
                           f'ESTRELAS POR JA TER TODAS AS 20 ESTRELAS DISPONIVEIS VOCE GANHOU`` '
                           f'✨ **ITENS PARA PET** ✨ {response}')

        elif update_user['user']['stars'] > 19 and update['user']['stars'] > 19:
            response = await self.bot.db.add_reward(ctx, ['?-Bollash'])
            await ctx.send(f'<a:fofo:524950742487007233>│{ctx.author.mention} ``COMO NEM VOCE NEM`` '
                           f'{member.mention} ``PODEM MAIS GANHAR ESTRELAS POR JA TEREM TODAS AS 20``'
                           f' ``VOCE GANHOU`` ✨ **ITENS PARA PET** ✨ {response}')

        response = await self.bot.db.add_reward(ctx, ['Energy', 'Energy', 'Energy', 'Energy', 'Energy'])
        await ctx.send(f'<a:fofo:524950742487007233>│``VOCÊ TAMBEM GANHOU`` ✨ **ENERGIA 5x** ✨ {response}')


def setup(bot):
    bot.add_cog(DailyClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDAILYCLASS\033[1;32m foi carregado com sucesso!\33[m')
