import json
import discord

from discord.ext import commands
from asyncio import TimeoutError
from resources.check import check_it
from resources.db import Database

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

color = int(_auth['default_embed'], 16)


class StatusClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='status', aliases=['habilidades'])
    async def status(self, ctx):
        if ctx.invoked_subcommand is None:
            data = self.bot.db.get_data("user_id", ctx.author.id, "users")
            if ctx.author.id == data["user_id"]:
                resposta = discord.Embed(
                    title='Escolha onde você quer adiconar seu ponto de habilidade:',
                    color=color,
                    description='**ATUALMENTE VOCÊ TEM {} PONTOS DE HABILIDADES DISPONIVEIS**\n'
                                '``E ABAIXO SE ENCONTRA SEUS PONTOS DISTRIBUIDOS:``\n'
                                '**1**: ``Strenght - {}``\n**2**: ``Constitution - {}``\n**3**: ``Dexterity - {}``\n'
                                '**4**: ``Inteligence - {}``\n**5**: ``Lucky - {}``'.format(data['status']['PDH'],
                                                                                            data['status']['STR'],
                                                                                            data['status']['CON'],
                                                                                            data['status']['DEX'],
                                                                                            data['status']['INT'],
                                                                                            data['status']['LUC']))
                resposta.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                resposta.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                resposta.set_footer(text="Ashley ® Todos os direitos reservados.")
                await ctx.channel.send(embed=resposta, delete_after=60.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @status.command(name='add', aliases=['adicionar'])
    async def _add(self, ctx):
        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if ctx.author.id == data["user_id"]:
            resposta = discord.Embed(
                title='Escolha onde você quer adiconar seu ponto de habilidade:',
                color=color,
                description='**ATUALMENTE VOCÊ TEM {} PONTOS DE HABILIDADE**\n'
                            '``QUAL HABILIDADE VOCE DESEJA AUMENTAR?``\n'
                            '**1**: ``{}``\n**2**: ``{}``\n**3**: ``{}``\n'
                            '**4**: ``{}``\n**5**: ``{}``'.format(data['status']['PDH'], 'STR',
                                                                  'CON', 'DEX', 'INT', 'LUC'))
            resposta.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
            resposta.set_thumbnail(url="{}".format(ctx.author.avatar_url))
            resposta.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.channel.send(embed=resposta, delete_after=60.0)

            def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()

            try:
                option = await self.bot.wait_for('message', check=is_correct, timeout=15.0)
            except TimeoutError:
                return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito! Comando '
                                      'cancelado.``', delete_after=5.0)
            option = int(option.content)
            if update['status']['PDH'] > 0:
                if option == 1:
                    update['status']['STR'] += 1
                    update['status']['PDH'] -= 1
                elif option == 2:
                    update['status']['CON'] += 1
                    update['status']['PDH'] -= 1
                elif option == 3:
                    update['status']['DEX'] += 1
                    update['status']['PDH'] -= 1
                elif option == 4:
                    update['status']['INT'] += 1
                    update['status']['PDH'] -= 1
                elif option == 5:
                    update['status']['LUC'] += 1
                    update['status']['PDH'] -= 1
                else:
                    return await ctx.send('<:negate:520418505993093130>│``Opção Invalida!``', delete_after=5.0)
                self.bot.db.update_data(data, update, "users")
                await ctx.send('<:confirmado:519896822072999937>│``Ponto adicionado com sucesso!``', delete_after=5.0)
            else:
                await ctx.send('<:negate:520418505993093130>│``Você não tem pontos de habilidades disponiveis!``',
                               delete_after=5.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @status.command(name='reset', aliases=['resetar'])
    async def _reset(self, ctx):
        data = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if ctx.author.id == data["user_id"]:
            update['status']['STR'] = 1
            update['status']['CON'] = 1
            update['status']['DEX'] = 1
            update['status']['INT'] = 1
            update['status']['LUC'] = 1
            update['status']['PDH'] = update['user']['level'] - 1
            self.bot.db.update_data(data, update, "users")
            await ctx.send('<:confirmado:519896822072999937>│``Status resetados com sucesso!``', delete_after=5.0)


def setup(bot):
    bot.add_cog(StatusClass(bot))
    print('\033[1;32mO comando \033[1;34mSTATUSCLASS\033[1;32m foi carregado com sucesso!\33[m')
