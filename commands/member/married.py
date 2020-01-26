import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError
from random import choice

git = ["https://media.giphy.com/media/2djU0ypmLqqsjHKEnM/giphy.gif",
       "https://media.giphy.com/media/69xjQSxBEeiJ2nfTZU/giphy.gif",
       "https://media.giphy.com/media/wZP7BxvpdCxxRWXtqf/giphy.gif",
       "https://media.giphy.com/media/1dMo2z3pippL3vzO6s/giphy.gif",
       "https://media.giphy.com/media/67SVlMevO3Zoo95d8P/giphy.gif"]


class MarriedSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='marry', aliases=['casar'])
    async def marry(self, ctx, member: discord.Member = None):
        if member is not None:
            data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
            data_member = self.bot.db.get_data("user_id", member.id, "users")
            update_user = data_user
            update_member = data_member
            if data_member is None:
                return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                      '``esse usuário não está cadastrado!`` **Você so pode se casar com membros '
                                      'cadastrados!**', delete_after=5.0)
            if member.id == ctx.author.id:
                return await ctx.send('<:negate:520418505993093130>│``VOCE NÃO PODE CASAR CONSIGO MESMO!``')

            try:
                if data_user['user']['marrieding'] is False and data_member['user']['marrieding'] is False:
                    update_user['user']['marrieding'] = True
                    update_member['user']['marrieding'] = True
                    self.bot.db.update_data(data_user, update_user, 'users')
                    self.bot.db.update_data(data_member, update_member, 'users')
                elif data_user['user']['marrieding'] is True:
                    return await ctx.send('<:negate:520418505993093130>│``VOCÊ JÁ ESTÁ EM PROCESSO DE CASAMENTO!``')
                elif data_member['user']['marrieding'] is True:
                    return await ctx.send('<:negate:520418505993093130>│{} `` JÁ ESTÁ EM PROCESSO DE '
                                          'CASAMENTO!``'.format(member.mention))
            except KeyError:
                update_user['user']['marrieding'] = True
                update_member['user']['marrieding'] = True
                self.bot.db.update_data(data_user, update_user, 'users')
                self.bot.db.update_data(data_member, update_member, 'users')

            data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
            data_member = self.bot.db.get_data("user_id", member.id, "users")
            update_user = data_user
            update_member = data_member

            if data_user['user']['married'] is False and data_member['user']['married'] is False:
                await ctx.send(f'<a:vergonha:525105074398167061>│{member.mention}, ``VOCÊ RECEBEU UM PEDIDO DE '
                               f'CASAMENTO DE`` {ctx.author.mention} ``DIGITE`` **SIM** ``OU`` **NÃO**')

                def check(m):
                    return m.author.id == member.id and m.content.upper() in ['SIM', 'NÃO', 'S', 'N', 'NAO', 'CLARO']

                try:
                    answer = await self.bot.wait_for('message', check=check, timeout=60.0)
                except TimeoutError:
                    update_user['user']['marrieding'] = False
                    update_member['user']['marrieding'] = False
                    self.bot.db.update_data(data_user, update_user, 'users')
                    self.bot.db.update_data(data_member, update_member, 'users')
                    return await ctx.send('<:negate:520418505993093130>│``Desculpe, ele(a) demorou muito pra responder:'
                                          '`` **COMANDO CANCELADO**')

                if answer.content.upper() not in ['SIM', 'S', 'CLARO']:
                    update_user['user']['marrieding'] = False
                    update_member['user']['marrieding'] = False
                    self.bot.db.update_data(data_user, update_user, 'users')
                    self.bot.db.update_data(data_member, update_member, 'users')
                    return await ctx.send(f'<:oc_status:519896814225457152>│{ctx.author.mention} ``VOCE FOI '
                                          f'REJEITADO...``')
                else:
                    update_user['user']['married'] = True
                    update_member['user']['married'] = True
                    update_user['user']['married_at'] = member.id
                    update_member['user']['married_at'] = ctx.author.id
                    update_user['user']['marrieding'] = False
                    update_member['user']['marrieding'] = False
                    self.bot.db.update_data(data_user, update_user, 'users')
                    self.bot.db.update_data(data_member, update_member, 'users')
                    img = choice(git)
                    embed = discord.Embed(color=self.color)
                    embed.set_image(url=img)
                    await ctx.send(embed=embed)
                    return await ctx.send(
                        f"🎊 **PARABENS** 🎉 {ctx.author.mention} **e** {member.mention} **agora vocês"
                        f" estão casados!**")

            elif data_member['user']['married'] is True:
                update_user['user']['marrieding'] = False
                update_member['user']['marrieding'] = False
                self.bot.db.update_data(data_user, update_user, 'users')
                self.bot.db.update_data(data_member, update_member, 'users')
                return await ctx.send('<:negate:520418505993093130>│``ELE(A) JÁ ESTA CASADO(A)!``')
            else:
                update_user['user']['marrieding'] = False
                update_member['user']['marrieding'] = False
                self.bot.db.update_data(data_user, update_user, 'users')
                self.bot.db.update_data(data_member, update_member, 'users')
                return await ctx.send('<:negate:520418505993093130>│``VOCE JÁ ESTA CASADO(A)!``')
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você precisa mensionar alguem.``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='divorce', aliases=['separar'])
    async def divorce(self, ctx, member: discord.Member = None):
        if member is not None:
            data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
            data_member = self.bot.db.get_data("user_id", member.id, "users")
        else:
            data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
            data_member = self.bot.db.get_data("user_id", data_user['user']['married_at'], "users")

        update_user = data_user
        update_member = data_member

        if data_member is None:
            return await ctx.send('<:alert_status:519896811192844288>│**ATENÇÃO** : '
                                  '``esse usuário não está cadastrado!``', delete_after=5.0)
        if member is not None:
            if member.id == ctx.author.id:
                return await ctx.send('<:negate:520418505993093130>│``VOCE NÃO PODE SE SEPARAR DE VOCÊ MESMO!``')
        else:
            pass

        if data_user['user']['married'] is True and data_member['user']['married'] is True:
            if member is not None:
                if data_user['user']['married_at'] == member.id and data_member['user']['married_at'] == ctx.author.id:
                    update_user['user']['married'] = False
                    update_member['user']['married'] = False
                    update_user['user']['married_at'] = None
                    update_member['user']['married_at'] = None
                    self.bot.db.update_data(data_user, update_user, 'users')
                    self.bot.db.update_data(data_member, update_member, 'users')
                    return await ctx.send(
                        f"😢 **QUE PENA** 😢 {ctx.author.mention} **e** {member.mention} **agora vocês"
                        f" estão SEPARADOS!** ``ESCOLHA MELHOR DA PROXIMA VEZ!``")
                else:
                    await ctx.send("<:negate:520418505993093130>│``VOCÊ NÃO ESTÁ CASADO COM ESSA PESSOA!``")
            else:
                update_user['user']['married'] = False
                update_member['user']['married'] = False
                update_user['user']['married_at'] = None
                update_member['user']['married_at'] = None
                self.bot.db.update_data(data_user, update_user, 'users')
                self.bot.db.update_data(data_member, update_member, 'users')
                return await ctx.send(
                    f"😢 **QUE PENA** 😢 {ctx.author.mention} **agora você"
                    f" está SEPARADO(A)!** ``ESCOLHA MELHOR DA PROXIMA VEZ!``")
        elif data_member['user']['married'] is False:
            return await ctx.send('<:negate:520418505993093130>│``ELE(A) NÃO ESTA CASADO(A)!``')
        else:
            return await ctx.send('<:negate:520418505993093130>│``VOCE NÃO ESTA CASADO(A)!``')


def setup(bot):
    bot.add_cog(MarriedSystem(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mMARRIED_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
