import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import randint
from asyncio import sleep


class MineClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items = self.bot.items

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='mine', aliases=['minerar'])
    async def mine(self, ctx):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        try:
            if data['inventory']['Energy']:
                pass
        except KeyError:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE NÃO TEM ENERGIA!``')
            return await ctx.send(embed=embed)

        if update['inventory']['Energy'] < 25:
            return await ctx.send('<:alert:739251822920728708>│``VOCÊ PRECISA DE + DE 25 ENERGIAS PARA MINERAR``')

        update['inventory']['Energy'] -= 25
        if update['inventory']['Energy'] < 1:
            del update['inventory']['Energy']

        quant = 0

        text = "Minerando...\n----------.----------.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        msg = await ctx.send(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==--------.----------.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n====------.----------.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n======----.----------.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n========--.----------.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.----------.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 20:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items['sapphire'][0]} **{self.items['sapphire'][1]}**")

            try:
                update['inventory']['sapphire'] += item
            except KeyError:
                update['inventory']['sapphire'] = item
        # ========================================================================================

        text = "Minerando...\n==========.==--------.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.====------.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.======----.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.========--.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.----------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 15:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items['ruby'][0]} **{self.items['ruby'][1]}**")

            try:
                update['inventory']['ruby'] += item
            except KeyError:
                update['inventory']['ruby'] = item
        # ========================================================================================

        text = "Minerando...\n==========.==========.==--------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.====------.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.======----.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.========--.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.==========.----------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 10:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items['emerald'][0]} **{self.items['emerald'][1]}**")

            try:
                update['inventory']['emerald'] += item
            except KeyError:
                update['inventory']['emerald'] = item
        # ========================================================================================

        text = "Minerando...\n==========.==========.==========.==--------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.==========.====------.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.==========.======----.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.==========.========--.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.==========.==========.----------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 5:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items['diamond'][0]} **{self.items['diamond'][1]}**")

            try:
                update['inventory']['diamond'] += item
            except KeyError:
                update['inventory']['diamond'] = item
        # ========================================================================================

        text = "Minerando...\n==========.==========.==========.==========.==--------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.==========.==========.====------"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.==========.==========.======----"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "Minerando...\n==========.==========.==========.==========.========--"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        text = "MINERADO!\n==========.==========.==========.==========.=========="
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(0.2)

        # ========================================================================================
        if quant > 0:
            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 ``VOCE MINEROU:``\n"
                           f"``{quant}`` **ITENS NO TOTAL.**")
        else:
            await ctx.send(f"<:confirmed:721581574461587496>│``VOCE MINEROU:``\n"
                           f"``{quant}`` **ITENS NO TOTAL.** ``TENTE NOVAMENTE...``")
        # ========================================================================================
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(MineClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMINE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
