import discord

from asyncio import sleep
from discord.ext import commands
from resources.check import check_it
from resources.utility import ERRORS
from resources.db import Database


class ConfigClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.st = []
        self.color = self.bot.color

    def status(self):
        for v in self.bot.data_cog.values():
            self.st.append(v)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.group(name='config', aliases=['configuração'])
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            self.status()
            top = discord.Embed(title="Commands Status", color=self.color,
                                description=f"<:on_status:519896814799945728>│On\n"
                                f"<:alert_status:519896811192844288>│Alert\n"
                                f"<:oc_status:519896814225457152>│Off\n"
                                f"<:stream_status:519896814825242635>│Vip")
            top.add_field(name="Configs Commands:",
                          value=f"``PREFIX:`` **config** ``+``\n"
                          f"{self.st[0]}│**guild** ``or`` **server**\n"
                          f"{self.st[0]}│**report** ``or`` **reportar**\n"
                          f"{self.st[0]}│**language** ``or`` **idioma**\n"
                          f"{self.st[0]}│**log**")
            top.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            top.set_thumbnail(url=self.bot.user.avatar_url)
            top.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=top)

    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @check_it(no_pm=True, manage_guild=True)
    @config.command(name='language', aliases=['idioma'])
    async def _language(self, ctx, language=None):
        if language is not None:
            if language in self.bot.languages:
                if language != self.bot.data.get_language(ctx.guild.id):
                    self.bot.data.set_language(ctx.guild.id, language)
                    await ctx.send(f'Você acaba de mudar o idioma padrão do servidor para {language}')
                else:
                    await ctx.send(f'<:alert_status:519896811192844288>│``você ja está usando a linguagem`` '
                                   f'**{language}**')
            else:
                await ctx.send(f'<:negate:520418505993093130>│``Não existe essa linguagem disponível, escolha '
                               f'algumas dessas``: **{self.bot.languages}**')
        else:
            await ctx.send(f'<:confirmado:519896822072999937>│``Sua linguagem atual é`` '
                           f'**{self.bot.data.get_language(ctx.guild.id)}**')

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @config.command(name='log')
    async def _log(self, ctx):
        changes = {}
        configs = ['log', 'log_channel_id', 'msg_delete', 'msg_edit', 'channel_edit_topic', 'channel_edit_name',
                   'channel_created', 'channel_deleted', 'channel_edit', 'role_created', 'role_deleted',
                   'role_edit', 'guild_update', 'member_edit_avatar', 'member_edit_nickname',
                   'member_voice_entered', 'member_voice_exit', 'member_ban', 'member_unBan', 'emoji_update']
        data = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update = data
        if data is not None:
            for config in configs:
                def check_option(m):
                    return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

                def check_channel(m):
                    return m.author == ctx.author and m.channel_mentions[0].id

                if "log" in changes.keys():
                    if changes['log'] is False:
                        continue

                if config != "log_channel_id":
                    question = await ctx.send(f'<:stream_status:519896814825242635>│``Você deseja ativar o(a) '
                                              f'{config}`` **1** para ``SIM`` ou **0** para ``NÃO``')
                    answer = await self.bot.wait_for('message', check=check_option, timeout=60.0)
                    changes[config] = bool(int(answer.content))
                else:
                    question = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal de LOG``')
                    answer = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                    changes[config] = answer.content

                await question.delete()

            if "log" in changes.keys():
                if changes['log']:
                    for config in configs:
                        update['log_config'][config] = changes[config]
                else:
                    update['log_config']['log'] = False

            self.bot.db.update_data(data, update, "guilds")
            await ctx.send('<:confirmado:519896822072999937>│**PARABENS** : '
                           '``CONFIGURAÇÃO REALIZADA COM SUCESSO!``', delete_after=5.0)

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @config.command(name='guild', aliases=['server'])
    async def _guild(self, ctx):
        data = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update = data
        if data is not None:
            values = list()
            await ctx.send('<:send:519896817320591385>│``PRECISO QUE VOCÊ RESPONDA A ALGUMAS PERGUNTAS!``',
                           delete_after=5.0)

            def check_option(m):
                return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

            def check_channel(m):
                return m.author == ctx.author and m.channel_mentions[0].id

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
                    numbers = ['<:0_:578615675182907402>', '<:1_:578615669487304704>', '<:2_:578615674109165568>',
                               '<:3_:578615683424976916>', '<:4_:578615679406833685>', '<:5_:578615684708171787>',
                               '<:6_:578617070309343281>', '<:7_:578615679041798144>', '<:8_:578617071521497088>',
                               '<:9_:578617070317469708>']
                    channel_ = self.bot.get_channel(resp_6.channel_mentions[0].id)
                    text = str(ctx.guild.member_count)
                    list_ = list()
                    for l in text:
                        list_.append(numbers[int(l)])
                    await channel_.edit(topic="<a:caralho:525105064873033764> **Membros:** " + str(list_))

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

            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o meu '
                                 'AutoResponse?`` **1** para ``SIM`` ou **0** para ``NÃO``')

            resp_11 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
            values.append(resp_11.content)
            if resp_11.content == '1':
                await msg.delete()

                msg = await ctx.send('<:confirmado:519896822072999937>│``AutoResponse ativado!``')
                await sleep(2)

            await msg.delete()

            keys = ['log', 'log_channel_id', 'ash_news', 'ash_news_id', 'cont_users', 'cont_users_id',
                    'member_join', 'member_join_id', 'member_remove', 'member_remove_id', 'auto_msg']
            c = 0

            msg = await ctx.send("<a:loading:520418506567843860>│"
                                 "``AGUARDE, ESTOU PROCESSANDO SEU CADASTRO!``")

            for key in keys:
                if c % 2 == 0:
                    if c == 0:
                        update['log_config'][key] = bool(int(values[c]))
                    if c == 2:
                        update['bot_config'][key] = bool(int(values[c]))
                    if c == 4 or c == 6 or c == 8:
                        update['func_config'][key] = bool(int(values[c]))
                    if c == 10:
                        update['ia_config'][key] = bool(int(values[c]))
                    c += 1
                else:
                    if values[c] == -1:
                        if c == 1:
                            update['log_config'][key] = None
                        if c == 3:
                            update['bot_config'][key] = None
                        if c == 5 or c == 7 or c == 9:
                            update['func_config'][key] = None
                    else:
                        if c == 1:
                            update['log_config'][key] = values[c]
                        if c == 3:
                            update['bot_config'][key] = values[c]
                        if c == 5 or c == 7 or c == 9:
                            update['func_config'][key] = values[c]
                    c += 1

            self.bot.db.update_data(data, update, "guilds")
            await sleep(2)
            await msg.delete()

            await ctx.send('<:confirmado:519896822072999937>│**PARABENS** : '
                           '``CONFIGURAÇÃO REALIZADA COM SUCESSO!``', delete_after=5.0)

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @config.command(name='report', aliases=['reportar'])
    async def _report(self, ctx):
        data = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update = data
        if data is not None:
            values = list()
            await ctx.send('<:send:519896817320591385>│``PRECISO QUE VOCÊ RESPONDA A ALGUMAS PERGUNTAS!``',
                           delete_after=5.0)

            def check_option(m):
                return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

            def check_channel(m):
                return m.author == ctx.author and m.channel_mentions[0].id

            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o Report?`` '
                                 '**1** para ``SIM`` ou **0** para ``NÃO``')

            resp_1 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
            values.append(resp_1.content)
            if resp_1.content == '1':
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do Report!``')

                resp_2 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                values.append(resp_2.channel_mentions[0].id)
                await msg.delete()

                msg = await ctx.send('<:confirmado:519896822072999937>│``Report ativado!``')
                await sleep(2)
            else:
                values.append(-1)
            await msg.delete()

            keys = ['report', 'report_id']
            c = 0

            msg = await ctx.send("<a:loading:520418506567843860>│"
                                 "``AGUARDE, ESTOU PROCESSANDO SEU CADASTRO!``")

            for key in keys:
                if c % 2 == 0:
                    if c == 0:
                        update['func_config'][key] = bool(int(values[c]))
                    c += 1
                else:
                    if values[c] == -1:
                        if c == 1:
                            update['func_config'][key] = None
                    else:
                        if c == 1:
                            update['func_config'][key] = values[c]
                    c += 1

            self.bot.db.update_data(data, update, "guilds")
            await sleep(2)
            await msg.delete()

            await ctx.send('<:confirmado:519896822072999937>│**PARABENS** : '
                           '``CONFIGURAÇÃO REALIZADA COM SUCESSO!``', delete_after=5.0)

    @_guild.error
    async def _guild_error(self, ctx, error):
        if error.__str__() in ERRORS[4]:
            return await ctx.send('<:negate:520418505993093130>│``Você não marcou um canal de texto:`` '
                                  '**COMANDO CANCELADO**')
        if error.__str__() in ERRORS[5]:
            return await ctx.send("<:oc_status:519896814225457152>│``Tempo esgotado, por favor tente novamente.``")
        if error.__str__() in ERRORS[6]:
            return await ctx.send('<:negate:520418505993093130>│``Você precisa de uma permissão especifica:`` '
                                  '**manage_guild / Gerenciar Servidor**')

    @_log.error
    async def _log_error(self, ctx, error):
        if error.__str__() in ERRORS[4]:
            return await ctx.send('<:negate:520418505993093130>│``Você não marcou um canal de texto:`` '
                                  '**COMANDO CANCELADO**')
        if error.__str__() in ERRORS[5]:
            return await ctx.send("<:oc_status:519896814225457152>│``Tempo esgotado, por favor tente novamente.``")
        if error.__str__() in ERRORS[6]:
            return await ctx.send('<:negate:520418505993093130>│``Você precisa de uma permissão especifica:`` '
                                  '**manage_guild / Gerenciar Servidor**')

    @_report.error
    async def _guild_error(self, ctx, error):
        if error.__str__() in ERRORS[4]:
            return await ctx.send('<:negate:520418505993093130>│``Você não marcou um canal de texto:`` '
                                  '**COMANDO CANCELADO**')
        if error.__str__() in ERRORS[5]:
            return await ctx.send("<:oc_status:519896814225457152>│``Tempo esgotado, por favor tente novamente.``")
        if error.__str__() in ERRORS[7]:
            return await ctx.send('<:negate:520418505993093130>│``Você precisa de uma permissão especifica:`` '
                                  '**manage_guild / Gerenciar Servidor**')

    @_language.error
    async def _language_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<:negate:520418505993093130>│``Você não '
                           'tem permissão para usar esse comando!``')


def setup(bot):
    bot.add_cog(ConfigClass(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mCONFIG\033[1;32m foi carregado com sucesso!\33[m')
