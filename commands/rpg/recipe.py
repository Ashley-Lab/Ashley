import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import paginator
from asyncio import TimeoutError

resp = 0


class RecipeClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='craft', aliases=['construir'])
    async def craft(self, ctx, *, item=None):
        """Esse nem eu sei..."""
        global resp
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        recipes = self.bot.config['recipes']
        update = data

        if item is not None:

            item = item.lower()

            def check(m):
                return m.author.id == ctx.author.id and m.content.isdigit()

            if item in recipes.keys():

                recipe = recipes[item]
                description = '**Custo:**'
                maximo = None

                for c in recipe['cost']:
                    try:
                        quant = data['inventory'][c[0]]
                    except KeyError:
                        quant = 0
                    description += f'\n{self.bot.items[c[0]][0]} ``{c[0]}:`` **{c[1]}**/{quant}'

                description += '\n\n**Recompensa:**'

                for c in recipe['reward']:
                    try:
                        quant = data['inventory'][c[0]]
                    except KeyError:
                        quant = 0
                    description += f'\n{self.bot.items[c[0]][0]} ``{c[0]}:`` **{c[1]}**/{quant}'

                for c in recipe['cost']:
                    try:
                        tempmax = update['inventory'][c[0]] // c[1]
                    except KeyError:
                        tempmax = 0
                        await ctx.send(f'<:negate:520418505993093130>|``Você não tem o item`` **{c[0]}**')
                    if maximo is None or maximo > tempmax:
                        maximo = tempmax

                description += '\n\n**Maximo que você pode craftar:** ``{}``' \
                               '\n▶ **Craftar** ``1``\n⏩ **Craftar** ``2+``' \
                               '\n⏭ **Craftar o Maximo**\n❌ **Fechar**'.format(maximo)

                embed = discord.Embed(
                    title='Craft\n(Custo/Quantidade no inventario)',
                    color=self.bot.color,
                    description=description)

                msg = await ctx.send(embed=embed)
                emojis = ['▶', '⏩', '⏭', '❌']

                for c in emojis:
                    await msg.add_reaction(c)

                try:
                    reaction = await self.bot.wait_for('reaction_add', timeout=30.0)
                    while reaction[1].id != ctx.author.id or reaction[0].emoji not in emojis:
                        reaction = await self.bot.wait_for('reaction_add', timeout=30.0)
                except TimeoutError:
                    return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito! Comando '
                                          'cancelado.``', delete_after=5.0)

                if reaction[0].emoji == '▶':
                    try:
                        for c in recipe['cost']:
                            if update['inventory'][c[0]] >= c[1]:
                                update['inventory'][c[0]] -= c[1]
                            else:
                                return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                                      'necessarios.``')
                    except KeyError:
                        return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                              'necessarios.``')

                    for c in recipe['reward']:
                        try:
                            update['inventory'][c[0]] += c[1]
                        except KeyError:
                            update['inventory'][c[0]] = c[1]

                elif reaction[0].emoji == '⏩':
                    await ctx.send('<:alert_status:519896811192844288>│``Quantas receitas você quer fazer?``')
                    try:
                        resp = await self.bot.wait_for('message', check=check, timeout=30.0)
                    except TimeoutError:
                        return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                              ' CANCELADO**')

                    while True:
                        if int(resp.content) <= maximo:
                            break
                        try:
                            resp = await self.bot.wait_for('message', check=check, timeout=30.0)
                        except TimeoutError:
                            return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` '
                                                  '**COMANDO CANCELADO**')

                    try:
                        resp = int(resp.content)
                    except AttributeError:
                        pass

                    if resp < 1:
                        return await ctx.send('<:negate:520418505993093130>|``Voce nao pode craftar 0 item...``')

                    try:
                        for _ in range(resp):
                            for c in recipe['cost']:
                                if update['inventory'][c[0]] >= c[1]:
                                    update['inventory'][c[0]] -= c[1]
                                else:
                                    return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                                          'necessarios.``')
                    except KeyError:
                        return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                              'necessarios.``')

                    for c in recipe['reward']:
                        try:
                            update['inventory'][c[0]] += c[1] * resp
                        except KeyError:
                            update['inventory'][c[0]] = c[1] * resp

                elif reaction[0].emoji == '⏭':
                    if maximo < 1:
                        return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                              'necessarios.``')

                    try:
                        for _ in range(maximo):
                            for c in recipe['cost']:
                                if update['inventory'][c[0]] >= c[1]:
                                    update['inventory'][c[0]] -= c[1]
                                else:
                                    return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                                          'necessarios.``')
                    except KeyError:
                        return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                              'necessarios.``')

                    for c in recipe['reward']:
                        try:
                            update['inventory'][c[0]] += c[1] * maximo
                        except KeyError:
                            update['inventory'][c[0]] = c[1] * maximo

                if reaction[0].emoji == "❌":
                    await msg.delete()
                    return

                await msg.delete()
                await self.bot.db.update_data(data, update, 'users')
                await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``O ITEM`` ✨ **{item.upper()}** ✨ "
                               f"``FOI CRAFTADO FEITO COM SUCESSO!``")
            else:
                await ctx.send('<:negate:520418505993093130>|``Esse item não existe ou nao é craftavel.``')
        else:
            await ctx.send('<:negate:520418505993093130>|``DIGITE UM NOME DE UM ITEM. CASO NAO SAIBA USE O COMANDO:``'
                           ' **ASH RECIPE** ``PARA VER A LISTA DE ITENS CRAFTAVEIS!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='recipe', aliases=['receita'])
    async def recipe(self, ctx):
        """Esse nem eu sei..."""
        recipes = self.bot.config['recipes']
        embed = ['Recipes', self.color, '``Para craftar um item use:`` **ash craft nome_do_item**\n\n']
        await paginator(self.bot, self.bot.items, recipes, embed, ctx)


def setup(bot):
    bot.add_cog(RecipeClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mRECIPE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
