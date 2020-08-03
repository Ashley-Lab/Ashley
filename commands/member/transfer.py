from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError


class TransferClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='transfer', aliases=['trans'])
    async def transfer(self, ctx):
        """comando usado pra transferir sua conta da ashley de um server pro outro
        Use ash transfer"""
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        data_guild_future = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_user = data_user
        update_guild_native = data_guild_native
        update_guild_future = data_guild_future
        a = '{:,.2f}'.format(float(update_user["treasure"]["money"]))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        if data_user['guild_id'] == ctx.guild.id:
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, você já está casdastrado nessa guilda!``')

        def check(m):
            if m.author.id == ctx.guild.owner.id:
                if m.channel.id == ctx.channel.id:
                    if m.content.upper() in ['S', 'N']:
                        return True
            return False

        await ctx.send(f'{ctx.guild.owner.mention} ``o membro`` {ctx.author.mention} ``quer associar sua conta do meu '
                       f'sistema na sua guilda.``\n ``A conta dele contem exatos`` **R${d} de Ethernyas** ``você deseja'
                       f' recebe-lo? Responda com`` **[S/N]**', delete_after=60.0)

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=30.0)
        except TimeoutError:
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` '
                                  '**COMANDO CANCELADO**')

        if answer.content.upper() == "S":
            update_guild_native['data']['total_money'] -= update_user['treasure']['money']
            update_guild_future['data']['total_money'] += update_user['treasure']['money']
            update_user["guild_id"] = ctx.guild.id
            await self.bot.db.update_data(data_user, update_user, 'users')
            await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            await self.bot.db.update_data(data_guild_future, update_guild_future, 'guilds')
            await ctx.send(f'<:confirmed:721581574461587496>│🎊 **PARABENS** 🎉 {ctx.author.mention} ``Seu pedido foi'
                           f' aceito com sucesso, você agora faz parte da guilda`` **{ctx.guild.name}**')
        else:
            await ctx.send('<:negate:721581573396496464>│``Desculpe, seu pedido de transferencia foi negado!``')


def setup(bot):
    bot.add_cog(TransferClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mTRANSFER_CLASS\033[1;32m foi carregado com sucesso!\33[m')
