import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.img_edit import skill_points


class SkillClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='skill', aliases=['habilidade'])
    async def skill(self, ctx):
        """Comando usado pra ver seus status no rpg da Ashley
        Use ash skill"""
        if ctx.invoked_subcommand is None:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")

            if not data['rpg']['status']:
                embed = discord.Embed(
                    color=self.bot.color,
                    description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
                return await ctx.send(embed=embed)

            db = {
                "name": ctx.author.name,
                "avatar_member": ctx.author.avatar_url_as(format="png"),
                "vip": data['rpg']['vip'],
                "xp": data['rpg']['XP'],
                "level": str(data['rpg']['Level']),
                "class": str(data['rpg']['next_class']),
                "atk": str(data['rpg']['Status']['atk']),
                "dex": str(data['rpg']['Status']['agi']),
                "acc": str(data['rpg']['Status']['prec']),
                "con": str(data['rpg']['Status']['con']),
                "luk": str(data['rpg']['Status']['luk']),
                "pdh": str(data['rpg']['Status']['pdh'])
            }

            await skill_points(db)
            await ctx.send("> ``CLIQUE NA IMAGEM PARA MAIORES DETALHES``")
            if discord.File('skill_points.png') is None:
                return await ctx.send("<:negate:721581573396496464>│``ERRO!``")
            await ctx.send(file=discord.File('skill_points.png'))
            await ctx.send("> ``PARA ADICIONAR PONTOS DE HABILIDADE USE O COMANDO`` **ASH SKILL ADD**\n"
                           "> ``PARA RESETAR OS PONTOS DE HABILIDADE USE O COMANDO`` **ASH SKILL RESET**")

    @check_it(no_pm=True)
    @commands.cooldown(1, 0.5, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @skill.command(name='add', aliases=['adicionar'])
    async def _add(self, ctx, status=None):
        """Comando usado pra distribuir seus status no rpg da Ashley
        Use ash skill add e siga as instruções do comando"""
        if status is None:
            return await ctx.send("<:negate:520418505993093130>│``Você precisa colocar o nome do atributo que deseja "
                                  "adicionar o ponto:`` **ash skill add con**")

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if update['config']['battle']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE ESTÁ BATALHANDO!``')
            return await ctx.send(embed=embed)

        if update['rpg']['Status']['pdh'] > 0:
            if status.lower() == "con":
                if update['rpg']['Status']['con'] == 40:
                    embed = discord.Embed(
                        color=self.bot.color,
                        description='<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 40 PONTOS NESSE ATRIBUTO``')
                    return await ctx.send(embed=embed)
                update['rpg']['Status']['con'] += 1
                update['rpg']['Status']['pdh'] -= 1
            elif status.lower() == "acc":
                if update['rpg']['Status']['prec'] == 20:
                    embed = discord.Embed(
                        color=self.bot.color,
                        description='<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 20 PONTOS NESSE ATRIBUTO``')
                    return await ctx.send(embed=embed)
                update['rpg']['Status']['prec'] += 1
                update['rpg']['Status']['pdh'] -= 1
            elif status.lower() == "dex":
                if update['rpg']['Status']['agi'] == 20:
                    embed = discord.Embed(
                        color=self.bot.color,
                        description='<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 20 PONTOS NESSE ATRIBUTO``')
                    return await ctx.send(embed=embed)
                update['rpg']['Status']['agi'] += 1
                update['rpg']['Status']['pdh'] -= 1
            elif status.lower() == "atk":
                if update['rpg']['Status']['atk'] == 40:
                    embed = discord.Embed(
                        color=self.bot.color,
                        description='<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 40 PONTOS NESSE ATRIBUTO``')
                    return await ctx.send(embed=embed)
                update['rpg']['Status']['atk'] += 1
                update['rpg']['Status']['pdh'] -= 1
            elif status.lower() == "luk":
                if update['rpg']['Status']['luk'] == 20:
                    embed = discord.Embed(
                        color=self.bot.color,
                        description='<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 20 PONTOS NESSE ATRIBUTO``')
                    return await ctx.send(embed=embed)
                update['rpg']['Status']['luk'] += 1
                update['rpg']['Status']['pdh'] -= 1
            else:
                return await ctx.send('<:negate:721581573396496464>│``Não existe esse atributo!``')
            await self.bot.db.update_data(data, update, "users")
            await ctx.send(f'<:confirmed:721581574461587496>│``Ponto de Habilidade adicionado com sucesso em:`` '
                           f'**{status.upper()}**')
        else:
            await ctx.send('<:negate:721581573396496464>│``Você não tem pontos de habilidades disponiveis!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @skill.command(name='reset', aliases=['resetar'])
    async def _reset(self, ctx):
        """Comando usado pra resetar seus status
        Use ash skill reset"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if update['config']['battle']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE ESTÁ BATALHANDO!``')
            return await ctx.send(embed=embed)

        update['rpg']['Status']['con'] = 5
        update['rpg']['Status']['prec'] = 5
        update['rpg']['Status']['agi'] = 5
        update['rpg']['Status']['atk'] = 5
        update['rpg']['Status']['luk'] = 0
        update['rpg']['Status']['pdh'] = update['rpg']['Level']

        await self.bot.db.update_data(data, update, "users")
        await ctx.send('<:confirmed:721581574461587496>│``Status resetados com sucesso!``')


def setup(bot):
    bot.add_cog(SkillClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mSKILLCLASS\033[1;32m foi carregado com sucesso!\33[m')
