import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError, sleep

botmsg = {}
ctx_ = {}


class ShopClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.color

    @staticmethod
    def verify_money(data, num):
        cont = 0
        for _ in range(num):
            if data['treasure']['bronze'] > 100:
                cont += 1
            elif data['treasure']['silver'] > 10:
                cont += 1
            elif data['treasure']['gold'] > 1:
                cont += 1
            else:
                pass
        return cont

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='shop', aliases=['loja'])
    async def shop(self, ctx):
        embed = discord.Embed(
            title="Choice Category:",
            color=self.color,
            description=f"- For **Box**: click in <:gold_box:546019944211415040>\n"
                        f"- For **Booster**: click in <:coin:546019942936608778>\n"
                        f"- For **-**: click in <:booster_f:546019942756253764>\n"
                        f"- For **-**: click in <:booster_e:546019942374572053>\n"
                        f"- For **-**: click in <:booster_d:546019942550601729>\n"
                        f"- For **-**: click in <:booster_c:546019942705922048>\n"
                        f"- For **-**: click in <:booster_b:546019942512853003>\n"
                        f"- For **-**: click in <:booster_a:546019942680756234>")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        global botmsg, ctx_
        ctx_[ctx.author.id] = ctx
        botmsg[ctx.author.id] = await ctx.send(embed=embed)
        await botmsg[ctx.author.id].add_reaction('<:gold_box:546019944211415040>')
        await botmsg[ctx.author.id].add_reaction('<:coin:546019942936608778>')
        await botmsg[ctx.author.id].add_reaction('<:booster_f:546019942756253764>')
        await botmsg[ctx.author.id].add_reaction('<:booster_e:546019942374572053>')
        await botmsg[ctx.author.id].add_reaction('<:booster_d:546019942550601729>')
        await botmsg[ctx.author.id].add_reaction('<:booster_c:546019942705922048>')
        await botmsg[ctx.author.id].add_reaction('<:booster_b:546019942512853003>')
        await botmsg[ctx.author.id].add_reaction('<:booster_a:546019942680756234>')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        try:
            if botmsg[user.id]:
                pass
        except KeyError:
            return

        channel = self.bot.get_channel(reaction.message.channel.id)

        if reaction.emoji == "↩" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="Choice Category",
                color=self.color,
                description=f"- For **Box**: click in <:gold_box:546019944211415040>\n"
                            f"- For **Booster**: click in <:coin:546019942936608778>\n"
                            f"- For **-**: click in <:booster_f:546019942756253764>\n"
                            f"- For **-**: click in <:booster_e:546019942374572053>\n"
                            f"- For **-**: click in <:booster_d:546019942550601729>\n"
                            f"- For **-**: click in <:booster_c:546019942705922048>\n"
                            f"- For **-**: click in <:booster_b:546019942512853003>\n"
                            f"- For **-**: click in <:booster_a:546019942680756234>")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('<:gold_box:546019944211415040>')
                await botmsg[user.id].add_reaction('<:coin:546019942936608778>')
                await botmsg[user.id].add_reaction('<:booster_f:546019942756253764>')
                await botmsg[user.id].add_reaction('<:booster_e:546019942374572053>')
                await botmsg[user.id].add_reaction('<:booster_d:546019942550601729>')
                await botmsg[user.id].add_reaction('<:booster_c:546019942705922048>')
                await botmsg[user.id].add_reaction('<:booster_b:546019942512853003>')
                await botmsg[user.id].add_reaction('<:booster_a:546019942680756234>')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('<:gold_box:546019944211415040>')
                await botmsg[user.id].add_reaction('<:coin:546019942936608778>')
                await botmsg[user.id].add_reaction('<:booster_f:546019942756253764>')
                await botmsg[user.id].add_reaction('<:booster_e:546019942374572053>')
                await botmsg[user.id].add_reaction('<:booster_d:546019942550601729>')
                await botmsg[user.id].add_reaction('<:booster_c:546019942705922048>')
                await botmsg[user.id].add_reaction('<:booster_b:546019942512853003>')
                await botmsg[user.id].add_reaction('<:booster_a:546019942680756234>')

        if str(reaction.emoji) == "<:gold_box:546019944211415040>" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="Box",
                color=self.color,
                description=f"- For **Buy**: click in 🎫\n"
                            f"- For **Reset**: click in 💳\n"
                            f"- For **Back**: click in ↩")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('🎫')
                await botmsg[user.id].add_reaction('💳')
                await botmsg[user.id].add_reaction('↩')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('🎫')
                await botmsg[user.id].add_reaction('💳')
                await botmsg[user.id].add_reaction('↩')

        if str(reaction.emoji) == "<:coin:546019942936608778>" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="Booster",
                color=self.color,
                description=f"- For **Buy**: click in 💵\n"
                            f"- For **Back**: click in ↩")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('💵')
                await botmsg[user.id].add_reaction('↩')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('💵')
                await botmsg[user.id].add_reaction('↩')

        if str(reaction.emoji) == "<:booster_f:546019942756253764>" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="Booster",
                color=self.color,
                description=f"- For **Buy**: click in <:1_:578615669487304704>\n"
                            f"- For **Reset**: click in <:2_:578615674109165568>\n"
                            f"- For **Back**: click in ↩")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')

        if str(reaction.emoji) == "<:booster_e:546019942374572053>" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="None",
                color=self.color,
                description=f"- For **Buy**: click in <:1_:578615669487304704>\n"
                            f"- For **Reset**: click in <:2_:578615674109165568>\n"
                            f"- For **Back**: click in ↩")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')

        if str(reaction.emoji) == "<:booster_d:546019942550601729>" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="None",
                color=self.color,
                description=f"- For **Buy**: click in <:1_:578615669487304704>\n"
                            f"- For **Reset**: click in <:2_:578615674109165568>\n"
                            f"- For **Back**: click in ↩")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')

        if str(reaction.emoji) == "<:booster_c:546019942705922048>" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="None",
                color=self.color,
                description=f"- For **Buy**: click in <:1_:578615669487304704>\n"
                            f"- For **Reset**: click in <:2_:578615674109165568>\n"
                            f"- For **Back**: click in ↩")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')

        if str(reaction.emoji) == "<:booster_b:546019942512853003>" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="None",
                color=self.color,
                description=f"- For **Buy**: click in <:1_:578615669487304704>\n"
                            f"- For **Reset**: click in <:2_:578615674109165568>\n"
                            f"- For **Back**: click in ↩")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')

        if str(reaction.emoji) == "<:booster_a:546019942680756234>" and reaction.message.id == botmsg[user.id].id:
            embed = discord.Embed(
                title="None",
                color=self.color,
                description=f"- For **Buy**: click in <:1_:578615669487304704>\n"
                            f"- For **Reset**: click in <:2_:578615674109165568>\n"
                            f"- For **Back**: click in ↩")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url="https://icon-library.net/images/shop-icon-png/shop-icon-png-6.jpg")
            embed.set_footer(text="Ashley ® Todos os direitos reservados.")
            try:
                await botmsg[user.id].clear_reactions()
                await botmsg[user.id].edit(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')
            except discord.errors.Forbidden:
                await botmsg[user.id].delete()
                botmsg[user.id] = await channel.send(embed=embed)
                await botmsg[user.id].add_reaction('<:1_:578615669487304704>')
                await botmsg[user.id].add_reaction('<:2_:578615674109165568>')
                await botmsg[user.id].add_reaction('↩')

        if str(reaction.emoji) == "<:1_:578615669487304704>" and reaction.message.id == botmsg[user.id].id:
            botmsg[user.id] = await channel.send("<:negate:520418505993093130>│``Em contrução...``")

        if str(reaction.emoji) == "<:2_:578615674109165568>" and reaction.message.id == botmsg[user.id].id:
            botmsg[user.id] = await channel.send("<:negate:520418505993093130>│``Em contrução...``")

        if reaction.emoji == "🎫" and reaction.message.id == botmsg[user.id].id:
            await channel.send("<:alert_status:519896811192844288>│``Comprando box...``")
            data = self.bot.db.get_data("user_id", user.id, "users")
            try:
                if data['box']:
                    await channel.send("<:negate:520418505993093130>│``Você ja tem uma box...``")
            except KeyError:
                await self.bot.booster.buy_box(self.bot, ctx_[user.id])

        if reaction.emoji == "💳" and reaction.message.id == botmsg[user.id].id:
            await channel.send("<:alert_status:519896811192844288>│``Resetando box...``")
            await self.bot.booster.buy_box(self.bot, ctx_[user.id])

        if reaction.emoji == "💵" and reaction.message.id == botmsg[user.id].id:
            await channel.send("<:alert_status:519896811192844288>│``Comprando booster...``")
            await channel.send("<:alert_status:519896811192844288>│``Quantos boosters você deseja comprar?``")

            def check(m):
                return m.author.id == user.id and m.content.isdigit()

            try:
                answer = await self.bot.wait_for('message', check=check, timeout=60.0)
            except TimeoutError:
                return await channel.send('<:negate:520418505993093130>│``Desculpe, você demorou muito:`` **COMANDO'
                                          ' CANCELADO**')

            data = self.bot.db.get_data("user_id", user.id, "users")
            num = int(answer.content)
            if num > 10:
                return await channel.send("<:negate:520418505993093130>│``Você não pode comprar mais que 10 booster"
                                          " de uma vez...``")
            try:
                if data['box']:
                    num_ = self.verify_money(data, num)
                    if num_ < num:
                        return await channel.send("<:negate:520418505993093130>│``Você não tem dinheiro o"
                                                  " suficiente...``")
                    for c in range(num):
                        await self.bot.booster.buy_booster(self.bot, ctx_[user.id])
                        await sleep(1)
                    await channel.send("<:on_status:519896814799945728>│``Obrigado pelas compras, volte sempre!``")
            except KeyError:
                await channel.send("<:negate:520418505993093130>│``Você ainda não tem uma box...``")


def setup(bot):
    bot.add_cog(ShopClass(bot))
    print('\033[1;32m( * ) | O comando \033[1;34mSHOP\033[1;32m foi carregado com sucesso!\33[m')
