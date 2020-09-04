import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError, sleep

legend = {
    "Comum": [600, [0.01, 0.02, 0.07, 0.10, 0.20, 0.60]],
    "Incomum": [500, [0.02, 0.04, 0.10, 0.24, 0.50, 0.10]],
    "Raro": [400, [0.03, 0.07, 0.10, 0.50, 0.20, 0.10]],
    "Super Raro": [300, [0.04, 0.6, 0.30, 0.20, 0.20, 0.20]],
    "Ultra Raro": [200, [0.05, 0.35, 0.15, 0.15, 0.15, 0.15]],
    "Secret": [100, [0.25, 0.20, 0.25, 0.15, 0.10, 0.05]]
}


class BoxClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @staticmethod
    def verify_money(money, num, price):
        cont = 0
        for _ in range(num):
            if money > price:
                cont += 1
                money -= 500
            else:
                pass
        return cont

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='box', aliases=['caixa'])
    async def box(self, ctx):
        """Comando usado pra comprar e abrir booster boxes
                Use ash box e siga as instruções"""
        if ctx.invoked_subcommand is None:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            if data['config']['buying']:
                return await ctx.send('<:alert:739251822920728708>│``VOCE JA ESTA EM PROCESSO DE COMPRA...``')

            if data['box']['status']['active']:
                status = data['box']['status']['active']
                rarity = data['box']['status']['rarity']

                s = data['box']['status']['secret']
                ur = data['box']['status']['ur']
                sr = data['box']['status']['sr']
                r = data['box']['status']['r']
                i = data['box']['status']['i']
                c = data['box']['status']['c']

                size_full = legend[rarity][0]
                size_now = data['box']['status']['size']

                l_s = int(size_full * legend[rarity][1][0])
                l_ur = int(size_full * legend[rarity][1][1])
                l_sr = int(size_full * legend[rarity][1][2])
                l_r = int(size_full * legend[rarity][1][3])
                l_i = int(size_full * legend[rarity][1][4])
                l_c = int(size_full * legend[rarity][1][5])

                images = {'Secret': 'https://i.imgur.com/qjenk0j.png',
                          'Ultra Raro': 'https://i.imgur.com/fdudP2k.png',
                          'Super Raro': 'https://i.imgur.com/WYebgvF.png',
                          'Raro': 'https://i.imgur.com/7LnlnDA.png',
                          'Incomum': 'https://i.imgur.com/TnoC2j1.png',
                          'Comum': 'https://i.imgur.com/ma5tHvK.png'}

                description = '''
Raridade da Box:
**{}**
```Markdown
STATUS:
<ACTIVE: {}>

ITEMS:
<SECRET: {}/{}>
<UR: {}/{}>
<SR: {}/{}>
<R: {}/{}>
<I: {}/{}>
<C: {}/{}>
<SIZE: {}/{}>```'''.format(rarity, status, s, l_s, ur, l_ur, sr, l_sr, r, l_r, i, l_i, c, l_c, size_now, size_full)
                box = discord.Embed(
                    title="{}'s box:\n"
                          "``PARA ABRIR SUA BOX USE O COMANDO``\n"
                          "**ASH BOX BOOSTER**".format(ctx.author.name),
                    color=self.color,
                    description=description
                )
                box.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                box.set_thumbnail(url="{}".format(images[rarity]))
                box.set_footer(text="Ashley ® Todos os direitos reservados.")
                await ctx.send(embed=box)
            else:
                await ctx.send("<:alert:739251822920728708>│``Você não tem uma box ativa...``\n"
                               "``Para ativar sua box use o comando:`` **ash box buy**")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @box.command(name='buy', aliases=['comprar'])
    async def _buy(self, ctx):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data['config']['buying']:
            return await ctx.send('<:alert:739251822920728708>│``VOCE JA ESTA EM PROCESSO DE COMPRA...``')

        update['config']['buying'] = True
        await self.bot.db.update_data(data, update, 'users')

        def check_option(m):
            return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

        msg = await ctx.send("<a:loading:520418506567843860>│``Comprando a sua box...``")
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        if data['box']['status']['active']:
            await ctx.send("<:alert:739251822920728708>│``ATENÇÃO: VOCE JA TEM UMA BOX ATIVA NA SUA CONTA!``\n"
                           "``PARA ABRIR SUA BOX USE O COMANDO`` **ASH BOX BOOSTER**\n"
                           "``AGORA VOCE QUER RESETAR SUA BOX PARA OBTER UMA RARIDADE MAIOR?``\n"
                           "**1** para ``SIM`` ou **0** para ``NÃO``")
            try:
                answer = await self.bot.wait_for('message', check=check_option, timeout=30.0)
                answer = bool(int(answer.content))
                if answer:
                    await self.bot.booster.buy_box(self.bot, ctx)
                else:
                    data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                    update = data
                    update['config']['buying'] = False
                    await self.bot.db.update_data(data, update, 'users')
                    await msg.delete()
                    return await ctx.send('<:negate:721581573396496464>│**COMANDO CANCELADO PELO USUARIO!**')
            except TimeoutError:
                data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
                update = data
                update['config']['buying'] = False
                await self.bot.db.update_data(data, update, 'users')
                await msg.delete()
                return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` **COMANDO'
                                      ' CANCELADO**')
        else:
            await self.bot.booster.buy_box(self.bot, ctx)

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        if data['box']['status']['active']:
            await ctx.send(f"<:confirmed:721581574461587496>│``SUA BOX TEM A RARIDADE:`` "
                           f"**{data['box']['status']['rarity']}**")

        await msg.delete()
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        update['config']['buying'] = False
        await self.bot.db.update_data(data, update, 'users')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @box.command(name='booster', aliases=['pacote', 'abrir', 'open'])
    async def _booster(self, ctx):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if data['config']['buying']:
            return await ctx.send('<:alert:739251822920728708>│``VOCE JA ESTA EM PROCESSO DE COMPRA...``')

        if not data['box']['status']['active']:
            return await ctx.send("<:negate:520418505993093130>│``Você não tem uma box ativa...``\n"
                                  "``Para ativar sua box use o comando:`` **ash box buy**")

        update['config']['buying'] = True
        await self.bot.db.update_data(data, update, 'users')

        msg = await ctx.send("<a:loading:520418506567843860>│``Comprando booster...``")
        await ctx.send("<:alert:739251822920728708>│``Quantos boosters você deseja comprar?``")

        def check(m):
            return m.author.id == ctx.author.id and m.content.isdigit()

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=30.0)

        except TimeoutError:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['config']['buying'] = False
            await self.bot.db.update_data(data, update, 'users')
            await msg.delete()
            return await ctx.send('<:negate:721581573396496464>│``Desculpe, você demorou muito:`` **COMANDO'
                                  ' CANCELADO**')

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        num = int(answer.content)

        if num > 10:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['config']['buying'] = False
            await self.bot.db.update_data(data, update, 'users')
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``Você não pode comprar mais que 10 boosters"
                                  " de uma vez...``")

        if num < 1:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['config']['buying'] = False
            await self.bot.db.update_data(data, update, 'users')
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``Você não pode comprar 0 ou menos boosters``")

        price = 500
        if data['user']['ranking'] == "Bronze":
            price -= 50
        if data['user']['ranking'] == "Silver":
            price -= 75
        if data['user']['ranking'] == "Gold":
            price -= 125
        if data['config']['vip']:
            price -= 50
        num_ = self.verify_money(data['treasure']['money'], num, price)
        if num_ < num:
            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            update['config']['buying'] = False
            await self.bot.db.update_data(data, update, 'users')
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``Você não tem dinheiro o suficiente...``")
        for _ in range(num):
            if data['box']['status']['active']:
                await self.bot.booster.buy_booster(self.bot, ctx)
                await sleep(0.5)

        await msg.delete()
        await ctx.send("<:confirmed:721581574461587496>│``Obrigado pelas compras, volte sempre!``")

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        update['config']['buying'] = False
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(BoxClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mBOXCLASS\033[1;32m foi carregado com sucesso!\33[m')
