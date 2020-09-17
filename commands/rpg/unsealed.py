import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from random import choice
from asyncio import sleep, TimeoutError


git = ["https://media1.tenor.com/images/adda1e4a118be9fcff6e82148b51cade/tenor.gif?itemid=5613535",
       "https://media1.tenor.com/images/daf94e676837b6f46c0ab3881345c1a3/tenor.gif?itemid=9582062",
       "https://media1.tenor.com/images/0d8ed44c3d748aed455703272e2095a8/tenor.gif?itemid=3567970",
       "https://media1.tenor.com/images/17e1414f1dc91bc1f76159d7c3fa03ea/tenor.gif?itemid=15744166",
       "https://media1.tenor.com/images/39c363015f2ae22f212f9cd8df2a1063/tenor.gif?itemid=15894886"]


class MeltedClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.i = self.bot.items
        self.se = self.bot.config['equips']

        self.rarity = {
            "uncommon": 100,
            "rare": 50,
            "super rare": 30,
            "ultra rare": 19,
            "secret": 1
        }

        self.cost = {
            "melted_artifact": 1,
            "unsealed_stone": 2,
            "Discharge_Crystal": 10,
            "Acquittal_Crystal": 10,
            "Crystal_of_Energy": 10
        }

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='unsealed', aliases=['liberar', 'libertar'])
    async def unsealed(self, ctx, *, equip=None):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if equip is None:
            return await ctx.send("<:negate:721581573396496464>│``VOCE PRECISA DIZER O NOME DE UM EQUIPAMENTO!``")

        equip = equip.replace("_", " ")
        if equip.lower() not in [k.lower() for k in self.i.keys() if self.i[k][3] == 9]:
            return await ctx.send("<:negate:721581573396496464>│``VOCE PRECISA DIZER UM EQUIPAMENTO VALIDO!``")

        msg = f"\n".join([f"{self.i[k][0]} ``{v}`` ``{self.i[k][1]}``" for k, v in self.cost.items()])
        msg += "\n\n**OBS:** ``PARA CONSEGUIR OS ITENS VOCE PRECISAR USAR OS COMANDOS`` " \
               "**ASH MELTED, ASH STONE**  ``E`` **ASH BOX**"

        Embed = discord.Embed(
            title="O CUSTO PARA VOCE TIRAR O SELO DE UM EQUIPAMENTO:",
            color=self.bot.color,
            description=msg)
        Embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        Embed.set_thumbnail(url="{}".format(ctx.author.avatar_url))
        Embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=Embed)

        if equip not in data['inventory'].keys():
            return await ctx.send("<:negate:721581573396496464>│``Voce não tem esse equipamento no seu invetário...``\n"
                                  "**Obs:** ``VOCE CONSEGUE OS EQUIPAMENTOS CRAFTANDO, USANDO O COMANDO`` **ASH CRAFT**"
                                  " ``E O COMANDO`` **ASH RECIPE** ``PARA PEGAR AS RECEITAS DOS CRAFTS.``")

        cost = {}
        for i_, amount in self.cost.items():
            if i_ in data['inventory']:
                if data['inventory'][i_] < self.cost[i_]:
                    cost[i_] = self.cost[i_]
            else:
                cost[i_] = self.cost[i_]

        if len(cost) > 0:
            msg = f"\n".join([f"{self.i[key][0]} **{key.upper()}**" for key in cost.keys()])
            return await ctx.send(f"<:alert:739251822920728708>│``Lhe faltam esses itens para tirar o selo do item:``"
                                  f"\n{msg}\n``OLHE SEU INVENTARIO E VEJA A QUANTIDADE QUE ESTÁ FALTANDO.``")

        def check_option(m):
            return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

        msg = await ctx.send(f"<:alert:739251822920728708>│``VOCE JA TEM TODOS OS ITEM NECESSARIOS, DESEJA TIRAR O SELO"
                             f" DO SEU EQUIMENTO AGORA?``\n**1** para ``SIM`` ou **0** para ``NÃO``")
        try:
            answer = await self.bot.wait_for('message', check=check_option, timeout=30.0)
        except TimeoutError:
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``COMANDO CANCELADO!``")
        if answer.content == "0":
            await msg.delete()
            return await ctx.send("<:negate:721581573396496464>│``COMANDO CANCELADO!``")
        await msg.delete()

        msg = await ctx.send("<a:loading:520418506567843860>│``Selecionamento o equipamento para tirar o selo...``")
        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``removendo os itens de custo e o equipamento da sua "
                               f"conta...``")

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``removendo itens...``")

        for i_, amount in self.cost.items():
            update['inventory'][i_] -= amount
            if update['inventory'][i_] < 1:
                del update['inventory'][i_]

        await sleep(2)
        await msg.edit(content=f"<a:loading:520418506567843860>│``removendo equipamento...``")

        update['inventory'][equip] -= 1
        if update['inventory'][equip] < 1:
            del update['inventory'][equip]

        await msg.edit(content=f"<:confirmed:721581574461587496>│``itens retirados com sucesso...``")
        await sleep(2)

        # agora o item vai ser transformado em equipamento...

        await msg.edit(content=f"<a:loading:520418506567843860>│``Tirando o selo da sua armadura...``")

        list_rarity = []
        for i_, amount in self.rarity.items():
            list_rarity += [i_] * amount
        rarity = choice(list_rarity)

        legend = {
            "uncommon": "silver",
            "rare": "mystic",
            "super rare": "inspiron",
            "ultra rare": "violet",
            "secret": "hero"
        }

        reward_equip = None
        item_reward = equip.lower()
        item_reward = item_reward.replace("sealed", legend[rarity])

        if "leather" in equip:
            for k, v in self.se[f'set dynasty leather {rarity}'].items():
                if v['name'] == item_reward:
                    reward_equip = (k, v)
        elif "platinum" in equip:
            for k, v in self.se[f'set dynasty platinum {rarity}'].items():
                if v['name'] == item_reward:
                    reward_equip = (k, v)
        elif "cover" in equip:
            for k, v in self.se[f'set dynasty cover {rarity}'].items():
                if v['name'] == item_reward:
                    reward_equip = (k, v)

        try:
            update['rpg']['items'][reward_equip[0]] += 1
        except KeyError:
            update['rpg']['items'][reward_equip[0]] = 1
        await sleep(2)

        await msg.edit(content=f"<:confirmed:721581574461587496>│{reward_equip[1]['icon']} ``1`` "
                               f"**{reward_equip[1]['name']}** ``adicionado ao seu inventario com sucesso...``")

        img = choice(git)
        embed = discord.Embed(color=self.bot.color)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        await self.bot.db.update_data(data, update, 'users')


def setup(bot):
    bot.add_cog(MeltedClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mUNSEALED\033[1;32m foi carregado com sucesso!\33[m')
