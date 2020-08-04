import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice
from asyncio import sleep


class MeltedClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.i = self.bot.items
        self.art = ["braço_direito", "braço_esquerdo", "perna_direita", "perna_esquerda", "the_one", "anel", "balança",
                    "chave", "colar", "enigma", "olho", "vara", "aquario", "aries", "cancer", "capricornio",
                    "escorpiao", "gemeos", "leao", "peixes", "sargitario", "libra", "touro", "virgem"]

        self.cost = {
            "solution_agent_green": 3,
            "solution_agent_blue": 3,
            "nucleo_xyz": 2,
            "enchanted_stone": 1,
            "Discharge_Crystal": 4,
            "Acquittal_Crystal": 4,
            "Crystal_of_Energy": 8,
            "crystal_of_death": 2
        }

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='melted', aliases=['derreter'])
    async def melted(self, ctx):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        Embed = discord.Embed(
            title="O CUSTO PARA VOCE DERRETER UM ARTEFATO:",
            color=self.bot.color,
            description=f"\n".join([f"{self.i[k][0]} ``{v}`` ``{self.i[k][1]}``" for k, v in self.cost.items()])
        )
        Embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        Embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
        Embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=Embed)

        artifacts = []
        for i_, amount in data['inventory'].items():
            if i_ in self.art:
                artifacts += [i_] * amount

        if len(artifacts) < 3:
            return await ctx.send("<:negate:721581573396496464>│``Voce nao tem o minimo de 3 arfetados...``")

        cost = {}
        for i_, amount in self.cost.items():
            if i_ in data['inventory']:
                if data['inventory'][i_] < self.cost[i_]:
                    cost[i_] = self.cost[i_]
            else:
                cost[i_] = self.cost[i_]

        if len(cost) > 0:
            msg = f"\n".join([f"{self.i[key][0]} **{self.i[key][1]}**" for key in cost.keys()])
            return await ctx.send(f"<:alert:739251822920728708>│``Lhe faltam esses itens para derreter um arfetafo:``"
                                  f"\n{msg}\n``OLHE SEU INVENTARIO E VEJA A QUANTIDADE QUE ESTÁ FALTANDO.``")

        msg = await ctx.send("<a:loading:520418506567843860>│``Escolhendo 3 artefatos para derreter...``")
        await sleep(2)
        art1 = choice(artifacts)
        await msg.edit(content=f"<:confirmed:721581574461587496>│``O primeiro foi`` {self.i[art1][0]} **{art1}**")
        await sleep(2)
        artifacts.remove(art1)
        art2 = choice(artifacts)
        await msg.edit(content=f"<:confirmed:721581574461587496>│``O segundo foi`` {self.i[art2][0]} **{art2}**")
        await sleep(2)
        artifacts.remove(art2)
        art3 = choice(artifacts)
        await msg.edit(content=f"<:confirmed:721581574461587496>│``O terceiro foi`` {self.i[art3][0]} **{art3}**")
        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``removendo os itens de custo e os artefatos da sua "
                               f"conta...``")
        for i_, amount in self.cost.items():
            update['inventory'][i_] -= amount
            if update['inventory'][i_] < 1:
                del update['inventory'][i_]

        update['artifacts'][art1] -= art1
        if update['artifacts'][art1] < 1:
            del update['artifacts'][art1]

        update['artifacts'][art2] -= art2
        if update['artifacts'][art2] < 1:
            del update['artifacts'][art2]

        update['artifacts'][art3] -= art3
        if update['artifacts'][art3] < 1:
            del update['artifacts'][art3]
        await msg.edit(content=f"<:confirmed:721581574461587496>│``itens retirados com sucesso...``")
        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``Adicionando o`` <:melted_artifact:739573767260471356>"
                               f" **Melted Artifact** ``para sua conta...``")
        try:
            update['inventory']['melted_artifact'] += 1
        except KeyError:
            update['inventory']['melted_artifact'] = 1
        await sleep(2)
        await msg.edit(content=f"<:confirmed:721581574461587496>│<:melted_artifact:739573767260471356> "
                               f"**Melted Artifact** ``adicionado com sucesso...``")
        # await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(MeltedClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mMELTED\033[1;32m foi carregado com sucesso!\33[m')
