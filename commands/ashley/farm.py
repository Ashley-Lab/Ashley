import json
import discord

from resources.ia_list import areas_ctf
from resources.check import check_it
from discord.ext import commands
from asyncio import sleep
from resources.translation import t_
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)
resposta_area = -1
escolheu = False
msg_area_id = None


class FarmClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def add_role(self, ctx, roles, province):
        record = self.bot.db.get_data("user_id", ctx.author.id, "users")
        updates = record
        updates['config']['roles'] = roles
        updates['config']['provinces'] = province
        self.bot.db.update_data(record, updates, "users")

    async def add_hell(self, ctx, roles):
        record = self.bot.db.get_data("user_id", ctx.author.id, "users")
        updates = record
        updates['config']['roles'] = roles
        self.bot.db.update_data(record, updates, "users")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='respawn', aliases=['return'])
    async def respawn(self, ctx):
        if ctx.guild.id == _auth['default_guild']:
            cargos = ctx.author.roles
            record = self.bot.db.get_data("user_id", ctx.author.id, "users")
            updates = record
            if ctx.author.id == record["user_id"]:
                roles = record['config']['roles']
                if len(roles) > 0:
                    await ctx.send("<a:loading:520418506567843860>│``AGUARDE, ESTOU RETORNANDO VOCE "
                                   "PARA ONDE`` **VOCÊ ESTAVA**", delete_after=30.0)
                    for c in range(0, len(cargos)):
                        if cargos[c].name != "@everyone":
                            await ctx.author.remove_roles(cargos[c])
                            await sleep(1)
                    for c in range(0, len(roles)):
                        role = discord.utils.find(lambda r: r.name == roles[c], ctx.guild.roles)
                        await ctx.author.add_roles(role)
                        await sleep(1)
                    updates['config']['roles'] = []
                    updates['config']['provinces'] = None
                    self.bot.db.update_data(record, updates, "users")
                else:
                    await ctx.send("<:alert_status:519896811192844288>│``VOCE NAO TEM CARGOS NO BANCO DE "
                                   "DADOS!``")
        else:
            await ctx.send(
                t_(ctx, "<:oc_status:519896814225457152>│``Desculpe, mas apenas os`` **Membros do meu servidor** "
                        "``podem usar esse comando!``", "guilds"))

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='hell', aliases=['inferno'])
    async def hell(self, ctx):
        record = self.bot.db.get_data("user_id", ctx.author.id, "users")
        if ctx.author.id == record["user_id"]:
            if record['config']['provinces'] is None:
                if ctx.channel.id != 576795574783705104:
                    if ctx.guild.id == _auth['default_guild']:
                        await ctx.send("<a:loading:520418506567843860>│ ``AGUARDE, ESTOU LHE ENVINANDO PARA O "
                                       "SUB-MUNDO!``", delete_after=30.0)

                        rules = ctx.author.roles
                        roles = [r.name for r in ctx.author.roles if r.name != "@everyone"]
                        await self.add_hell(ctx, roles)

                        for c in range(0, len(rules)):
                            if rules[c].name != "@everyone":
                                await ctx.author.remove_roles(rules[c])
                                await sleep(1)
                        role = discord.utils.find(lambda r: r.name == "👺Mobrau👺", ctx.guild.roles)
                        await ctx.author.add_roles(role)

                    else:
                        await ctx.send(
                            t_(ctx,
                               "<:oc_status:519896814225457152>│``Desculpe, mas apenas os`` **Membros do meu servidor**"
                               " ``podem usar esse comando!``", "guilds"))
                else:
                    await ctx.send(f'<:oc_status:519896814225457152>│``Você já está no inferno!``')
            else:
                await ctx.send(f'<:oc_status:519896814225457152>│``Você está numa provincia! '
                               f'Retorne usando`` **({self.bot.prefix_} + respawn)** ``para conseguir '
                               f'ir para o sub-mundo primeiro``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='teleport', aliases=['teletransportar'])
    async def teleport(self, ctx):
        record = self.bot.db.get_data("user_id", ctx.author.id, "users")
        if ctx.author.id == record["user_id"]:
            if ctx.channel.id != 576795574783705104:
                if record['config']['provinces'] is None:
                    global msg_user_farm
                    msg_user_farm = ctx.author
                    if ctx.guild.id == _auth['default_guild']:
                        embed = discord.Embed(
                            title="Escolha a área que você deseja Ir:\n"
                                  "```COMANDO PARA VOLTAR AO CLAN ATUAL: ash.respawn```",
                            color=color,
                            description="- Para ir até **Etheria**: Clique em :crystal_ball:\n"
                                        "- Para ir até **Rauberior**: Clique em :lion_face:\n"
                                        "- Para ir até **Ilumiora**: Clique em :candle:\n"
                                        "- Para ir até **Kerontaris**: Clique em :skull:\n"
                                        "- Para ir até **Widebor**: Clique em :bird:\n"
                                        "- Para ir até **Jangalor**: Clique em :deciduous_tree:\n"
                                        "- Para ir até **Yotungar**: Clique em :dagger:\n"
                                        "- Para ir até **Shoguriar**: Clique em :japanese_castle:\n"
                                        "- Para ir até **Dracaris**: Clique em :fire:\n"
                                        "- Para ir até **Forgerion**: Clique em :hammer_pick:")
                        botmsg = await ctx.send(embed=embed)
                        await botmsg.add_reaction('🔮')
                        await botmsg.add_reaction('🦁')
                        await botmsg.add_reaction('🕯')
                        await botmsg.add_reaction('💀')
                        await botmsg.add_reaction('🐦')
                        await botmsg.add_reaction('🌳')
                        await botmsg.add_reaction('🗡')
                        await botmsg.add_reaction('🏯')
                        await botmsg.add_reaction('🔥')
                        await botmsg.add_reaction('⚒')
                        global msg_area_id
                        msg_area_id = botmsg.id
                        area = 0
                        while True:
                            if escolheu is True and area > resposta_area:
                                area = 0
                            if area == resposta_area:
                                break
                            if area >= 30:
                                await ctx.send("<:oc_status:519896814225457152>│``Você demorou demais pra "
                                               "escolher`` **COMANDO CANCELADO!**")
                                break
                            area += 1
                            await sleep(1)
                        if resposta_area != -1:
                            rules = ctx.author.roles

                            roles = [r.name for r in ctx.author.roles if r.name != "@everyone"]
                            await self.add_role(ctx, roles, areas_ctf[resposta_area])

                            for c in range(0, len(rules)):
                                if rules[c].name != "@everyone":
                                    await ctx.author.remove_roles(rules[c])
                                    await sleep(1)
                            role = discord.utils.find(lambda r: r.name == areas_ctf[resposta_area], ctx.guild.roles)
                            await ctx.author.add_roles(role)
                        await botmsg.delete()
                    else:
                        await ctx.send(
                            t_(ctx,
                               "<:oc_status:519896814225457152>│``Desculpe, mas apenas os`` **Membros do meu servidor**"
                               " ``podem usar esse comando!``", "guilds"))
                else:
                    await ctx.send(f'<:oc_status:519896814225457152>│``Você já está numa provincia! '
                                   f'Retorne usando`` **({self.bot.prefix_} + respawn)** ``para conseguir '
                                   f'ir para outra provincia primeiro``')
            else:
                await ctx.send(f'<:oc_status:519896814225457152>│``Você está no sub-mundo! '
                               f'Retorne usando`` **({self.bot.prefix_} + respawn)** ``para conseguir '
                               f'ir para uma provincia primeiro``')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        msg = reaction.message
        canal = self.bot.get_channel(reaction.message.channel.id)

        global resposta_area
        global escolheu

        if reaction.emoji == "🔮" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 0
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "🦁" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 1
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "🕯" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 2
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "💀" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 3
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "🐦" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 4
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "🌳" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 5
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "🗡" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 6
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "🏯" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 7
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "🔥" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 8
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()

        if reaction.emoji == "⚒" and msg.id == msg_area_id and msg_user_farm == user:
            if resposta_area == -1:
                resposta_area = 9
                escolheu = True
                msg_final = await canal.send("<a:loading:520418506567843860>│"
                                             "``AGUARDE, ESTOU PROCESSANDO SUA ESCOLHA!``")
                await sleep(30)
                resposta_area = -1
                await msg_final.delete()


def setup(bot):
    bot.add_cog(FarmClass(bot))
    print('\033[1;32mO comando \033[1;34mFARM\033[1;32m foi carregado com sucesso!\33[m')
