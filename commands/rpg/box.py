import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError, sleep

legend = {"Comum": 500, "Incomum": 400, "Raro": 300, "Super Raro": 200, "Ultra Raro": 150, "Secret": 100}


class BoxClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @staticmethod
    def verify_money(money, num):
        cont = 0
        for _ in range(num):
            if money > 500:
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
            if data is not None:
                if data['box']['status']['active']:
                    status = data['box']['status']['active']
                    rarity = data['box']['status']['rarity']
                    num = legend[rarity]
                    secret = data['box']['status']['secret']
                    ur = data['box']['status']['ur']
                    sr = data['box']['status']['sr']
                    r = data['box']['status']['r']
                    i = data['box']['status']['i']
                    c = data['box']['status']['c']
                    size = data['box']['status']['size']
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
<SECRET: {}>
<UR: {}>
<SR: {}>
<R: {}>
<I: {}>
<C: {}>
<SIZE: {}/{}>```'''.format(rarity, status, secret, ur, sr, r, i, c, size, num)
                    box = discord.Embed(
                        title="{}'s box:".format(ctx.author.name),
                        color=self.color,
                        description=description
                    )
                    box.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
                    box.set_thumbnail(url="{}".format(images[rarity]))
                    box.set_footer(text="Ashley ® Todos os direitos reservados.")
                    await ctx.send(embed=box)
                else:
                    await ctx.send("<:negate:520418505993093130>│``Você não tem uma box ativa...``\n"
                                   "``Para ativar sua box use o comando:`` **ash box buy**")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @box.command(name='buy', aliases=['comprar'])
    async def _buy(self, ctx):
        await ctx.send("<:alert_status:519896811192844288>│``Comprando a sua box...``")
        await self.bot.booster.buy_box(self.bot, ctx)
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        await ctx.send(f"<:on_status:519896814799945728>│``SUA BOX TEM A RARIDADE:`` "
                       f"**{data['box']['status']['rarity']}**")

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @box.command(name='booster', aliases=['pacote'])
    async def _booster(self, ctx):
        await ctx.send("<:alert_status:519896811192844288>│``Comprando booster...``")
        await ctx.send("<:alert_status:519896811192844288>│``Quantos boosters você deseja comprar?``")

        def check(m):
            return m.author.id == ctx.author.id and m.content.isdigit()

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=60.0)
        except TimeoutError:
            return await ctx.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                  ' CANCELADO**')

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        num = int(answer.content)
        if num > 10:
            return await ctx.send("<:negate:520418505993093130>│``Você não pode comprar mais que 10 boosters"
                                  " de uma vez...``")
        elif num < 1:
            return await ctx.send("<:negate:520418505993093130>│``Você não pode comprar 0 ou menos boosters``")

        if data['box']['status']['active']:
            num_ = self.verify_money(data['treasure']['money'], num)
            if num_ < num:
                return await ctx.send("<:negate:520418505993093130>│``Você não tem dinheiro o suficiente...``")
            for _ in range(num):
                await self.bot.booster.buy_booster(self.bot, ctx)
                await sleep(0.5)
            await ctx.send("<:on_status:519896814799945728>│``Obrigado pelas compras, volte sempre!``")
        else:
            await ctx.send("<:negate:520418505993093130>│``Você não tem uma box ativa...``\n"
                           "``Para ativar sua box use o comando:`` **ash box buy**")


def setup(bot):
    bot.add_cog(BoxClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mBOXCLASS\033[1;32m foi carregado com sucesso!\33[m')
