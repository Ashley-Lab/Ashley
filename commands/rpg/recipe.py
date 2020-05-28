import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from resources.utility import paginator


class DoorClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(name='recipe', aliases=['craft'])
    async def recipe(self, ctx, *, item=None):
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        recipes = self.bot.config['recipes']

        if item is not None:

            def check(m):
                return m.author.id == ctx.author.id

            if item in recipes.keys():

                recipe = recipes[item]
                description = 'Materiais:'
                maximo = None

                for c in recipe['cost']:
                    description += f'\n{c[0]}X{c[1]}'

                description += '\n\nResultado:'

                for c in recipe['reward']:
                    description += f'\n{c[0]}X{c[1]}'

                try:
                    for c in recipe['cost']:
                        tempmax = data['inventory'][c[0]] // c[1]
                        if maximo is None or maximo > tempmax:
                            maximo = tempmax
                except KeyError:
                    return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens necessarios.``')

                description += '\nMaximo que você pode craftar{}' \
                               '\n▶:craftar 1\n⏩:craftar alguns' \
                               '\n⏭:craftar o maximo\n❌:fechar'.format(maximo)

                embed = discord.Embed(
                    title='Recipe',
                    color=self.bot.color,
                    description=description)

                msg = await ctx.send(embed=embed)
                emojis = ['▶', '⏩', '⏭', '❌']

                for c in emojis:
                    await msg.add_reaction(c)

                reaction = await self.bot.wait_for('reaction_add')
                while reaction[1].id != ctx.author or reaction[0].emoji not in emojis:
                    reaction = await self.bot.wait_for('reaction_add')

                if reaction[0].emoji == '▶':
                    try:
                        for c in recipe['cost']:
                            data['inventory'][c[0]] -= c[1]
                    except KeyError:
                        return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                              'necessarios.``')

                    for c in recipe['reward']:
                        try:
                            data['inventory'][c[0]] += c[1]
                        except KeyError:
                            data['inventory'][c[0]] = c[1]

                elif reaction[0].emoji == '⏩':
                    await ctx.send('<:alert_status:519896811192844288>│``Quantas receitas você quer fazer?``')
                    resp = await self.bot.wait_for('message', check=check)

                    while True:
                        try:
                            resp = int(resp.content)
                            if resp <= maximo:
                                break
                        except TypeError:
                            pass
                        await ctx.send('<:negate:520418505993093130>|``Valor invalido tente denovo.``')
                        resp = await self.bot.wait_for('message')

                    resp = int(resp)

                    try:
                        for c in recipe['cost']:
                            data['inventory'][c[0]] -= c[1]
                    except KeyError:
                        return await ctx.send('<:negate:520418505993093130>|``Você não tem todos os itens '
                                              'necessarios.``')

                    for c in recipe['reward']:
                        try:
                            data['inventory'][c[0]] += c[1] * resp
                        except KeyError:
                            data['inventory'][c[0]] = c[1] * resp

                elif reaction[0].emoji == '⏭':
                    for c in recipe['cost']:
                        data['inventory'][c[0]] -= c[1] * maximo

                    for c in recipe['reward']:
                        try:
                            data['inventory'][c[0]] += c[1] * maximo
                        except KeyError:
                            data['inventory'][c[0]] = c[1] * maximo

                await msg.delete()
                print(str(data))
                await ctx.send("<:confirmado:519896822072999937>│``CRAFT FEITO COM SUCESSO!``")
            else:
                await ctx.send('<:negate:520418505993093130>|``Esse item não existe.``')
        else:
            embed = ['Recipes/Craft', self.color, '``Para craftar um item use:`` **ash craft <nome_do_item>**\n\n']
            await paginator(self.bot, recipes, recipes, embed, ctx)


def setup(bot):
    bot.add_cog(DoorClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDOOR_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
