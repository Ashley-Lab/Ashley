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
                                  f"{self.st[30]} `pagar   ` Paga uma quantia de **ETHERNYAS** a um usuário.\n"
                                  f"{self.st[30]} `dar     ` Oferece uma quantidade de um **ITEM** a um usuário.\n"
                                  f"{self.st[87]} `rifa    ` Tente conseguir um **ARTEFATO** para seu perfil.\n"
                                  f"{self.st[87]} `transfer` Transfere sua conta para outro servidor.\n"
                                  f"{self.st[66]} `diario  ` Lista os comandos de recompensas diárias.\n"
                                  f"`🔴` `loja    ` Abre um menu com diversos itens para compra.")
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
                            value=f"{self.st[43]} `skill   ` ...\n"
                                  f"{self.st[43]} `batalha ` ...\n"
                                  f"{self.st[4]} `caixa   ` ...\n"
                                  f"{self.st[66]} `diario  ` ...\n"
                                  f"{self.st[30]} `rec     ` ...\n"
                                  f"{self.st[96]} `gift    ` ...\n"
                                  f"{self.st[96]} `open    ` ...\n"
                                  f"{self.st[97]} `craft   ` ...\n"
                                  f"{self.st[97]} `recipe  ` ...\n"
                                  f"{self.st[88]} `i       ` ...\n")
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
                            value=f"{self.st[76]} `pet     ` ...\n")
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
                            value=f"{self.st[24]} `reflita ` ...\n"
                                  f"{self.st[16]} `pensador` ...\n"
                                  f"{self.st[14]} `palin   ` ...\n"
                                  f"{self.st[15]} `diga    ` ...\n"
                                  f"{self.st[10]} `textao  ` ...\n"
                                  f"{self.st[12]} `fofoca  ` ...\n"
                                  f"{self.st[13]} `abraço  ` ...\n"
                                  f"{self.st[71]} `beijo   ` ...\n"
                                  f"{self.st[72]} `lambida ` ...\n"
                                  f"{self.st[80]} `dançar  ` ...\n"
                                  f"{self.st[89]} `facebook` ...\n"
                                  f"{self.st[90]} `insta   ` ...\n"
                                  f"{self.st[91]} `twitter ` ...\n"
                                  f"{self.st[92]} `zap     ` ...\n"
                                  f"{self.st[70]} `chute   ` ...\n"
                                  f"{self.st[74]} `empurrao` ...\n"
                                  f"{self.st[75]} `tapa    ` ...\n"
                                  f"{self.st[73]} `soco    ` ...\n")
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
                            value=f"{self.st[11]} `gif       ` ...\n"
                                  f"{self.st[5]} `ping      ` ...\n"
                                  f"{self.st[47]} `rolar     ` ...\n"
                                  f"{self.st[2]} `feedback  ` ...\n"
                                  f"{self.st[21]} `serverinfo` ...\n"
                                  f"{self.st[26]} `userinfo  ` ...\n"
                                  f"{self.st[22]} `roleinfo  ` ...\n"
                                  f"{self.st[3]} `botinfo   ` ...\n"
                                  f"{self.st[78]} `perfil    ` ...\n"
                                  f"{self.st[45]} `sorteio   ` ...\n"
                                  f"{self.st[8]} `convite   ` ...\n"
                                  f"{self.st[20]} `emoji     ` ...\n"
                                  f"{self.st[44]} `avatar    ` ...\n"
                                  f"{self.st[79]} `casar     ` ...\n"
                                  f"{self.st[82]} `bok       ` ...\n"
                                  f"{self.st[79]} `separar   ` ...\n"
                                  f"{self.st[46]} `rank      ` ...\n"
                                  f"{self.st[67]} `top       ` ...")
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
                                  f"{self.st[39]} `source         ` ...\n"
                                  f"{self.st[32]} `announce       ` ...\n"
                                  f"{self.st[1]} `staff delete   ` ...\n"
                                  f"{self.st[1]} `staff ban      ` ...\n"
                                  f"{self.st[1]} `staff kick     ` ...\n"
                                  f"{self.st[1]} `staff slowmode ` ...\n"
                                  f"{self.st[1]} `staff report   ` ...\n"
                                  f"{self.st[0]} `config         ` ...\n"
                                  f"{self.st[42]} `log            ` ...\n"
                                  f"{self.st[31]} `channel        ` ...")
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
                            value=f"{self.st[33]} ``md        `` ...\n"
                                  f"{self.st[32]} ``verify    `` ...\n"
                                  f"{self.st[40]} ``tdc       `` ...\n"
                                  f"{self.st[34]} ``eval      `` ...\n"
                                  f"{self.st[38]} ``rc        `` ...\n"
                                  f"{self.st[35]} ``load      `` ...\n"
                                  f"{self.st[41]} ``unload    `` ...\n"
                                  f"{self.st[37]} ``reload    `` ...\n"
                                  f"{self.st[36]} ``logout    `` ...\n"
                                  f"{self.st[86]} ``add_ban   `` ...\n"
                                  f"{self.st[86]} ``remove_ban`` ...\n"
                                  f"{self.st[86]} ``add_vip   `` ...\n"
                                  f"{self.st[86]} ``remove_vip`` ...\n")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            await botmsg[user.id].edit(embed=embed)
            await self.add_reactions(user)
            if user.id in self.bot.staff:
                await botmsg[user.id].add_reaction('🛡')


def setup(bot):
    bot.add_cog(Helper(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mAJUDA\033[1;32m foi carregado com sucesso!\33[m')
