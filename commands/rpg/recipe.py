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

                for c in recipe['custo']:
                    name = c.keys()[0]
                    quantidade = c[name]
                    description += '\n{}X{}'.format(name, quantidade)

                description += '\n\nResultado:'

                for c in recipe['recompeça']:
                    name = c.keys()[0]
                    quantidade = c[name]
                    description += '\n{}X{}'.format(name, quantidade)

                for c in recipe['custo']:
                    tempmax = data['inventory'][c.keys()[0]] // c[c.keys()[0]]
                    if maximo is None or maximo > tempmax:
                        maximo = tempmax

                description += '\nMaximo que você pode craftar{}' \
                               '\n▶:craftar 1\n⏩:craftar alguns' \
                               '\n⏭:craftar o maximo\n❌:fechar'.format(maximo)

                embed = discord.Embed(
                    title='Recipe',
                    color=0x564128,
                    description=description)

                msg = ctx.send(embed=embed)
                emojis = ['▶', '⏩', '⏭', '❌']

                for c in emojis:
                    await msg.add_reaction(c)

                reaction = await self.bot.wait_for('reaction_add')
                while reaction[1].id != ctx.author or reaction[0].emoji not in emojis:
                    reaction = await self.bot.wait_for('reaction_add')

                if reaction[0].emoji == '▶':
                    for c in recipe['custo']:
                        name = c.keys()[0]
                        quantidade = c[name]
                        data['inventory'][c.keys()[0]] -= quantidade

                    for c in recipe['recompensa']:
                        name = c.keys()[0]
                        quantidade = c[name]
                        try:
                            data['inventory'][c.keys()[0]] += quantidade
                        except KeyError:
                            data['inventory'][c.keys()[0]] = quantidade

                elif reaction[0].emoji == '⏩':
                    await ctx.send('Quantas receitas você quer fazer?')
                    resp = await self.bot.wait_for('message', check=check)

                    while True:
                        try:
                            resp = int(resp.content)
                            if resp <= maximo:
                                break
                        except TypeError:
                            pass
                        await ctx.send('Valor invalido tente denovo.')
                        resp = await self.bot.wait_for('message')

                    resp = int(resp)

                    for c in recipe['custo']:
                        name = c.keys()[0]
                        quantidade = c[name] * resp
                        data['inventory'][c.keys()[0]] -= quantidade

                    for c in recipe['recompensa']:
                        name = c.keys()[0]
                        quantidade = c[name] * resp
                        try:
                            data['inventory'][c.keys()[0]] += quantidade
                        except KeyError:
                            data['inventory'][c.keys()[0]] = quantidade

                elif reaction[0].emoji == '⏭':
                    for c in recipe['custo']:
                        name = c.keys()[0]
                        quantidade = c[name] * maximo
                        data['inventory'][c.keys()[0]] -= quantidade

                    for c in recipe['recompensa']:
                        name = c.keys()[0]
                        quantidade = c[name] * maximo
                        try:
                            data['inventory'][c.keys()[0]] += quantidade
                        except KeyError:
                            data['inventory'][c.keys()[0]] = quantidade

                await msg.delete()
                print(str(data))
            else:
                ctx.send('item não existe')
        else:
            embed = ['Recipes/Craft', self.color, 'Lista dos Recipes: \n']
            await paginator(self.bot, recipes, {}, embed, ctx)


def setup(bot):
    bot.add_cog(DoorClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDOOR_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
