import discord

from asyncio import sleep
from discord.ext import commands
from resources.check import check_it
from resources.utility import ERRORS


class RegisterClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.group(name='register', aliases=['registro'])
    async def register(self, ctx):
        if ctx.invoked_subcommand is None:
            user = ctx.message.author
            guild = ctx.message.guild
            data = self.bot.db.get_data("user_id", ctx.author.id, "users")
            data_guild = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            update_guild = data_guild
            if data is None and user.id in [r.id for r in guild.members if not r.bot]:
                self.bot.db.add_user(ctx)
                update_guild['data']['accounts'] += 1
                self.bot.db.update_data(data_guild, update_guild, 'guilds')
                await ctx.send('<:confirmado:519896822072999937>│``Cadastro feito com sucesso!``')
            else:
                await ctx.send('<:negate:520418505993093130>│``Você já está registrado em meu banco de dados!``')

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @register.command(name='guild')
    async def _guild(self, ctx):
        data = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        if data is None:
            values = list()
            await ctx.send('<:send:519896817320591385>│``PRECISO QUE VOCÊ RESPONDA A ALGUMAS PERGUNTAS!``',
                           delete_after=5.0)

            def check_option(m):
                return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

            def check_channel(m):
                return m.author == ctx.author and m.channel_mentions[0].id

            register = await ctx.send('<:stream_status:519896814825242635>│``VOCÊ DESEJA CONFIGURAR O SERVIDOR '
                                      'AGORA?!`` **1** para ``SIM`` ou **0** para ``NÃO``')

            resp = await self.bot.wait_for('message', check=check_option, timeout=60.0)

            if resp.content == '1':

                await register.delete()

                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o ActionLog?`` '
                                     '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_1 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
                values.append(resp_1.content)
                if resp_1.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do ActionLog!``')

                    resp_2 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                    values.append(resp_2.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmado:519896822072999937>│``ActionLog ativado!``')
                    await sleep(2)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o BotNews?`` '
                                     '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_3 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
                values.append(resp_3.content)
                if resp_3.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do BotNews!``')

                    resp_4 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                    values.append(resp_4.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmado:519896822072999937>│``BotNews ativado!``')
                    await sleep(2)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o MemberCont?`` '
                                     '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_5 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
                values.append(resp_5.content)
                if resp_5.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do MemberCont!``')

                    resp_6 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                    values.append(resp_6.channel_mentions[0].id)
                    await msg.delete()

                    try:
                        numbers = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
                        channel_ = self.bot.get_channel(resp_6.channel_mentions[0].id)
                        text = str(ctx.guild.member_count)
                        for n in range(0, 10):
                            text = text.replace(str(n), numbers[n])
                        await channel_.edit(topic="Membros: " + text)

                        msg = await ctx.send('<:confirmado:519896822072999937>│``Contador de membros ativado!``')
                        await sleep(2)

                    except discord.Forbidden:
                        await ctx.send("<:negate:520418505993093130>│``Não tenho permissão para editar canais "
                                       "nesse servidor!``", delete_after=5.0)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o MemberJoin?`` '
                                     '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_7 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
                values.append(resp_7.content)
                if resp_7.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do MemberJoin!``')

                    resp_8 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                    values.append(resp_8.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmado:519896822072999937>│``MemberJoin ativado!``')
                    await sleep(2)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o '
                                     'MemberRemove?`` **1** para ``SIM`` ou **0** para ``NÃO``')

                resp_9 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
                values.append(resp_9.content)
                if resp_9.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do '
                                         'MemberRemove!``')

                    resp_10 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                    values.append(resp_10.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmado:519896822072999937>│``MemberRemove ativado!``')
                    await sleep(2)
                else:
                    values.append(-1)
                await msg.delete()

                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o '
                                     'AutoResponse da Ashley?`` **1** para ``SIM`` ou **0** para ``NÃO``')

                resp_11 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
                values.append(resp_11.content)
                if resp_11.content == '1':
                    await msg.delete()

                    msg = await ctx.send('<:confirmado:519896822072999937>│``AutoResponse ativado!``')
                    await sleep(2)

                await msg.delete()

            else:
                await register.delete()

            keys = ['log', 'log_channel_id', 'ash_news', 'ash_news_id', 'cont_users', 'cont_users_id',
                    'member_join', 'member_join_id', 'member_remove', 'member_remove_id', 'auto_msg']
            data = {}
            c = 0

            msg = await ctx.send("<a:loading:520418506567843860>│``AGUARDE, ESTOU PROCESSANDO SEU CADASTRO!``")

            if resp.content == '1':
                for key in keys:
                    if c % 2 == 0:
                        data[key] = bool(int(values[c]))
                        c += 1
                    else:
                        if values[c] == -1:
                            data[key] = None
                        else:
                            data[key] = values[c]
                        c += 1

            self.bot.db.add_guild(ctx.guild, data)
            await sleep(2)
            await msg.delete()

            await ctx.send('<:confirmado:519896822072999937>│**PARABENS** : '
                           '``CADASTRO FINALIZADO COM SUCESSO!``', delete_after=5.0)

        else:
            await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                           '``essa guilda já está cadastrada!``')

    @_guild.error
    async def _guild_error(self, ctx, error):
        if error.__str__() in ERRORS[5]:
            return await ctx.send("<:oc_status:519896814225457152>│``Tempo esgotado, por favor tente novamente.``")
        if error.__str__() in ERRORS[4]:
            return await ctx.send('<:negate:520418505993093130>│``Você não marcou um canal de texto:`` '
                                  '**COMANDO CANCELADO**')


def setup(bot):
    bot.add_cog(RegisterClass(bot))
    print('\033[1;32mO comando \033[1;34mREGISTERCLASS\033[1;32m foi carregado com sucesso!\33[m')
