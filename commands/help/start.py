import copy
import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database

botmsg = {}


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.st = []
        self.color = self.bot.color
        self.cont = 0

    def status(self):
        for v in self.bot.data_cog.values():
            self.st.append(v)

    async def add_reactions(self, user: discord.Member):
        self.cont += 1
        await botmsg[user.id].add_reaction('🧭')
        await botmsg[user.id].add_reaction('🎙️')
        await botmsg[user.id].add_reaction('💰')
        await botmsg[user.id].add_reaction('🎲')
        await botmsg[user.id].add_reaction('⚔')
        await botmsg[user.id].add_reaction('🐻')
        await botmsg[user.id].add_reaction('🌎')
        await botmsg[user.id].add_reaction('📢')
        await botmsg[user.id].add_reaction('👮🏽‍♂️')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='help_cont', aliases=['ajuda_contador'])
    async def help_cont(self, ctx):
        await ctx.send(f"**Quantidade de vezes que o ajuda foi paginado:** ``{self.cont}``**!**")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='help', aliases=['ajuda'])
    async def help(self, ctx, *, command_help=None):
        """há fala serio!"""
        if command_help is None:
            self.status()
            embed = discord.Embed(title="-==Artigo de Ajuda==-\nPara detalhar o comando use: ash help <command>",
                                  color=self.color, description=f"Olá {ctx.author.name}, eu sou a **Ashley**, um bot "
                                                                f"de diversão e jogos, incluindo RPG de turnos e "
                                                                f"sistemas de economia e moderação completos!")

            embed.add_field(name="**Um pouco acerca dos meus sistemas**",
                            value=">>> Possuo um sistema de economia muito completo e fechado, ou seja, o meu dono "
                                  "não tem controle sobre ele. É um sistema que tem vindo a ser atualizado ao longo "
                                  "do tempo para que possa ser o mais semelhante possível à economia real.\nExiste "
                                  "também um sistema de RPG, que se baseia em juntar itens para criar equipamentos "
                                  "melhores e batalhar contra monstros mais fortes!\nPor fim, mas não menos "
                                  "importante, temos o sistema de moderação avançado, feito com rigor de forma a "
                                  "impedir que jogadores abusivos arruinem a experiência de todos os usuários.",
                            inline=False)

            embed.add_field(name="**Entretenimento**",
                            value=">>> Existem categorias de entretenimento que contêm (mini)jogos e outros diversos. "
                                  "Se você é um colecionador, irá adorar o meu sistema de coleção de artefactos e de "
                                  "Pets!\n\nO sistema de Pets consiste em capturar, cuidar e evoluí-los, de forma a "
                                  "torná-los os seus melhores amigos. Nenhum esforço é em vão, eles irão compensar "
                                  "você por se dedicar tanto a eles!", inline=False)

            embed.add_field(name="**Categorias**",
                            value=">>> "
                                  "🎙️ — Interações com a IA\n"
                                  "💰 — Economia\n"
                                  "🎲 — Mini Jogos\n"
                                  "⚔ — Rpg\n"
                                  "🐻 — Pets\n"
                                  "🌎 — Diversos\n"
                                  "📢 — Utilidade\n"
                                  "👮🏽‍♂️ — Staff\n\n"
                                  "_Para obter uma lista de comandos referentes a cada categoria, basta "
                                  "clicar na reação abaixo correspondente._\n\n"
                                  "_Para voltar à página inicial, reaja com 🧭_", inline=False)

            embed.add_field(name="**Estado dos comandos**",
                            value=">>> Todos os comandos possuem um estado para que seja fácil entender se estão "
                                  "disponíveis ou não para uso.\nAbaixo está uma lista com referências aos diversos "
                                  "estados, que aparecerão antes do nome dos comandos.\n\n`🟢  Disponível           "
                                  "   `\n`🟡  Com possíveis problemas `\n`🔴  Desativado              `\n`🟣  VIP  "
                                  "                   `", inline=False)

            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="http://sisadm2.pjf.mg.gov.br/imagem/ajuda.png")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            global botmsg
            try:
                botmsg[ctx.author.id] = await ctx.author.send(embed=embed)
                if ctx.message.guild is not None:
                    await ctx.send('<:send:519896817320591385>│``ENVIADO PARA O SEU PRIVADO!``')
                await self.add_reactions(ctx.author)
                if ctx.author.id in self.bot.staff:
                    await botmsg[ctx.author.id].add_reaction('🛡')
            except discord.errors.Forbidden:
                botmsg[ctx.author.id] = await ctx.send(embed=embed)
                await self.add_reactions(ctx.author)
                if ctx.author.id in self.bot.staff:
                    await botmsg[ctx.author.id].add_reaction('🛡')
        else:
            msg = copy.copy(ctx.message)
            msg.content = 'ash ' + command_help
            ctx_ = await self.bot.get_context(msg)
            if ctx_.command is not None:
                if ctx_.command.help is not None:
                    return await ctx.send(f"```{ctx_.command.help}```")
                await ctx.send("<:alert_status:519896811192844288>│``Comando Ainda nao tem uma ajuda definida``")
            else:
                await ctx.send("<:alert_status:519896811192844288>│``Comando Inválido``")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        try:
            if botmsg[user.id]:
                pass
        except KeyError:
            return

        if reaction.emoji == "🧭" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="-==Artigo de Ajuda==-\nPara detalhar o comando use: ash help <command>",
                color=self.color,
                description=f"Olá {user.name}, eu sou a **Ashley**, um bot de diversão e jogos, "
                            f"incluindo RPG de turnos e sistemas de economia e moderação completos!")

            embed.add_field(name="**Um pouco acerca dos meus sistemas**",
                            value=">>> Possuo um sistema de economia muito completo e fechado, ou seja, o meu dono "
                                  "não tem controle sobre ele. É um sistema que tem vindo a ser atualizado ao longo "
                                  "do tempo para que possa ser o mais semelhante possível à economia real.\nExiste "
                                  "também um sistema de RPG, que se baseia em juntar itens para criar equipamentos "
                                  "melhores e batalhar contra monstros mais fortes!\nPor fim, mas não menos "
                                  "importante, temos o sistema de moderação avançado, feito com rigor de forma a "
                                  "impedir que jogadores abusivos arruinem a experiência de todos os usuários.",
                            inline=False)

            embed.add_field(name="**Entretenimento**",
                            value=">>> Existem categorias de entretenimento que contêm (mini)jogos e outros diversos. "
                                  "Se você é um colecionador, irá adorar o meu sistema de coleção de artefactos e de "
                                  "Pets!\nO sistema de Pets consiste em capturar, cuidar e evoluí-los, de forma a "
                                  "torná-los os seus melhores amigos. Nenhum esforço é em vão, eles irão compensar "
                                  "você por se dedicar tanto a eles!", inline=False)

            embed.add_field(name="**Categorias**",
                            value=">>> "
                                  "🎙️ — Interações com a IA\n"
                                  "💰 — Economia\n"
                                  "🎲 — Mini Jogos\n"
                                  "⚔ — Rpg\n"
                                  "🐻 — Pets\n"
                                  "🌎 — Diversos\n"
                                  "📢 — Utilidade\n"
                                  "👮🏽‍♂️ — Staff\n\n"
                                  "_Para obter uma lista de comandos referentes a cada categoria, basta "
                                  "clicar na reação abaixo correspondente._\n\n"
                                  "_Para voltar à página inicial, reaja com 🧭_", inline=False)

            embed.add_field(name="**Estado dos comandos**",
                            value=">>> Todos os comandos possuem um estado para que seja fácil entender se estão "
                                  "disponíveis ou não para uso.\nAbaixo está uma lista com referências aos diversos "
                                  "estados, que aparecerão antes do nome dos comandos.\n\n`🟢  Disponível           "
                                  "   `\n`🟡  Com possíveis problemas `\n`🔴  Desativado              `\n`🟣  VIP  "
                                  "                   `", inline=False)

            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="http://sisadm2.pjf.mg.gov.br/imagem/ajuda.png")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🎙️" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(color=self.color,
                                  description=f"Inteligência Artificial, mais conhecida como IA, é uma inteligência "
                                              f"semelhante à humana, pertencente a sistemas tecnológicos. Por palavras"
                                              f" mais simples, é como se as \"máquinas\" tivessem mente própria.\nEu "
                                              f"proporciono um sistema de IA que, atualmente, responde a mensagens dos"
                                              f" membros, desde bons-dias e boas-noites até várias perguntas ou até "
                                              f"mesmo brincar consigo, e pode ser ativado/desativado utilizando o "
                                              f"comando abaixo.\n\n_Note que, para usufruir deste sistema de IA "
                                              f"totalmente, terá que ativar o meu Serviço de Interação com Membros "
                                              f"(SIM) através do comando `ash config guild`.\nNote também que existe "
                                              f"uma diferença entre o SIM e o comando `ash ia`. O SIM ativa a IA em si"
                                              f" e o comando ativa as respostas automáticas, ou seja, eu irei responder"
                                              f" a você mesmo quando você não fale comigo diretamente!_")
            embed.set_author(name="Ashley — Comandos de IA", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://i.dlpng.com/static/png/6689410_preview.png")
            embed.add_field(name="🎙️",
                            value=f"{self.st[95]} `ia      ` Habilita/Desabilita a interação com a IA.\n")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "💰" and reaction.message.id == botmsg[user.id].id:
            link = "http://www.pngmart.com/files/7/Money-PNG-Transparent-Image.png"
            embed = discord.Embed(color=self.color)
            embed.set_author(name="Ashley — Comandos de Economia", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=link)
            embed.add_field(name="💰",
                            value=f"{self.st[28]} `economia` Mostra a quantidade total de **ETHERNYAS** do Bot.\n"
                                  f"{self.st[29]} `tesouro ` Mostra a quantidade de **ETHERNYAS** no servidor.\n"
                                  f"{self.st[30]} `carteira` Mostra a quantidade das suas **ETHERNYAS**.\n"
                                  f"{self.st[29]} `guild   ` Comandos que usa o tesouro da guilda.\n"
                                  f"{self.st[30]} `pagar   ` Paga uma quantia de **ETHERNYAS** a um usuário.\n"
                                  f"{self.st[30]} `dar     ` Oferece uma quantidade de um **ITEM** a um usuário.\n"
                                  f"{self.st[87]} `rifa    ` Tente conseguir um **ARTEFATO** para seu perfil.\n"
                                  f"{self.st[87]} `bollash ` Tente dropar uma **BOLLASH** no seu inventario.\n"
                                  f"{self.st[87]} `transfer` Transfere sua conta para outro servidor.\n"
                                  f"{self.st[66]} `diario  ` Lista os comandos de recompensas diárias.")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🎲" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(color=self.color)
            embed.set_author(name="Ashley — Comandos de Mini Jogos", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/897/PNG/512/1-03_icon-icons.com_69189.png")
            embed.add_field(name="🎲",
                            value=f"{self.st[18]} `advinhe ` Tente acerdar um numero de 0 à 5\n"
                                  f"{self.st[19]} `jkp     ` Jogue pedra, pape ou tesoura\n"
                                  f"{self.st[17]} `moeda   ` Jogue cara ou coroa\n"
                                  f"{self.st[68]} `yugioh  ` Tente acertar o nome de uma carta\n"
                                  f"{self.st[69]} `charada ` Tente acertar uma charada\n"
                                  f"{self.st[81]} `pokemon ` Tente acertar o nome de um pokemon\n"
                                  f"{self.st[77]} `forca   ` Jogue o jogo da forca\n")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "⚔" and reaction.message.id == botmsg[user.id].id:
            link = "https://pt.seaicons.com/wp-content/uploads/2015/07/Iron-Sword-icon.png"
            embed = discord.Embed(color=self.color)
            embed.set_author(name="Ashley — Comandos do RPG", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=link)
            embed.add_field(name="⚔",
                            value=f"{self.st[43]} `skill      ` Seu painel de progresso do RPG.\n"
                                  f"{self.st[43]} `batalha    ` Batalhe contra monstros poderosos.\n"
                                  f"{self.st[4]} `caixa      ` Compre itens para criar suas armaduras.\n"
                                  f"{self.st[66]} `diario     ` Reinvidique seus premios diarios.\n"
                                  f"{self.st[30]} `rec        ` De ate 5 recomendações para seus amigos.\n"
                                  f"{self.st[98]} `lover      ` Ganha meu cargo de amor.\n"
                                  f"{self.st[98]} `unlover    ` Perde meu cargo de amor.\n"
                                  f"{self.st[96]} `gift       ` Use seu codigo promocional.\n"
                                  f"{self.st[96]} `open       ` Abra um presente e descubra algo incrivel.\n"
                                  f"{self.st[97]} `craft      ` Crie seus itens para ser o melhor no rpg.\n"
                                  f"{self.st[97]} `recipe     ` Olhe todas as receitas disponiveis.\n"
                                  f"{self.st[99]} `derreter   ` Use seus artefatos, para o item GOD.\n"
                                  f"{self.st[101]} `identificar` Identifique suas ?-Bollash.\n"
                                  f"{self.st[88]} `i          ` Abre seu inventario e veja tudo o que tem.\n")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🐻" and reaction.message.id == botmsg[user.id].id:
            link = "https://cdn.iconscout.com/icon/free/png-256/dog-face-tongue-human-friend-33944.png"
            embed = discord.Embed(color=self.color)
            embed.set_author(name="Ashley — Comandos de PET", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=link)
            embed.add_field(name="🐻",
                            value=f"`🔴` `pet     ` ...\n")  # {self.st[76]}
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🌎" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(color=self.color)
            embed.set_author(name="Ashley — Comandos Diversos", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="http://www.pngall.com/wp-content/uploads/2016/06/Earth-Free-PNG-Image-180x180.png")
            embed.add_field(name="🌎",
                            value=f"{self.st[24]} `reflita ` Tenha seu momento de reflexão diario.\n"
                                  f"{self.st[16]} `pensador` Uma frase aleatoria, para voce se divertir.\n"
                                  f"{self.st[14]} `palin   ` Frases que sao a mesma coisa de tras pra frente.\n"
                                  f"{self.st[15]} `diga    ` Me faça dizer algo, não seja timido.\n"
                                  f"{self.st[10]} `textao  ` Me faça dizer algo bem grande.\n"
                                  f"{self.st[12]} `fofoca  ` Revele aquela fofoca, depois eu apago. rsrs\n"
                                  f"{self.st[13]} `abraço  ` De um abraço em quem voce ama.\n"
                                  f"{self.st[71]} `beijo   ` De uma beijoca na sua paixao.\n"
                                  f"{self.st[72]} `lambida ` Depois de uma lambida, tudo fica mais feliz.\n"
                                  f"{self.st[80]} `dançar  ` Dance com seu perceiro preferido.\n"
                                  f"{self.st[89]} `facebook` Simule uma postagem no facebook.\n"
                                  f"{self.st[90]} `insta   ` Simule uma postagem no instagram.\n"
                                  f"{self.st[91]} `twitter ` Simule uma postagem no twitter.\n"
                                  f"{self.st[92]} `zap     ` Simule uma postagem no whatsapp.\n"
                                  f"{self.st[70]} `chute   ` Desconte sua raiva em alguem.\n"
                                  f"{self.st[74]} `empurrao` Empurre aquela pessoa que te fez mal.\n"
                                  f"{self.st[75]} `tapa    ` De um tapa na cara da sociedade.\n"
                                  f"{self.st[73]} `soco    ` Um murro para desestressar\n")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "📢" and reaction.message.id == botmsg[user.id].id:
            link = "https://image.freepik.com/vetores-gratis/caixa-de-ferramentas-com-muitas-ferramentas_1308-35876.jpg"
            embed = discord.Embed(color=self.color)
            embed.set_author(name="Ashley — Comandos de Utilidade", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=link)
            embed.add_field(name="📢",
                            value=f"{self.st[79]} `casar     ` Case com o amor da sua vida.\n"
                                  f"{self.st[82]} `bok       ` Comando exclusivo para casados. +18\n"
                                  f"{self.st[79]} `separar   ` Se nao deu certo, se separe...\n"
                                  f"{self.st[11]} `gif       ` Pesquise um gif bem bonitinho.\n"
                                  f"{self.st[5]} `ping      ` Veja minha latencia, estou sempre pronta.\n"
                                  f"{self.st[47]} `rolar     ` Role um dado no padrao quantidade_X_lados.\n"
                                  f"{self.st[2]} `feedback  ` Deixe sua sugestão ou relate um bug.\n"
                                  f"{self.st[21]} `serverinfo` Informações uteis sobre o **Servidor**.\n"
                                  f"{self.st[26]} `userinfo  ` Informações uteis sobre o **Usuario**.\n"
                                  f"{self.st[22]} `roleinfo  ` Informações uteis sobre um **Cargo**.\n"
                                  f"{self.st[3]} `botinfo   ` Informações uteis sobre **EUZINHA**.\n"
                                  f"{self.st[78]} `perfil    ` Veja seu perfil, lindao e bonitao.\n"
                                  f"{self.st[45]} `sorteio   ` Faça um sorteio de um membro.\n"
                                  f"{self.st[8]} `convite   ` Entre no meu servidor de suporte.\n"
                                  f"{self.st[20]} `emoji     ` Veja todos os emojis do servidor.\n"
                                  f"{self.st[44]} `avatar    ` Olhe sua foto toda lindona.\n"
                                  f"{self.st[46]} `rank      ` Veja seu rank no meu sistema.\n"
                                  f"{self.st[67]} `top       ` Todos os tops disponiveis para voce.")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "👮🏽‍♂️" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(color=self.color)
            embed.set_author(name="Ashley — Comandos de Staff", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="http://mieinfo.com/wp-content/uploads/2013/08/policia-mie.png")
            embed.add_field(name="👮🏽‍♂️",
                            value=f"`🔴` `reception      ` ...\n"  # {self.st[94]}
                                  f"`🔴` `door           ` ...\n"  # {self.st[48]}
                                  f"{self.st[39]} `source         ` Olhe meu codigo fonte.\n"
                                  f"{self.st[32]} `announce       ` Mande um anuncio para eu divulgar.\n"
                                  f"{self.st[1]} `staff delete   ` Exclua ate as ultimas 100 mensagens.\n"
                                  f"{self.st[1]} `staff ban      ` Bana um membro incoveniente.\n"
                                  f"{self.st[1]} `staff kick     ` Espulse um engraçadinho que se achou.\n"
                                  f"{self.st[1]} `staff slowmode ` Ative o modo lento em um canal.\n"
                                  f"{self.st[1]} `staff report   ` Reporte um membro para um moderador.\n"
                                  f"{self.st[98]} `status         ` Veja seus estados em tempo real.\n"
                                  f"{self.st[0]} `config         ` Veja minhas configurações.\n"
                                  f"{self.st[42]} `log            ` Ative ou desative alguns dos logs.\n"
                                  f"{self.st[31]} `channel        ` Sistema de bloqueio de comandos.")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')

        if reaction.emoji == "🛡" and reaction.message.id == botmsg[user.id].id:
            link = "http://www.creativemultimediainstitute.in/images/pages/computer-programming-language-classes.png"
            embed = discord.Embed(color=self.color)
            embed.set_author(name="Ashley — Comandos Owner", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=link)
            embed.add_field(name="🛡",
                            value=f"{self.st[33]} ``md        `` Criar o arquivo README.\n"
                                  f"{self.st[32]} ``verify    `` Verificar um ANUNCIO.\n"
                                  f"{self.st[40]} ``tdc       `` Total de Comandos Usados.\n"
                                  f"{self.st[34]} ``eval      `` Programar com o bot ligado.\n"
                                  f"{self.st[38]} ``rc        `` Repetir comandos.\n"
                                  f"{self.st[35]} ``load      `` Carregar um dos COGS.\n"
                                  f"{self.st[41]} ``unload    `` Desativar um dos COGS.\n"
                                  f"{self.st[37]} ``reload    `` Recarregar um dos COGS.\n"
                                  f"{self.st[36]} ``logout    `` Desligar a ashley.\n"
                                  f"{self.st[98]} ``cg        `` Cria um GIFT instantaneo.\n"
                                  f"{self.st[46]} ``stars     `` Adiciona ou retira estrelas.\n"
                                  f"{self.st[86]} ``add_ban   `` Banir um membro ou guilda.\n"
                                  f"{self.st[86]} ``remove_ban`` Desbanir um membro ou guilda.\n"
                                  f"{self.st[86]} ``add_vip   `` Tornar um membro ou guilda vip.\n"
                                  f"{self.st[86]} ``remove_vip`` Retirar o vip de um membro ou guilda.\n")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')


def setup(bot):
    bot.add_cog(Helper(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mAJUDA\033[1;32m foi carregado com sucesso!\33[m')
