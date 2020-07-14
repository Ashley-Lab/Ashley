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
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.group(name='config', aliases=['configuração'])
    async def config(self, ctx):
        """Comando usado pra configurar alguns settings da ashley
        Use ash config pra ver as configurações disponiveis"""
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
                                f"{self.st[0]}│**log**")
            top.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            top.set_thumbnail(url=self.bot.user.avatar_url)
            top.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=top)

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @config.command(name='log')
    async def _log(self, ctx):
        """Comando usado pra configurar os logs da ashley
        Use ash config log e siga as instruções do comando"""
        changes = {}
        configs = ['log', 'log_channel_id', 'msg_delete', 'msg_edit', 'channel_edit_topic', 'channel_edit_name',
                   'channel_created', 'channel_deleted', 'channel_edit', 'role_created', 'role_deleted',
                   'role_edit', 'guild_update', 'member_edit_avatar', 'member_edit_nickname',
                   'member_voice_entered', 'member_voice_exit', 'member_ban', 'member_unBan', 'emoji_update']
        data = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
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

            await self.bot.db.update_data(data, update, "guilds")
            await ctx.send('<:confirmado:519896822072999937>│**PARABENS** : '
                           '``CONFIGURAÇÃO REALIZADA COM SUCESSO!``', delete_after=5.0)

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @config.command(name='guild', aliases=['server'])
    async def _guild(self, ctx):
        """Comando usado pra configurar sua guilda/server na Ashley
        Use ash config guild e siga as instruções do comando(use # pra marcar canais)"""
        data = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update = data
        if data is not None:
            values = list()
            await ctx.send('<:send:519896817320591385>│``PRECISO QUE VOCÊ RESPONDA A ALGUMAS PERGUNTAS!``',
                           delete_after=5.0)

            def check_option(m):
                return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

            def check_channel(m):
                return m.author == ctx.author and m.channel_mentions[0].id

            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o ActionLog?`` \n'
                                 '```O ActionLog serve para você verificar tudo o que ocorre no seu servidor atravez de'
                                 ' um canal de registro de ações.```\n'
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
            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o BotNews?`` \n'
                                 '```O BotNews é um canal onde vc vai receber em primeira mao todas as novidades da '
                                 'ashley```\n'
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
            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o Contador de membros?`` \n'
                                 '```O Contador de membros é um recurso onde a ashley edita um canal para mostrar '
                                 'quantos membros existem em seu servidor, em tempo real.```\n'
                                 '**1** para ``SIM`` ou **0** para ``NÃO``')

            resp_5 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
            values.append(resp_5.content)
            if resp_5.content == '1':
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do Contador de membros!``')

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
                    for letter in text:
                        list_.append(numbers[int(letter)])
                    await channel_.edit(topic="<a:caralho:525105064873033764> **Membros:** " + str(list_))

                    msg = await ctx.send('<:confirmado:519896822072999937>│``Contador de membros ativado!``')
                    await sleep(2)

                except discord.Forbidden:
                    await ctx.send("<:negate:520418505993093130>│``Não tenho permissão para editar canais "
                                   "nesse servidor!``", delete_after=5.0)
            else:
                values.append(-1)
            await msg.delete()
            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o Registro de entrada de '
                                 'membros?`` \n'
                                 '```Esse recurso registra em um canal a entrada de novos membros, quando ele entrou, '
                                 'etc```\n'
                                 '**1** para ``SIM`` ou **0** para ``NÃO``')

            resp_7 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
            values.append(resp_7.content)
            if resp_7.content == '1':
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do Registro de Entrada '
                                     'de Membros!``')

                resp_8 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                values.append(resp_8.channel_mentions[0].id)
                await msg.delete()

                msg = await ctx.send('<:confirmado:519896822072999937>│``Registro de entrada de Membros ativado!``')
                await sleep(2)
            else:
                values.append(-1)
            await msg.delete()
            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o '
                                 'Registro de Saida de membros?``\n'
                                 '```Esse recurso registra em um canal a sainda de membros, quando ele saiu, '
                                 'etc```\n'
                                 ' **1** para ``SIM`` ou **0** para ``NÃO``')

            resp_9 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
            values.append(resp_9.content)
            if resp_9.content == '1':
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do '
                                     'Registro de Sainda de Membros!``')

                resp_10 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                values.append(resp_10.channel_mentions[0].id)
                await msg.delete()

                msg = await ctx.send('<:confirmado:519896822072999937>│``Registro de Saida de Membros ativado!``')
                await sleep(2)
            else:
                values.append(-1)
            await msg.delete()
            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o Sorteio de Membros?`` \n'
                                 '```O Sorteio de Membros serve para escolher um dos seus membros para receber premios '
                                 'da ashley, todo aqueles registrados em nossos sistemas vao ter muitas regalias.\n'
                                 'OBS: essa função apenas entrará em vigor em servidores com 50 ou mais membros e 10 '
                                 'ou mais membros cadastrados na ashley```\n'
                                 '**1** para ``SIM`` ou **0** para ``NÃO``')

            resp_11 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
            values.append(resp_11.content)
            if resp_11.content == '1':
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do Sorteio de Membros!``')

                resp_12 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                values.append(resp_12.channel_mentions[0].id)
                await msg.delete()

                msg = await ctx.send('<:confirmado:519896822072999937>│``Sorteio de Membros ativado!``')
                await sleep(2)
            else:
                values.append(-1)
            await msg.delete()
            msg = await ctx.send(
                '<:stream_status:519896814825242635>│``Você deseja ativar o Log de Programação de Ashley?`` \n'
                '```O Log de Programação de Ashley serve para que voce veja como ela foi programada, o codigo'
                ' de Ashley é aberto e todos podem ter a certeza de que nosso bot não tem nenhum codigo malicioso'
                ' presamos muito pela nossa imagem, alem de sempre queremos contribuir de alguma forma para a '
                'comunidade de bots do discord.```\n'
                '**1** para ``SIM`` ou **0** para ``NÃO``')

            resp_13 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
            values.append(resp_13.content)
            if resp_13.content == '1':
                await msg.delete()
                msg = await ctx.send(
                    '<:stream_status:519896814825242635>│``Marque o canal do Log de Programação de Ashley!``')

                resp_14 = await self.bot.wait_for('message', check=check_channel, timeout=60.0)
                values.append(resp_14.channel_mentions[0].id)
                await msg.delete()

                msg = await ctx.send('<:confirmado:519896822072999937>│``Log de Programação de Ashley ativado!``')
                await sleep(2)
            else:
                values.append(-1)
            await msg.delete()

            msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o meu '
                                 'Serviço de Interação com Membros?``\n'
                                 '```Esse serviço ativa as minhas interações com Inteligencia Artifical,'
                                 'meu sistema de perguntas e respostas alem de varias outras coisas legais e '
                                 'divertidas que eu posso fazer.```\n'
                                 ' **1** para ``SIM`` ou **0** para ``NÃO``')

            resp_15 = await self.bot.wait_for('message', check=check_option, timeout=60.0)
            values.append(resp_15.content)
            if resp_15.content == '1':
                await msg.delete()

                msg = await ctx.send(
                    '<:confirmado:519896822072999937>│``Serviço de Interação com Membros ativado!``')
                await sleep(2)

            await msg.delete()

            keys = ['log', 'log_channel_id', 'ash_news', 'ash_news_id', 'cont_users', 'cont_users_id',
                    'member_join', 'member_join_id', 'member_remove', 'member_remove_id', 'ash_draw', 'ash_draw_id',
                    'ash_git', 'ash_git_id', 'auto_msg']
            c = 0

            msg = await ctx.send("<a:loading:520418506567843860>│"
                                 "``AGUARDE, ESTOU PROCESSANDO SEU CADASTRO!``")

            for key in keys:
                if c % 2 == 0:
                    if c == 0:
                        update['log_config'][key] = bool(int(values[c]))
                    if c == 2 or c == 10 or c == 12:
                        update['bot_config'][key] = bool(int(values[c]))
                    if c == 4 or c == 6 or c == 8:
                        update['func_config'][key] = bool(int(values[c]))
                    if c == 14:
                        update['ia_config'][key] = bool(int(values[c]))
                    c += 1
                else:
                    if values[c] == -1:
                        if c == 1:
                            update['log_config'][key] = None
                        if c == 3 or c == 11 or c == 13:
                            update['bot_config'][key] = None
                        if c == 5 or c == 7 or c == 9:
                            update['func_config'][key] = None
                    else:
                        if c == 1:
                            update['log_config'][key] = values[c]
                        if c == 3 or c == 11 or c == 13:
                            update['bot_config'][key] = values[c]
                        if c == 5 or c == 7 or c == 9:
                            update['func_config'][key] = values[c]
                    c += 1

            await self.bot.db.update_data(data, update, "guilds")
            await sleep(2)
            await msg.delete()

            await ctx.send('<:confirmado:519896822072999937>│**PARABENS** : '
                           '``CONFIGURAÇÃO REALIZADA COM SUCESSO!``', delete_after=5.0)

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @config.command(name='report', aliases=['reportar'])
    async def _report(self, ctx):
        """Comando usado pra configurar o report da Ashley
        Use ash config report e siga as instruções do comando(use # pra marcar os canais)"""
        data = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
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

            await self.bot.db.update_data(data, update, "guilds")
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


def setup(bot):
    bot.add_cog(ConfigClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mCONFIG\033[1;32m foi carregado com sucesso!\33[m')
