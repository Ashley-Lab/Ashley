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
    @commands.group(name='register', aliases=['registro', "registrar"])
    async def register(self, ctx):
        """ Usado pra registrar um usuario na ashley Exemplo: "ash register" """
        if ctx.invoked_subcommand is None:
            data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            if data_guild is None:
                return await ctx.send('<:negate:721581573396496464>│``Sua guilda ainda não está registrada, por '
                                      'favor digite:`` **ash register guild** ``para cadastrar sua guilda '
                                      'no meu`` **banco de dados!**')
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            if data is None and ctx.author.id in [r.id for r in ctx.guild.members if not r.bot]:
                await self.bot.db.add_user(ctx)
                data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
                update_guild = data_guild
                update_guild['data']['accounts'] += 1
                await self.bot.db.update_data(data_guild, update_guild, 'guilds')

                await ctx.send('<:confirmed:721581574461587496>│``Cadastro feito com sucesso!``')
            else:
                await ctx.send('<:negate:721581573396496464>│``Você já está registrado em meu banco de dados!``')

    @check_it(no_pm=True, manage_guild=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @register.command(name='guild', aliases=['guilda', "servidor"])
    async def _guild(self, ctx):
        """Usado pra registrar seu servidor na ashley
        Use ash register guild e siga as instruções do comando(use # pra marcar os canais)"""
        data = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        if data is None:
            values = list()
            await ctx.send('<:send:519896817320591385>│``PRECISO QUE VOCÊ RESPONDA A ALGUMAS PERGUNTAS!``',
                           delete_after=5.0)

            def check_option(m):
                return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

            def check_channel(m):
                while not m.bot.is_closed():
                    try:
                        return m.author == ctx.author and m.channel_mentions[0].id
                    except IndexError:
                        pass

            register = await ctx.send('<:stream_status:519896814825242635>│``VOCÊ DESEJA CONFIGURAR O SERVIDOR '
                                      'AGORA?!`` **1** para ``SIM`` ou **0** para ``NÃO``')

            resp = await self.bot.wait_for('message', check=check_option, timeout=30.0)

            if resp.content == '1':

                await register.delete()

                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o ActionLog?`` \n'
                                     '```O ActionLog serve para você verificar tudo o que ocorre no seu servidor '
                                     'atravez de um canal de registro de ações.```\n'
                                     '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_1 = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                values.append(resp_1.content)
                if resp_1.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do ActionLog!``')

                    resp_2 = await self.bot.wait_for('message', check=check_channel, timeout=30.0)
                    values.append(resp_2.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmed:721581574461587496>│``ActionLog ativado!``')
                    await sleep(2)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o BotNews?`` \n'
                                     '```O BotNews é um canal onde vc vai receber em primeira mao todas as novidades '
                                     'da ashley```\n'
                                     '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_3 = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                values.append(resp_3.content)
                if resp_3.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do BotNews!``')

                    resp_4 = await self.bot.wait_for('message', check=check_channel, timeout=30.0)
                    values.append(resp_4.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmed:721581574461587496>│``BotNews ativado!``')
                    await sleep(2)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send(
                    '<:stream_status:519896814825242635>│``Você deseja ativar o Contador de membros?`` \n'
                    '```O Contador de membros é um recurso onde a ashley edita um canal para mostrar '
                    'quantos membros existem em seu servidor, em tempo real.```\n'
                    '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_5 = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                values.append(resp_5.content)
                if resp_5.content == '1':
                    await msg.delete()
                    msg = await ctx.send(
                        '<:stream_status:519896814825242635>│``Marque o canal do Contador de membros!``')

                    resp_6 = await self.bot.wait_for('message', check=check_channel, timeout=30.0)
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

                        msg = await ctx.send('<:confirmed:721581574461587496>│``Contador de membros ativado!``')
                        await sleep(2)

                    except discord.Forbidden:
                        await ctx.send("<:negate:721581573396496464>│``Não tenho permissão para editar canais "
                                       "nesse servidor!``", delete_after=5.0)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send(
                    '<:stream_status:519896814825242635>│``Você deseja ativar o Registro de entrada de '
                    'membros?`` \n'
                    '```Esse recurso registra em um canal a entrada de novos membros, quando ele entrou, '
                    'etc```\n'
                    '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_7 = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                values.append(resp_7.content)
                if resp_7.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do Registro de Entrada '
                                         'de Membros!``')

                    resp_8 = await self.bot.wait_for('message', check=check_channel, timeout=30.0)
                    values.append(resp_8.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmed:721581574461587496>│``Registro de entrada de Membros ativado!``')
                    await sleep(2)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send('<:stream_status:519896814825242635>│``Você deseja ativar o '
                                     'Registro de Saida de membros?``\n'
                                     '```Esse recurso registra em um canal a sainda de membros, quando ele saiu, '
                                     'etc```\n'
                                     ' **1** para ``SIM`` ou **0** para ``NÃO``')

                resp_9 = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                values.append(resp_9.content)
                if resp_9.content == '1':
                    await msg.delete()
                    msg = await ctx.send('<:stream_status:519896814825242635>│``Marque o canal do '
                                         'Registro de Sainda de Membros!``')

                    resp_10 = await self.bot.wait_for('message', check=check_channel, timeout=30.0)
                    values.append(resp_10.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmed:721581574461587496>│``Registro de Saida de Membros ativado!``')
                    await sleep(2)
                else:
                    values.append(-1)
                await msg.delete()
                msg = await ctx.send(
                    '<:stream_status:519896814825242635>│``Você deseja ativar o Sorteio de Membros?`` \n'
                    '```O Sorteio de Membros serve para escolher um dos seus membros para receber premios '
                    'da ashley, todo aqueles registrados em nossos sistemas vao ter muitas regalias.\n'
                    'OBS: essa função apenas entrará em vigor em servidores com 50 ou mais membros e 10 '
                    'ou mais membros cadastrados na ashley```\n'
                    '**1** para ``SIM`` ou **0** para ``NÃO``')

                resp_11 = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                values.append(resp_11.content)
                if resp_11.content == '1':
                    await msg.delete()
                    msg = await ctx.send(
                        '<:stream_status:519896814825242635>│``Marque o canal do Sorteio de Membros!``')

                    resp_12 = await self.bot.wait_for('message', check=check_channel, timeout=30.0)
                    values.append(resp_12.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmed:721581574461587496>│``Sorteio de Membros ativado!``')
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

                resp_13 = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                values.append(resp_13.content)
                if resp_13.content == '1':
                    await msg.delete()
                    msg = await ctx.send(
                        '<:stream_status:519896814825242635>│``Marque o canal do Log de Programação de Ashley!``')

                    resp_14 = await self.bot.wait_for('message', check=check_channel, timeout=30.0)
                    values.append(resp_14.channel_mentions[0].id)
                    await msg.delete()

                    msg = await ctx.send('<:confirmed:721581574461587496>│``Log de Programação de Ashley ativado!``')
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

                resp_15 = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                values.append(resp_15.content)
                if resp_15.content == '1':
                    await msg.delete()

                    msg = await ctx.send(
                        '<:confirmed:721581574461587496>│``Serviço de Interação com Membros ativado!``')
                    await sleep(2)

                await msg.delete()

            else:
                await register.delete()

            keys = ['log', 'log_channel_id', 'ash_news', 'ash_news_id', 'cont_users', 'cont_users_id',
                    'member_join', 'member_join_id', 'member_remove', 'member_remove_id', 'ash_draw', 'ash_draw_id',
                    'ash_git', 'ash_git_id', 'auto_msg']

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

            await self.bot.db.add_guild(ctx.guild, data)
            await sleep(2)
            await msg.delete()

            await ctx.send('<:confirmed:721581574461587496>│**PARABENS** : '
                           '``CADASTRO FINALIZADO COM SUCESSO!``', delete_after=5.0)

        else:
            await ctx.send('<:alert:739251822920728708>│**ATENÇÃO** : '
                           '``essa guilda já está cadastrada!``')

    @_guild.error
    async def _guild_error(self, ctx, error):
        if error.__str__() in ERRORS[5]:
            return await ctx.send("<:negate:721581573396496464>│``Tempo esgotado, por favor tente novamente.``")
        if error.__str__() in ERRORS[4]:
            return await ctx.send('<:negate:721581573396496464>│``Você não marcou um canal de texto:`` '
                                  '**COMANDO CANCELADO**')


def setup(bot):
    bot.add_cog(RegisterClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mREGISTERCLASS\033[1;32m foi carregado com sucesso!\33[m')
