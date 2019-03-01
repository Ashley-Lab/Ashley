import json
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class FeedBackClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='feedback', aliases=['sugestao'])
    async def feedback(self, ctx, *, msg: str = None):
        if msg is None:
            return await ctx.send('<:negate:520418505993093130>│``ESCOLHA ENTRE`` **REPORT** ``OU`` **SUGGESTION**')
        try:
            if msg.upper() == "REPORT":
                await ctx.send('<:send:519896817320591385>│``ESTAREI ENVIANDO PARA SEU PRIVADO O FORMULARIO!``',
                               delete_after=5.0)

                msg_1 = await ctx.author.send(
                    '<:stream_status:519896814825242635>│``Qual comando você deseja reportar?`` '
                    '{}'.format(ctx.author.mention))

                def check(m):
                    return m.author == ctx.author

                try:
                    member = await self.bot.wait_for('message', check=check, timeout=60.0)
                except TimeoutError:
                    return await ctx.author.send(
                        '<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')
                await msg_1.delete()
                msg_2 = await ctx.author.send('<:stream_status:519896814825242635>│``Qual o motivo do report?`` '
                                              '{}'.format(ctx.author.mention))
                try:
                    report = await self.bot.wait_for('message', check=check, timeout=60.0)
                except TimeoutError:
                    return await ctx.author.send(
                        '<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')
                await msg_2.delete()
                msg_3 = await ctx.author.send('<:stream_status:519896814825242635>│``Que dia aconteceu isso?`` '
                                              '{}'.format(ctx.author.mention))
                try:
                    day = await self.bot.wait_for('message', check=check, timeout=60.0)
                except TimeoutError:
                    return await ctx.author.send(
                        '<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')
                await msg_3.delete()
                msg_4 = await ctx.author.send(
                    '<:stream_status:519896814825242635>│``Link da prova já hospedada senhor`` '
                    '{}:'.format(ctx.author.mention))
                try:
                    file = await self.bot.wait_for('message', check=check, timeout=60.0)
                except TimeoutError:
                    return await ctx.author.send(
                        '<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')
                await msg_4.delete()
                embed = discord.Embed(colour=color,
                                      description="O Úsuario: {} acabou de reportar o comando {}!".format(
                                          ctx.author.mention, member.content))
                embed.add_field(name='✏Motivo:', value=report.content)
                embed.add_field(name='📅Data do ocorrido:', value=day.content)
                embed.add_field(name='🗒Prova:', value=file.content)
                embed.add_field(name='👤Comando reportado:', value=member.content)
                embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                canal = self.bot.get_channel(525361582281064468)
                await canal.send(embed=embed)

                await ctx.author.send('<:confirmado:519896822072999937>│``FORMULARIO FINALIZADO COM SUCESSO!``',
                                      delete_after=5.0)
            elif msg.upper() == "SUGGESTION":
                await ctx.send('<:stream_status:519896814825242635>│``Qual a sua sugestão?`` '
                               '{}'.format(ctx.author.mention))

                def check(m):
                    return m.author == ctx.author

                try:
                    sugsestion = await self.bot.wait_for('message', check=check, timeout=60.0)
                except TimeoutError:
                    return await ctx.author.send(
                        '<:oc_status:519896814225457152>│``Desculpe, você demorou muito!``')

                member = ctx.author
                server = ctx.guild
                channel = self.bot.get_channel(530418605284917252)
                embed = discord.Embed(title='Suggestion', color=color)
                embed.add_field(name='Info',
                                value=f'● Server: {server.name}\n● ServerID: {server.id}\n● Usuario: {member.name}\n● '
                                f'UsuarioID: {member.id}')
                embed.add_field(name='Feedback', value=f'{sugsestion.content}', inline=False)
                embed.set_thumbnail(url="{}".format(member.avatar_url))
                embed.set_footer(text="Ashley ® Todos os direitos reservados.")
                await channel.send(embed=embed)
                await ctx.send('<:confirmado:519896822072999937>│``Feedback enviado com sucesso!``')
            else:
                await ctx.send("<:oc_status:519896814225457152>│``OPÇÃO INVALIDA! "
                               "ESCOLHA ENTRE`` **REPORT** ``OU`` **SUGGESTION**")
        except discord.errors.HTTPException:
            await ctx.send("<:oc_status:519896814225457152>│``SEU FEEDBACK FOI GRANDE DEMAIS, TENTE MANDAR "
                           "EM PARTES!``")


def setup(bot):
    bot.add_cog(FeedBackClass(bot))
    print('\033[1;32mO comando \033[1;34mFEEDBACK\033[1;32m foi carregado com sucesso!\33[m')
