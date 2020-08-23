from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import paginator


class InventoryClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.i = self.bot.items
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='inventory', aliases=['inventario', 'i'])
    async def inventory(self, ctx):
        """Comando usado pra ver seu inventario
        Use ash i ou ash inventory"""
        if ctx.invoked_subcommand is None:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            embed = ['Inventário:', self.color, 'Items: \n']
            await paginator(self.bot, self.i, data['inventory'], embed, ctx)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @inventory.command(name='equip', aliases=['equipamento', 'e'])
    async def _equip(self, ctx):
        """Comando usado pra ver seu inventario de equipamentos
                Use ash i ou ash inventory"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")

        if len(data['rpg']['items'].keys()) == 0:
            return await ctx.send(f"<:negate:721581573396496464>|``SEU INVENTARIO DE EQUIPAMENTOS ESTÁ VAZIO!``")

        embed = ['Inventário:', self.color, 'Equipamentos: \n']

        eq = dict()
        for ky in self.bot.config['equips'].keys():
            for k, v in self.bot.config['equips'][ky].items():
                eq[k] = v

        await paginator(self.bot, eq, data['rpg']['items'], embed, ctx)


def setup(bot):
    bot.add_cog(InventoryClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mINVENTORYCLASS\033[1;32m foi carregado com sucesso!\33[m')
