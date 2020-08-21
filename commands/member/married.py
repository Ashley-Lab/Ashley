import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError
from random import choice

git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class MarriedSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='marry', aliases=['casar', 'casamento'])
    async def marry(self, ctx, member: discord.Member = None):
        """Comando usado pra pedir alguem em casamento
        Use ash marry <@pessoa desejada>"""
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        if data_user['user']['married']:
            return await ctx.send('<:alert:739251822920728708>│``VOCE JÁ ESTA CASADO(A)!``')

        if data_user['user']['marrieding'] is True:
            return await ctx.send('<:alert:739251822920728708>│``VOCÊ JÁ ESTÁ EM PROCESSO DE CASAMENTO!``')

        if member is None:
            return await ctx.send('<:alert:739251822920728708>│``Você precisa mencionar alguem.``')

        if member.id == ctx.author.id:
            return await ctx.send('<:alert:739251822920728708>│``VOCE NÃO PODE CASAR CONSIGO MESMO!``')

        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_member = data_member

        if data_member is None:
            return await ctx.send('<:alert:739251822920728708>│**ATENÇÃO**: ``esse usuário não está cadastrado!`` '
                                  '**Você so pode se casar com membros cadastrados!**', delete_after=5.0)

        if data_member['user']['married'] is True:
            return await ctx.send('<:alert:739251822920728708>│``ELE(A) JÁ ESTA CASADO(A)!``')

        if data_member['user']['marrieding'] is True:
            return await ctx.send(f'<:alert:739251822920728708>│{member.mention} ``JÁ ESTÁ EM PROCESSO DE CASAMENTO!``')

        if data_user['user']['marrieding'] is False and data_member['user']['marrieding'] is False:
            update_user['user']['marrieding'] = True
            update_member['user']['marrieding'] = True
            await self.bot.db.update_data(data_user, update_user, 'users')
            await self.bot.db.update_data(data_member, update_member, 'users')

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        data_member = await self.bot.db.get_data("user_id", member.id, "users")
        update_member = data_member

        await ctx.send(f'<a:vergonha:525105074398167061>│{member.mention}, ``VOCÊ RECEBEU UM PEDIDO DE '
                       f'CASAMENTO DE`` {ctx.author.mention} ``DIGITE`` **SIM** ``OU`` **NÃO**')

        def check(m):
            return m.author.id == member.id and m.content.upper() in ['SIM', 'NÃO', 'S', 'N', 'NAO', 'CLARO']

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=30.0)
        except TimeoutError:
            update_user['user']['marrieding'] = False
            update_member['user']['marrieding'] = False
            await self.bot.db.update_data(data_user, update_user, 'users')
            await self.bot.db.update_data(data_member, update_member, 'users')
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, ele(a) demorou muito pra responder:`` '
                                  '**COMANDO CANCELADO**')

        if answer.content.upper() not in ['SIM', 'S', 'CLARO']:
            update_user['user']['marrieding'] = False
            update_member['user']['marrieding'] = False
            await self.bot.db.update_data(data_user, update_user, 'users')
            await self.bot.db.update_data(data_member, update_member, 'users')
            return await ctx.send(f'<:negate:721581573396496464>│{ctx.author.mention} ``VOCE FOI REJEITADO...``')

        update_user['user']['married'] = True
        update_user['user']['married_at'] = member.id
        update_user['user']['marrieding'] = False
        await self.bot.db.update_data(data_user, update_user, 'users')

        update_member['user']['married'] = True
        update_member['user']['married_at'] = ctx.author.id
        update_member['user']['marrieding'] = False
        await self.bot.db.update_data(data_member, update_member, 'users')

        embed = discord.Embed(color=self.color)
        embed.set_image(url=choice(git))
        await ctx.send(embed=embed)
        await ctx.send(f"🎊 **PARABENS** 🎉 {ctx.author.mention} **e** {member.mention} **vocês estão casados!**")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='divorce', aliases=['separar', 'separação', 'divorcio', 'separaçao', 'divorciar'])
    async def divorce(self, ctx):
        """Comando usado pra se divorciar
        Use ash divorce <@prostiranha em questão>"""

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        if not data_user['user']['married']:
            return await ctx.send('<:alert:739251822920728708>│``VOCE NÃO CASADO(A)!``')

        data_member = await self.bot.db.get_data("user_id", data_user['user']['married_at'], "users")
        update_member = data_member

        update_user['user']['married'] = False
        update_user['user']['married_at'] = None
        await self.bot.db.update_data(data_user, update_user, 'users')

        update_member['user']['married'] = False
        update_member['user']['married_at'] = None
        await self.bot.db.update_data(data_member, update_member, 'users')

        await ctx.send(f"😢 **QUE PENA** 😢 {ctx.author.mention} **e** {member.mention} **agora vocês estão SEPARADOS!**"
                       f" ``ESCOLHAM MELHOR DA PROXIMA VEZ!``")


def setup(bot):
    bot.add_cog(MarriedSystem(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMARRIED_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
