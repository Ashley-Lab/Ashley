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
        self.i = self.bot.items

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='craft', aliases=['construir'])
    async def craft(self, ctx, *, item=None):
        """Esse nem eu sei..."""
        global resp
        recipes = self.bot.config['recipes']

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['config']['buying']:
            return await ctx.send('<:alert:739251822920728708>│``VOCE JA ESTA EM PROCESSO DE COMPRA...``')

        update['config']['buying'] = True
        await self.bot.db.update_data(data, update, 'users')

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
                    description += f'\n{self.i[c[0]][0]} **{c[1]}**/``{quant}`` ``{self.i[c[0]][1]}``'

                description += '\n\n**Recompensa:**'

                for c in recipe['reward']:
                    try:
                        quant = data['inventory'][c[0]]
                    except KeyError:
                        quant = 0
                    description += f'\n{self.i[c[0]][0]} **{c[1]}**/``{quant}`` ``{self.i[c[0]][1]}``'

                for c in recipe['cost']:
                    try:
                        tempmax = update['inventory'][c[0]] // c[1]
                    except KeyError:
                        tempmax = 0
                        await ctx.send(f'<:alert:739251822920728708>|``Você não tem o item`` **{c[0]}**')
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
                    reaction = await self.bot.wait_for('reaction_add', timeout=60.0)
                    while reaction[1].id != ctx.author.id or reaction[0].emoji not in emojis:
                        reaction = await self.bot.wait_for('reaction_add', timeout=60.0)
                except TimeoutError:
                    data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                    update = data
                    update['config']['buying'] = False
                    await self.bot.db.update_data(data, update, 'users')
                    return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito! Comando '
                                          'cancelado.``', delete_after=5.0)

                if reaction[0].emoji == '▶':
                    try:
                        for c in recipe['cost']:
                            if update['inventory'][c[0]] >= c[1]:
                                update['inventory'][c[0]] -= c[1]
                                if update['inventory'][c[0]] < 1:
                                    del update['inventory'][c[0]]
                            else:
                                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                                update = data
                                update['config']['buying'] = False
                                await self.bot.db.update_data(data, update, 'users')
                                return await ctx.send('<:alert:739251822920728708>|``Você não tem todos os itens '
                                                      'necessarios.``')
                    except KeyError:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['buying'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:alert:739251822920728708>|``Você não tem todos os itens '
                                              'necessarios.``')

                    for c in recipe['reward']:
                        try:
                            update['inventory'][c[0]] += c[1]
                        except KeyError:
                            update['inventory'][c[0]] = c[1]

                elif reaction[0].emoji == '⏩':
                    await ctx.send('<:alert:739251822920728708>│``Quantas receitas você quer fazer?``')
                    try:
                        resp = await self.bot.wait_for('message', check=check, timeout=60.0)
                    except TimeoutError:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['buying'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` **COMANDO'
                                              ' CANCELADO**')

                    while not self.bot.is_closed():
                        if int(resp.content) <= maximo:
                            break
                        try:
                            resp = await self.bot.wait_for('message', check=check, timeout=60.0)
                        except TimeoutError:
                            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                            update = data
                            update['config']['buying'] = False
                            await self.bot.db.update_data(data, update, 'users')
                            return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` '
                                                  '**COMANDO CANCELADO**')

                    try:
                        resp = int(resp.content)
                    except AttributeError:
                        pass

                    if resp < 1:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['buying'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:alert:739251822920728708>|``Voce nao pode craftar 0 item...``')

                    try:
                        for _ in range(resp):
                            for c in recipe['cost']:
                                if update['inventory'][c[0]] >= c[1]:
                                    update['inventory'][c[0]] -= c[1]
                                    if update['inventory'][c[0]] < 1:
                                        del update['inventory'][c[0]]
                                else:
                                    data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                                    update = data
                                    update['config']['buying'] = False
                                    await self.bot.db.update_data(data, update, 'users')
                                    return await ctx.send('<:alert:739251822920728708>|``Você não tem todos os itens '
                                                          'necessarios.``')
                    except KeyError:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['buying'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:alert:739251822920728708>|``Você não tem todos os itens '
                                              'necessarios.``')

                    for c in recipe['reward']:
                        try:
                            update['inventory'][c[0]] += c[1] * resp
                        except KeyError:
                            update['inventory'][c[0]] = c[1] * resp

                elif reaction[0].emoji == '⏭':
                    if maximo < 1:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['buying'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:alert:739251822920728708>|``Você não tem todos os itens '
                                              'necessarios.``')

                    try:
                        for _ in range(maximo):
                            for c in recipe['cost']:
                                if update['inventory'][c[0]] >= c[1]:
                                    update['inventory'][c[0]] -= c[1]
                                    if update['inventory'][c[0]] < 1:
                                        del update['inventory'][c[0]]
                                else:
                                    data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                                    update = data
                                    update['config']['buying'] = False
                                    await self.bot.db.update_data(data, update, 'users')
                                    return await ctx.send('<:alert:739251822920728708>|``Você não tem todos os itens '
                                                          'necessarios.``')
                    except KeyError:
                        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                        update = data
                        update['config']['buying'] = False
                        await self.bot.db.update_data(data, update, 'users')
                        return await ctx.send('<:alert:739251822920728708>|``Você não tem todos os itens '
                                              'necessarios.``')

                    for c in recipe['reward']:
                        try:
                            update['inventory'][c[0]] += c[1] * maximo
                        except KeyError:
                            update['inventory'][c[0]] = c[1] * maximo

                if reaction[0].emoji == "❌":
                    await msg.delete()
                    data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                    update = data
                    update['config']['buying'] = False
                    await self.bot.db.update_data(data, update, 'users')
                    return

                quantidade = 1
                if reaction[0].emoji == '⏩':
                    quantidade = resp
                if reaction[0].emoji == '⏭':
                    quantidade = maximo

                await msg.delete()
                await self.bot.db.update_data(data, update, 'users')
                await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``O ITEM`` ✨ **{item.upper()}** ✨ "
                               f"``FOI CRAFTADO`` **{quantidade}X** ``COM SUCESSO!``")
            else:
                await ctx.send('<:negate:721581573396496464>|``Esse item não existe ou nao é craftavel.``')
        else:
            await ctx.send('<:negate:721581573396496464>|``DIGITE UM NOME DE UM ITEM. CASO NAO SAIBA USE O COMANDO:``'
                           ' **ASH RECIPE** ``PARA VER A LISTA DE ITENS CRAFTAVEIS!``')
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        update['config']['buying'] = False
        await self.bot.db.update_data(data, update, 'users')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='recipe', aliases=['receita'])
    async def recipe(self, ctx):
        """Esse nem eu sei..."""
        recipes = self.bot.config['recipes']
        embed = ['Recipes', self.color, '``Para craftar um item use:``\n**ash craft nome_do_item**\n\n']
        await paginator(self.bot, self.bot.items, recipes, embed, ctx)


def setup(bot):
    bot.add_cog(RecipeClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mRECIPE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
