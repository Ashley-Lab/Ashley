import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice
from asyncio import sleep


class MeltedClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.c = self.bot.color
        self.i = self.bot.items

        self.reward = {
            "G-Bollash": 90,
            "B-Bollash": 7,
            "O-Bollash": 2,
            "R-Bollash": 1
        }

        self.cost = {
            "?-Bollash": 1,
            "Crystal_of_Energy": 1,
            "Melted_Bone": 2,
            "Life_Crystal": 3,
            "Death_Blow": 2,
            "Stone_of_Soul": 3,
            "Vital_Force": 2,
        }

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='identifier', aliases=['identificar', 'identifique'])
    async def identifier(self, ctx):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        msg = f"\n".join([f"{self.i[k][0]} ``{v}`` ``{self.i[k][1]}``" for k, v in self.cost.items()])
        msg += "\n\n**OBS:** ``PARA CONSEGUIR OS ITENS VOCE PRECISAR USAR O COMANDO`` **ASH BOX**"

        Embed = discord.Embed(title="O CUSTO PARA VOCE IDENTIFICAR UMA ?-BOLLASH:", color=self.c, description=msg)
        Embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        Embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
        Embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=Embed)

        if update['inventory']['?-Bollash'] < 1:
            return await ctx.send("<:negate:721581573396496464>│``Voce nao tem o minimo de 1 ?-Bollash...``\n"
                                  "**Obs:** ``VOCE CONSEGUE SUAS ?-BOLLASH USANDO O COMANDO`` **ASH BOLLASH**")

        cost = {}
        for i_, amount in self.cost.items():
            if i_ in data['inventory']:
                if data['inventory'][i_] < self.cost[i_]:
                    cost[i_] = self.cost[i_]
            else:
                cost[i_] = self.cost[i_]

        if len(cost) > 0:
            msg = f"\n".join([f"{self.i[key][0]} **{key.upper()}**" for key in cost.keys()])
            return await ctx.send(f"<:alert:739251822920728708>│``Lhe faltam esses itens para derreter um arfetafo:``"
                                  f"\n{msg}\n``OLHE SEU INVENTARIO E VEJA A QUANTIDADE QUE ESTÁ FALTANDO.``")

        msg = await ctx.send("<a:loading:520418506567843860>│``Identificando sua ?-Bollash...``")
        await sleep(2)

        list_bollash = []
        for k, v in self.reward.items():
            list_bollash += [k] * v
        bollash = choice(list_bollash)

        await msg.edit(content=f"<:confirmed:721581574461587496>│``Sua ?-Bollash foi identificada como`` "
                               f"{self.i[bollash][0]} **{self.i[bollash][1]}**")

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``removendo os itens de custo da sua conta...``")
        for i_, amount in self.cost.items():
            update['inventory'][i_] -= amount
            if update['inventory'][i_] < 1:
                del update['inventory'][i_]

        await sleep(2)
        await msg.edit(content=f"<:confirmed:721581574461587496>│``itens retirados com sucesso...``")

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``Adicionando o`` {self.i[bollash][0]} "
                               f"**{self.i[bollash][1]}** ``para sua conta...``")
        try:
            update['inventory'][bollash] += 1
        except KeyError:
            update['inventory'][bollash] = 1
        await sleep(2)
        await msg.edit(content=f"<:confirmed:721581574461587496>│{self.i[bollash][0]} ``1``"
                               f"**{self.i[bollash][1]}** ``adicionado ao seu inventario com sucesso...``")
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(MeltedClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMELTED\033[1;32m foi carregado com sucesso!\33[m')
