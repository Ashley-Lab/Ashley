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

            if not data['rpg']['active']:
                embed = discord.Embed(
                    color=self.bot.color,
                    description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
                return await ctx.send(embed=embed)

            db = {
                "name": ctx.author.name,
                "avatar_member": ctx.author.avatar_url_as(format="png"),
                "vip": data['rpg']['vip'],
                "xp": data['rpg']['xp'],
                "level": str(data['rpg']['level']),
                "class": str(data['rpg']['next_class']),
                "atk": str(data['rpg']['status']['atk']),
                "dex": str(data['rpg']['status']['agi']),
                "acc": str(data['rpg']['status']['prec']),
                "con": str(data['rpg']['status']['con']),
                "luk": str(data['rpg']['status']['luk']),
                "pdh": str(data['rpg']['status']['pdh'])
            }

            await skill_points(db)
            await ctx.send("``--==ENTENDA O QUE OS ATRIBUTOS ALTERAM NO SEU PERSONAGEM==--``\n"
                           ">>> >>> `ATK` - **O ATK é somado ao seu dano de Skill e a chance de critical.**\n"
                           ">>> `DEX` - **O DEX aumenta sua chance de esquiva.**\n"
                           ">>> `ACC` - **O ACC aumenta sua chance de acerto da Skill.**\n"
                           ">>> `CON` - **O CON aumenta seu HP e sua MANA total.**\n"
                           ">>> `LUK` - **LUK aumenta a chance de efeito da Skill e o level da skill.**\n"
                           "```Markdown\n[>>]: PARA ADICIONAR PONTOS DE HABILIDADE USE O COMANDO\n<ASH SKILL ADD>\n"
                           "[>>]: PARA RESETAR OS PONTOS DE HABILIDADE USE O COMANDO\n<ASH SKILL RESET>```")
            if discord.File('skill_points.png') is None:
                return await ctx.send("<:negate:721581573396496464>│``ERRO!``")
            await ctx.send(file=discord.File('skill_points.png'), delete_after=60.0)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @skill.command(name='add', aliases=['adicionar'])
    async def _add(self, ctx, status=None, n=1):
        """Comando usado pra distribuir seus status no rpg da Ashley
        Use ash skill add e siga as instruções do comando"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if not data['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
            return await ctx.send(embed=embed)

        if update['config']['battle']:
            msg = '<:negate:721581573396496464>│``VOCE ESTÁ BATALHANDO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if status is None:
            return await ctx.send("<:negate:520418505993093130>│``Você precisa colocar o nome do atributo que deseja "
                                  "adicionar o ponto:`` **ash skill add con 1**")

        if status.lower() not in ['con', 'atk', 'acc', 'dex', 'luk']:
            return await ctx.send('<:negate:721581573396496464>│``Não existe esse atributo!``')

        if status.lower() == "acc":
            status = "prec"
        if status.lower() == "dex":
            status = "agi"

        if update['rpg']['status']['pdh'] < 0:
            return await ctx.send('<:negate:721581573396496464>│``Você não tem pontos de habilidades disponiveis!``')
        if update['rpg']['status']['pdh'] < n:
            return await ctx.send(f'<:negate:721581573396496464>│``Você não {n} pontos de habilidades disponiveis!``')

        if status.lower() == "con" and update['rpg']['status']['con'] + n > 40:
            msg = '<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 40 PONTOS NESSE ATRIBUTO``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if status.lower() == "prec" and update['rpg']['status']['prec'] + n > 20:
            msg = '<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 20 PONTOS NESSE ATRIBUTO``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if status.lower() == "agi" and update['rpg']['status']['agi'] + n > 20:
            msg = '<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 20 PONTOS NESSE ATRIBUTO``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if status.lower() == "atk" and update['rpg']['status']['atk'] + n > 40:
            msg = '<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 40 PONTOS NESSE ATRIBUTO``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if status.lower() == "luk" and update['rpg']['status']['luk'] + n > 20:
            msg = '<:negate:721581573396496464>│``VOCE NAO PODE PASSAR DE 20 PONTOS NESSE ATRIBUTO``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        update['rpg']['status'][status.lower()] += n
        update['rpg']['status']['pdh'] -= n
        await self.bot.db.update_data(data, update, "users")

        if status.lower() == "prec":
            status = "acc"
        if status.lower() == "agi":
            status = "dex"

        await ctx.send(f'<:confirmed:721581574461587496>│``Ponto de Habilidade adicionado com sucesso em:`` '
                       f'**{status.upper()}**')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @skill.command(name='reset', aliases=['resetar'])
    async def _reset(self, ctx):
        """Comando usado pra resetar seus status
        Use ash skill reset"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if not data['rpg']['active']:
            msg = '<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if update['config']['battle']:
            msg = '<:negate:721581573396496464>│``VOCE ESTÁ BATALHANDO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        update['rpg']['status']['con'] = 5
        update['rpg']['status']['prec'] = 5
        update['rpg']['status']['agi'] = 5
        update['rpg']['status']['atk'] = 5
        update['rpg']['status']['luk'] = 0
        update['rpg']['status']['pdh'] = update['rpg']['level']

        await self.bot.db.update_data(data, update, "users")
        await ctx.send('<:confirmed:721581574461587496>│``Status resetados com sucesso!``')


def setup(bot):
    bot.add_cog(SkillClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mSKILLCLASS\033[1;32m foi carregado com sucesso!\33[m')
