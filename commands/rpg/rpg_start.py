import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError


class RpgStart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.c = "``Comando Cancelado``"
        self.cl = ['paladin', 'necromancer', 'wizard', 'warrior', 'priest', 'warlock', 'assassin']

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='rpg', aliases=['start'])
    async def rpg(self, ctx):
        """Esse nem eu sei..."""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        asks = {'lower_net': False, 'next_class': None}

        def check_battle(m):
            return m.author == ctx.author and m.content == '0' or m.author == ctx.author and m.content == '1'

        def check_option(m):
            return m.author == ctx.author and m.content.isdigit()

        embed = discord.Embed(color=self.bot.color,
                              description=f'<:stream_status:519896814825242635>│``DESEJA ATIVAR O MODO DE BATALHA SEM '
                                          f'IMAGEM?``\n```O modo de batalha sem imagem faz com que seja carregado '
                                          f'mais rapido as mensagens```\n**1** para ``SIM`` ou **0** para ``NÃO``')
        msg = await ctx.send(embed=embed)

        try:
            answer = await self.bot.wait_for('message', check=check_battle, timeout=30.0)
        except TimeoutError:
            embed = discord.Embed(color=self.bot.color, description=f'<:negate:721581573396496464>│{self.c}')
            return await ctx.send(embed=embed)

        asks['lower_net'] = True if answer.content == "1" else False
        await msg.delete()

        embed = discord.Embed(color=self.bot.color,
                              description=f'<:stream_status:519896814825242635>│``QUAL CLASSE VOCE DESEJA APRENDER?``\n'
                                          f'```As classes fazem voce aprender habilidades unicas de cada uma```\n'
                                          f'``USE OS NUMEROS PARA DIZER QUAL CLASSE VOCE DESEJA:``\n'
                                          f'**1** para ``{self.cl[0].upper()}``\n**2** para ``{self.cl[1].upper()}``\n'
                                          f'**3** para ``{self.cl[2].upper()}``\n**4** para ``{self.cl[3].upper()}``\n'
                                          f'**5** para ``{self.cl[4].upper()}``\n**6** para ``{self.cl[5].upper()}``\n'
                                          f'**7** para ``{self.cl[6].upper()}``')
        msg = await ctx.send(embed=embed)

        try:
            answer = await self.bot.wait_for('message', check=check_option, timeout=30.0)
        except TimeoutError:
            embed = discord.Embed(color=self.bot.color, description=f'<:negate:721581573396496464>│{self.c}')
            return await ctx.send(embed=embed)

        if int(answer.content) in [1, 2, 3, 4, 5, 6, 7]:
            asks['next_class'] = self.cl[int(answer.content) - 1]
        else:
            await msg.delete()
            return await ctx.send("f'<:negate:721581573396496464>│``ESSA OPÇAO NAO ESTÁ DISPONIVEL, TENTE NOVAMENTE!``")
        await msg.delete()

        rpg = {
            "vip": update['rpg']['vip'],
            "lower_net": asks['lower_net'],
            "Class": 'Default',
            "next_class": asks['next_class'],
            "Level": 1,
            "XP": 0,
            "Status": {"con": 5, "prec": 5, "agi": 5, "atk": 5, "luk": 0, "pdh": 0},
            "artifacts": dict(),
            "relics": dict(),
            'items': list(),
            'equipped_items': list(),
            "status": True
        }

        update['rpg'] = rpg
        await self.bot.db.update_data(data, update, 'users')
        embed = discord.Embed(color=self.bot.color,
                              description=f'<:confirmed:721581574461587496>│``CONFIGURAÇÃO DO RPG FEITA COM SUCESSO!``')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(RpgStart(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mRPG_START_SYSTEM\033[1;32m foi carregado com sucesso!\33[m')
