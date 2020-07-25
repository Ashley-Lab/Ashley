import discord

from discord.ext import commands
from asyncio import TimeoutError
from resources.check import check_it
from resources.db import Database


class StaffAdmin(commands.Cog):
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
    @commands.group(hidden=True)
    async def staff(self, ctx):
        """Comando usado pra retornar a lista de comandos pra staff
        Use ash staff"""
        if ctx.invoked_subcommand is None:
            self.status()
            embed = discord.Embed(
                title="Commands Status",
                color=self.color,
                description=f"<:on_status:519896814799945728>│On\n"
                f"<:alert_status:519896811192844288>│Alert\n"
                f"<:oc_status:519896814225457152>│Off\n"
                f"<:stream_status:519896814825242635>│Vip")
            embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="http://mieinfo.com/wp-content/uploads/2013/08/policia-mie.png")
            embed.add_field(name="Staffs Commands:",
                            value=f"``PREFIX:`` **config** ``+``\n"
                                  f"{self.st[1]}│**delete** ``or`` **limpar**\n"
                                  f"{self.st[1]}│**ban** ``or`` **banir**\n"
                                  f"{self.st[1]}│**kick** ``or`` **expulsar**\n"
                                  f"{self.st[1]}│**slowmode** ``or`` **modolento**\n"
                                  f"{self.st[1]}│**report** ``or`` **denuncia**\n")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @check_it(no_pm=True, manage_messages=True)
    @staff.command(name='delete', aliases=["limpar", "purge", "apagar"])
    async def _delete(self, ctx, number: int):
        """Comando usado pra apagar varias mensagens em um canal
        Use ash staff delete <numero de mensagens a se apagar>"""
        if number > 100:
            return await ctx.send("<:negate:520418505993093130>│``Você nao pode apagar mais do que 100 mensagens``")
        try:
            await ctx.message.channel.purge(limit=number)
        except discord.Forbidden:
            await ctx.send("<:negate:520418505993093130>│``Não tenho permissão para apagar mensagens nesse "
                           "servidor!``")

    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @check_it(no_pm=True, ban_members=True)
    @staff.command(name='ban', aliases=['banir'])
    async def _ban(self, ctx, member=None, *, reason: str = None):
        """Comando usado pra banir usuarios
        Use ash staff ban <@usario a ser banido>"""
        try:
            user = ctx.message.mentions[0]
            if reason is None or member is None:
                return await ctx.send("<:negate:520418505993093130>│``Você precisa dizer um motivo para banir esse "
                                      "usuário!``")
            elif user.id == ctx.author.id:
                return await ctx.send("<:negate:520418505993093130>│``Você não pode banir a si mesmo!``")
            await ctx.guild.ban(user, delete_message_days=1, reason=reason)
            await ctx.send("<:confirmado:519896822072999937>│``O usuario(a)`` <@{}> ``foi banido com sucesso do "
                           "servidor.``".format(user.id))
        except IndexError:
            await ctx.send("<:alert_status:519896811192844288>│``Você deve especificar um usuario para banir!``")
        except discord.Forbidden:
            await ctx.send("<:negate:520418505993093130>│``Não posso banir o usuário, o cargo dele está acima de mim "
                           "ou não tenho permissão para banir membros!``")

    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @check_it(no_pm=True, kick_members=True)
    @staff.command(name='kick', aliases=['expulsar'])
    async def _kick(self, ctx, member=None, *, reason: str = None):
        """Comando usado pra kickar usuarios
        Use ash staff kick <@usuario a ser kickado>"""
        try:
            user = ctx.message.mentions[0]
            if reason is None or member is None:
                return await ctx.send("<:negate:520418505993093130>│``Você precisa dizer um motivo para kickar esse "
                                      "usuário!``")
            elif user.id == ctx.author.id:
                return await ctx.send("<:negate:520418505993093130>│``Você não pode banir a si mesmo!``")
            await ctx.guild.kick(user, reason=reason)
            await ctx.send("<:confirmado:519896822072999937>│``O usuario(a)`` <@{}> ``foi expulso com sucesso do "
                           "servidor.``".format(user.id))
        except IndexError:
            await ctx.send("<:alert_status:519896811192844288>│``Você deve especificar um usuario para expulsar!``")
        except discord.Forbidden:
            await ctx.send("<:negate:520418505993093130>│``Não posso expulsar o usuário, o cargo dele está acima de"
                           " mim ou não tenho permissão para banir membros!``")

    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @check_it(no_pm=True, manage_channels=True)
    @staff.command(name='slowmode', aliases=['modolento'])
    async def _slowmode(self, ctx, timer: str = None):
        """Comando usado pra ligar o slowmode em um canal
        Use ash staff slowmode"""
        try:
            if timer is None:
                if ctx.channel.slowmode_delay == 0:
                    await ctx.channel.edit(slowmode_delay=2)
                    embed = discord.Embed(
                        color=self.color,
                        description="<:confirmado:519896822072999937>│``MODO DALEY ATIVADO!``")
                    await ctx.send(embed=embed)
                else:
                    await ctx.channel.edit(slowmode_delay=0)
                    embed = discord.Embed(
                        color=self.color,
                        description="<:confirmado:519896822072999937>│``MODO DALEY DESATIVADO!``")
                    await ctx.send(embed=embed)
            elif timer.isdigit():
                if int(timer) > 120:
                    timer = 120
                await ctx.channel.edit(slowmode_delay=int(timer))
                if int(timer) == 0:
                    embed = discord.Embed(
                        color=self.color,
                        description="<:confirmado:519896822072999937>│``MODO DALEY DESATIVADO!``")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        color=self.color,
                        description="<:confirmado:519896822072999937>│``MODO DALEY ATIVADO!``")
                    await ctx.send(embed=embed)
            else:
                await ctx.send("<:negate:520418505993093130>│``POR FAVOR DIGITE UM NUMERO``")
        except discord.Forbidden:
            await ctx.send("<:negate:520418505993093130>│``NÃO TENHO PERMISSÃO PARA ALTERAR ESSE CANAL``")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @staff.command(name='report', aliases=['denuncia'])
    async def _report(self, ctx):
        """Comando usado pra reportar algo pra staff do servidor
        use ash staff report <report>"""
        try:
            data = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            if data['func_config']['report']:
                await ctx.send('<:send:519896817320591385>│``ESTAREI ENVIANDO PARA SEU PRIVADO O FORMULARIO!``',
                               delete_after=5.0)

                msg_1 = await ctx.author.send('<:stream_status:519896814825242635>│``Qual úsuario você deseja '
                                              'denunciar?`` {}'.format(ctx.author.mention))

                def check(m):
                    return m.author == ctx.author

                try:
                    member = await self.bot.wait_for('message', check=check, timeout=30.0)
                except TimeoutError:
                    return await ctx.author.send('<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')
                await msg_1.delete()
                msg_2 = await ctx.author.send('<:stream_status:519896814825242635>│``Qual o motivo da denuncia?`` '
                                              '{}'.format(ctx.author.mention))
                try:
                    report = await self.bot.wait_for('message', check=check, timeout=30.0)
                except TimeoutError:
                    return await ctx.author.send('<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')
                await msg_2.delete()
                msg_3 = await ctx.author.send('<:stream_status:519896814825242635>│``Que dia aconteceu isso?`` '
                                              '{}'.format(ctx.author.mention))
                try:
                    day = await self.bot.wait_for('message', check=check, timeout=30.0)
                except TimeoutError:
                    return await ctx.author.send('<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')
                await msg_3.delete()
                msg_4 = await ctx.author.send('<:stream_status:519896814825242635>│``Link da prova já hospedada '
                                              'senhor`` {}:'.format(ctx.author.mention))
                try:
                    file = await self.bot.wait_for('message', check=check, timeout=30.0)
                except TimeoutError:
                    return await ctx.author.send('<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')
                await msg_4.delete()
                embed = discord.Embed(colour=self.color,
                                      description="O Úsuario: {} acabou de denunciar um "
                                                  "membro!".format(ctx.author.mention))
                embed.add_field(name='✏Motivo:', value=report.content)
                embed.add_field(name='📅Data do ocorrido:', value=day.content)
                embed.add_field(name='🗒Prova:', value=file.content)
                embed.add_field(name='👤Úsuario denunciado:', value=member.content)
                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                canal = self.bot.get_channel(data['func_config']['report_id'])
                await canal.send(embed=embed)
                await ctx.author.send('<:confirmado:519896822072999937>│``FORMULARIO FINALIZADO COM SUCESSO!``',
                                      delete_after=5.0)
            else:
                await ctx.author.send("<:negate:520418505993093130>│``Recurso Desabilitado, peça para um ADM "
                                      "habilizar o recurso usando`` **ash config report**")

        except discord.errors.Forbidden:
            await ctx.send('<:negate:520418505993093130>│``INFELIZMENTE NÃO TENHO PERMISSÃO DE ENVIAR A MENSAGEM '
                           'PRA VOCÊ!``')
        except KeyError:
            await ctx.send("<:negate:520418505993093130>│``Recurso Desabilitado, peça para um ADM "
                           "habilizar o recurso usando`` **ash config report**")

    @_ban.error
    async def _ban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<:negate:520418505993093130>│``Você não '
                           'tem permissão para usar esse comando!``')

    @_kick.error
    async def _kick_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<:negate:520418505993093130>│``Você não '
                           'tem permissão para usar esse comando!``')

    @_delete.error
    async def _delete_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<:negate:520418505993093130>│``Você não '
                           'tem permissão para usar esse comando!``')

    @_slowmode.error
    async def _delete_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<:negate:520418505993093130>│``Você não '
                           'tem permissão para usar esse comando!``')


def setup(bot):
    bot.add_cog(StaffAdmin(bot))
    print('\033[1;36m( 🔶 ) | O  grupo de comandos \033[1;31mSTAFFS\033[1;36m foram carregados com sucesso!\33[m')
