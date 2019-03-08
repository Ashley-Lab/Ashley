from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class TransferClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='transfer', aliases=['trans'])
    async def transfer(self, ctx):
        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        data_guild_native = self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        data_guild_future = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_user = data_user
        update_guild_native = data_guild_native
        update_guild_future = data_guild_future

        a = '{:,.2f}'.format(float(data_user["treasure"]["money"]))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        d = c.replace('v', '.')

        def check(m):
            return m.author.id == ctx.guild.owner.id and m.channel.id == ctx.channel.id and m.content in ['S', 'N']

        await ctx.send(f'{ctx.guild.owner.mention} ``o membro`` {ctx.author.mention} ``quer associar sua conta da '
                       f'ashley na sua guilda.``\n ``Sua conta atual contem exatos`` **R${d} de Money** ``você deseja '
                       f'recebe-lo? Responsta com`` **[S/N]**', delete_after=60.0)

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=60.0)
        except TimeoutError:
            return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` '
                                  '**COMANDO CANCELADO**')

        if answer.content.upper() == "S":
            total = 1 * update_user['treasure']['bronze']
            total += 10 * update_user['treasure']['silver']
            total += 100 * update_user['treasure']['gold']
            update_guild_native['data']['total_money'] -= update_user['treasure'][total]
            update_guild_future['data']['total_money'] += update_user['treasure'][total]
            update_guild_native['data']['total_gold'] -= update_user['treasure']['gold']
            update_guild_future['data']['total_gold'] += update_user['treasure']['gold']
            update_guild_native['data']['total_silver'] -= update_user['treasure']['silver']
            update_guild_future['data']['total_silver'] += update_user['treasure']['silver']
            update_guild_native['data']['total_bronze'] -= update_user['treasure']['bronze']
            update_guild_future['data']['total_bronze'] += update_user['treasure']['bronze']
            update_user["guild_id"] = ctx.guild.id
            update_user["guild_name"] = ctx.guild.name
            update_user["guild_icon_url"] = ctx.guild.icon_url
            self.bot.db.update_data(data_user, update_user, 'users')
            self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            self.bot.db.update_data(data_guild_future, update_guild_future, 'guilds')
            await ctx.send(f'<:confirmado:519896822072999937>│🎊 **PARABENS** 🎉 {ctx.author.mention} ``Seu pedido foi'
                           f' aceito com sucesso, você agora faz parte da guilda`` **{ctx.guild.name}**')
        else:
            return await ctx.send('<:negate:520418505993093130>│``Desculpe, seu pedido de transferencia foi negado!``')


def setup(bot):
    bot.add_cog(TransferClass(bot))
    print('\033[1;32mO comando \033[1;34mTRANSFER_CLASS\033[1;32m foi carregado com sucesso!\33[m')
