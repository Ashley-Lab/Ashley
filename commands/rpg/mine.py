import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import randint, choice
from asyncio import sleep


class MineClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items = self.bot.items
        self.reward = ['sapphire', 'sapphire', 'sapphire', 'sapphire', 'sapphire', 'sapphire',
                       'sapphire', 'sapphire', 'sapphire', 'sapphire', 'sapphire', 'sapphire',
                       'ruby', 'ruby', 'ruby', 'ruby', 'ruby', 'ruby', 'ruby', 'ruby',
                       'emerald', 'emerald', 'emerald', 'emerald', 'diamond', 'diamond']

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='mine', aliases=['minerar'])
    async def mine(self, ctx):
        """Comando para minerar pedras preciosas."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        try:
            if update['inventory']['Energy']:
                pass
        except KeyError:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``VOCE NÃO TEM ENERGIA!``')
            return await ctx.send(embed=embed)

        if update['config']['mine']:
            return await ctx.send('<:alert:739251822920728708>│``VOCÊ JA ESTÁ MINERANDO...``')

        if update['inventory']['Energy'] < 25:
            return await ctx.send('<:alert:739251822920728708>│``VOCÊ PRECISA DE + DE 25 ENERGIAS PARA MINERAR``')

        update['inventory']['Energy'] -= 25
        if update['inventory']['Energy'] < 1:
            del update['inventory']['Energy']

        update['config']['mine'] = True
        await self.bot.db.update_data(data, update, 'users')
        quant = 0

        text = "Minerando 0%...\n``--------------------------------------------------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        msg = await ctx.send(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 5:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 10%...\n``█████---------------------------------------------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 10:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 20%...\n``██████████----------------------------------------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 15:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 30%...\n``███████████████-----------------------------------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 20:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 40%...\n``████████████████████------------------------------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 25:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 50%...\n``█████████████████████████-------------------------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 30:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 60%...\n``██████████████████████████████--------------------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 35:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 70%...\n``███████████████████████████████████---------------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 40:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 80%...\n``████████████████████████████████████████----------``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 45:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "Minerando 90%...\n``█████████████████████████████████████████████-----``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        chance = randint(1, 100)
        if chance < 50:
            if chance == 1:
                quant += 2
                item = 2
            else:
                quant += 1
                item = 1

            reward = choice(self.reward)

            await ctx.send(f"<a:fofo:524950742487007233>│🎊 **PARABENS** 🎉 {ctx.author.name} ``VOCE MINEROU:``\n"
                           f"``+{item}`` {self.items[reward][0]} **{self.items[reward][1]}**")

            data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
            update = data
            try:
                update['inventory'][reward] += item
            except KeyError:
                update['inventory'][reward] = item
            await self.bot.db.update_data(data, update, 'users')
        # ========================================================================================

        text = "**MINERADO 100%!**\n``██████████████████████████████████████████████████``"
        embed = discord.Embed(color=self.bot.color, description=text)
        await msg.edit(embed=embed)
        await sleep(3)

        # ========================================================================================
        await ctx.send(f"<:confirmed:721581574461587496>│{ctx.author.name} ``VOCE MINEROU:``\n"
                       f"``{quant}`` **ITENS NO TOTAL.**")
        # ========================================================================================

        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data
        update['config']['mine'] = False
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(MineClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMINE_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
