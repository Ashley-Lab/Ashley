import discord

from discord.ext import commands
from asyncio import TimeoutError
from resources.check import check_it
from resources.db import Database


class SkillClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='skill', aliases=['habilidade', 'status'])
    async def skill(self, ctx):
        """Comando usado pra ver seus status no rpg da Ashley
        Use ash skill"""
        if ctx.invoked_subcommand is None:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            if ctx.author.id == data["user_id"]:
                resposta = discord.Embed(
                    title='Escolha onde você quer adiconar seu ponto de habilidade:',
                    color=self.color,
                    description='**ATUALMENTE VOCÊ TEM {} PONTOS DE HABILIDADES DISPONIVEIS**\n'
                                '``E ABAIXO SE ENCONTRA SEUS PONTOS DISTRIBUIDOS:``\n'
                                '**1**: ``Constituição - {}``\n**2**: ``Presição - {}``\n**3**: ``Agilidade - {}``\n'
                                '**4**: ``Ataque - {}``\n**5**: ``Sorte - '
                                '{}``'.format(data['rpg']['Status']['pdh'],
                                              data['rpg']['Status']['con'],
                                              data['rpg']['Status']['prec'],
                                              data['rpg']['Status']['agi'],
                                              data['rpg']['Status']['atk'],
                                              data['rpg']['Status']['luk']))
                resposta.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                resposta.set_thumbnail(url="{}".format(ctx.author.avatar_url))
                resposta.set_footer(text="Ashley ® Todos os direitos reservados.")
                await ctx.send(embed=resposta, delete_after=60.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @skill.command(name='add', aliases=['adicionar'])
    async def _add(self, ctx):
        """Comando usado pra distribuir seus status no rpg da Ashley
        Use ash skill add e siga as instruções do comando"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if ctx.author.id == data["user_id"]:
            resposta = discord.Embed(
                title='Escolha onde você quer adiconar seu ponto de habilidade:',
                color=self.color,
                description='ATUALMENTE VOCÊ TEM **{}** PONTOS DE HABILIDADE\n'
                            '``QUAL HABILIDADE VOCE DESEJA AUMENTAR?``\n'
                            '**1**: ``{}``\n**2**: ``{}``\n**3**: ``{}``\n'
                            '**4**: ``{}``\n**5**: ``{}``'.format(data['rpg']['Status']['pdh'], 'con',
                                                                  'prec', 'agi', 'atk', 'luk'))
            resposta.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
            resposta.set_thumbnail(url="{}".format(ctx.author.avatar_url))
            resposta.set_footer(text="Ashley ® Todos os direitos reservados.")
            await ctx.send(embed=resposta, delete_after=60.0)

            def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()

            try:
                option = await self.bot.wait_for('message', check=is_correct, timeout=30.0)
            except TimeoutError:
                return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito! Comando '
                                      'cancelado.``', delete_after=5.0)
            option = int(option.content)
            if update['rpg']['Status']['pdh'] > 0:
                if option == 1:
                    update['rpg']['Status']['con'] += 1
                    update['rpg']['Status']['pdh'] -= 1
                elif option == 2:
                    update['rpg']['Status']['prec'] += 1
                    update['rpg']['Status']['pdh'] -= 1
                elif option == 3:
                    update['rpg']['Status']['agi'] += 1
                    update['rpg']['Status']['pdh'] -= 1
                elif option == 4:
                    update['rpg']['Status']['atk'] += 1
                    update['rpg']['Status']['pdh'] -= 1
                elif option == 5:
                    update['rpg']['Status']['luk'] += 1
                    update['rpg']['Status']['pdh'] -= 1
                else:
                    return await ctx.send('<:negate:520418505993093130>│``Opção Invalida!``', delete_after=5.0)
                await self.bot.db.update_data(data, update, "users")
                await ctx.send('<:confirmado:519896822072999937>│``Ponto adicionado com sucesso!``', delete_after=5.0)
            else:
                await ctx.send('<:negate:520418505993093130>│``Você não tem pontos de habilidades disponiveis!``',
                               delete_after=5.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @skill.command(name='reset', aliases=['resetar'])
    async def _reset(self, ctx):
        """Comando usado pra resetar seus status
        Use ash skill reset"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if ctx.author.id == data["user_id"]:
            update['rpg']['Status']['con'] = 5
            update['rpg']['Status']['prec'] = 5
            update['rpg']['Status']['agi'] = 5
            update['rpg']['Status']['atk'] = 5
            update['rpg']['Status']['luk'] = 0
            update['rpg']['Status']['pdh'] = update['rpg']['Level'] - 1
            await self.bot.db.update_data(data, update, "users")
            await ctx.send('<:confirmado:519896822072999937>│``Status resetados com sucesso!``', delete_after=5.0)


def setup(bot):
    bot.add_cog(SkillClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mSKILLCLASS\033[1;32m foi carregado com sucesso!\33[m')
