import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database
from asyncio import TimeoutError, sleep
from config import data as _data
from random import randint
from resources.utility import create_id

limit = 16
_class = _data['skills']
levels = [5, 10, 15, 20, 25]


class EnchanterClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = None
        self.atacks = {}
        self.up_chance = 0
        self.chance_skill = self.bot.config['attribute']['chance_skill']
        self.botmsg = {}
        self.he = self.bot.help_emoji

    def config_player(self, user, data, lower_net):
        # configuração do player
        set_value = ["shoulder", "breastplate", "gloves", "leggings", "boots"]
        db_player = data
        db_player["img"] = user.avatar_url_as(format="png")
        db_player['name'] = user.name
        db_player["armor"] = 0
        db_player["lower_net"] = lower_net
        set_e = list()

        # bonus status player
        eq = dict()
        for ky in self.bot.config["equips"].keys():
            for kk, vv in self.bot.config["equips"][ky].items():
                eq[kk] = vv

        for k in db_player["status"].keys():
            try:
                db_player["status"][k] += self.bot.config["skills"][db_player['class']]['modifier'][k]
                if db_player['level'] > 25:
                    db_player["status"][k] += self.bot.config["skills"][db_player['next_class']]['modifier'][k]
            except KeyError:
                pass

        for c in db_player['equipped_items'].keys():
            if db_player['equipped_items'][c] is None:
                continue

            if c in set_value:
                set_e.append(str(c))

            db_player["armor"] += eq[db_player['equipped_items'][c]]['armor']
            for name in db_player["status"].keys():
                try:
                    db_player["status"][name] += eq[db_player['equipped_items'][c]]['modifier'][name]
                except KeyError:
                    pass

        for kkk in self.bot.config["set_equips"].values():
            if kkk['set'] == set_e:
                for name in db_player["status"].keys():
                    try:
                        db_player["status"][name] += kkk['modifier'][name]
                    except KeyError:
                        pass

        return db_player

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.group(name='enchant', aliases=['encantar', 'en'])
    async def enchant(self, ctx):
        """Comando usado pra ver os encatamentos das suas habilidades no rpg da Ashley
        Use ash enchant"""
        if ctx.invoked_subcommand is None:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                member = ctx.author

            try:
                if self.he[ctx.author.id]:
                    if str(ctx.command) in self.he[ctx.author.id].keys():
                        pass
                    else:
                        self.he[ctx.author.id][str(ctx.command)] = False
            except KeyError:
                self.he[ctx.author.id] = {str(ctx.command): False}

            data = await self.bot.db.get_data("user_id", member.id, "users")

            if not data['rpg']['active']:
                embed = discord.Embed(
                    color=self.bot.color,
                    description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
                return await ctx.send(embed=embed)

            self.atacks = {}
            data_player = self.config_player(ctx.author, data['rpg'], data['rpg']['lower_net'])
            rate = [_class[data_player['class']]['rate']['life'], _class[data_player['class']]['rate']['mana']]
            if data_player['level'] > 25:
                rate[0] += _class[data_player['next_class']]['rate']['life']
                rate[1] += _class[data_player['next_class']]['rate']['mana']
            data_player['status']['hp'] = data_player['status']['con'] * rate[0]
            data_player['status']['mp'] = data_player['status']['con'] * rate[1]

            self.db = data_player
            for c in range(5):
                if self.db['level'] >= levels[c]:
                    self.atacks[_class[self.db['next_class']][str(c)]['name']] = _class[self.db['next_class']][str(c)]
                else:
                    self.atacks[_class[self.db['class']][str(c)]['name']] = _class[self.db['class']][str(c)]
            atacks = eval(str(self.atacks.keys()).replace('dict_keys(', '').replace(')', ''))

            description = ''
            for c in range(0, len(atacks)):
                lvs = self.db['skills'][c]
                lvl_skill = lvs if 0 <= lvs <= 9 else 9
                c2, ls = atacks[c], lvs
                dado = self.atacks[c2]['damage'][lvl_skill]
                d1 = int(dado[:dado.find('d')])
                d2 = int(dado[dado.find('d') + 1:])
                dd = f"{f'{d2}-{d2 * d1}' if d2 != d2 * d1 else d2}"
                if lvs >= 11:
                    dd = f'{d2 + int((lvs - 10) * 10)}-{d2 * d1}'
                icon = self.atacks[c2]['icon']
                skill_type = self.atacks[c2]['type']

                try:
                    effect_skill = str(self.atacks[c2]['effs'][lvl_skill].keys())
                except KeyError:
                    effect_skill = "sem efeito"
                except TypeError:
                    effect_skill = "sem efeito"

                rm = int(((self.db['status']['con'] * _class[self.db['next_class']]['rate']['mana']) / 100) * 35)
                ru = int(((self.db['status']['con'] * _class[self.db['next_class']]['rate']['mana']) / 100) * 50)
                eff_mana = effect_skill.replace('dict_keys([', '').replace('])', '').replace('\'', '')
                a_mana = self.atacks[c2]['mana'][lvl_skill] + self.db['level']
                if self.db['level'] > 25:
                    a_mana = self.atacks[c2]['mana'][lvl_skill] + (self.db['level'] * 2)

                _mana = a_mana if eff_mana != "cura" else rm
                _mana = ru if self.atacks[c2]['type'] == "especial" else _mana
                damage = int(self.db['status']['atk'] * 2 / 100 * (80 + c * 10))

                description += f"{icon} **{c2.upper()}** ``+{ls}``\n" \
                               f"``Dano:`` {f'**{dd} + {damage}**' if ls > 0 else f'**{damage}**'}\n``Tipo:`` " \
                               f"**{skill_type.upper()}**\n``Mana:`` **{_mana}**\n``Efeito(s):`` **{effect_skill}**" \
                               f"\n\n".replace('dict_keys([', '').replace('])', '').replace('\'', '')

            TM = int(self.db['status']['con'] * _class[self.db['next_class']]['rate']['mana'])

            embed = discord.Embed(title=f"ENCHANTER PANEL - TOTAL MANA: {TM}", description=description, color=0x000000)
            embed.set_thumbnail(url=ctx.author.avatar_url)

            _id = create_id()

            self.botmsg[_id] = await ctx.send(embed=embed)
            if not self.he[ctx.author.id][str(ctx.command)]:
                await self.botmsg[_id].add_reaction('<a:help:767825933892583444>')
                await self.botmsg[_id].add_reaction(self.bot.config['emojis']['arrow'][4])

            text = "```Markdown\n[>>]: PARA ENCANTAR UMA SKILL USE O COMANDO\n<ASH ENCHANT ADD NUMERO_DA_SKILL>```"

            again = False
            msg = None
            if not self.he[ctx.author.id][str(ctx.command)]:
                self.he[ctx.author.id][str(ctx.command)] = True
                while not self.bot.is_closed():
                    try:
                        reaction = await self.bot.wait_for('reaction_add', timeout=30.0)
                        while reaction[1].id != ctx.author.id:
                            reaction = await self.bot.wait_for('reaction_add', timeout=30.0)

                        emo = "<a:help:767825933892583444>"
                        emoji = str(emo).replace('<a:', '').replace(emo[emo.rfind(':'):], '')
                        emo_2 = self.bot.config['emojis']['arrow'][4]
                        emoji_2 = str(emo_2).replace('<:', '').replace(emo_2[emo_2.rfind(':'):], '')

                        try:
                            try:
                                _reaction = reaction[0].emoji.name
                            except AttributeError:
                                _reaction = reaction[0].emoji

                            if _reaction == emoji and reaction[0].message.id == self.botmsg[_id].id and not again:
                                if reaction[1].id == ctx.author.id:
                                    again = True
                                    try:
                                        await self.botmsg[_id].remove_reaction("<a:help:767825933892583444>",
                                                                               ctx.author)
                                    except discord.errors.Forbidden:
                                        pass
                                    msg = await ctx.send(text)

                            elif _reaction == emoji and reaction[0].message.id == self.botmsg[_id].id and again:
                                if reaction[1].id == ctx.author.id:
                                    again = False
                                    try:
                                        await self.botmsg[_id].remove_reaction("<a:help:767825933892583444>",
                                                                               ctx.author)
                                    except discord.errors.Forbidden:
                                        pass
                                    await msg.delete()

                            if _reaction == emoji_2 and reaction[0].message.id == self.botmsg[_id].id:
                                if reaction[1].id == ctx.author.id:
                                    self.he[ctx.author.id][str(ctx.command)] = False
                                    await self.botmsg[_id].remove_reaction(
                                        self.bot.config['emojis']['arrow'][4], ctx.me)
                                    await self.botmsg[_id].remove_reaction(
                                        "<a:help:767825933892583444>", ctx.me)
                                    return

                        except AttributeError:
                            pass
                    except TimeoutError:
                        self.he[ctx.author.id][str(ctx.command)] = False
                        await self.botmsg[_id].remove_reaction(self.bot.config['emojis']['arrow'][4], ctx.me)
                        await self.botmsg[_id].remove_reaction("<a:help:767825933892583444>", ctx.me)
                        return

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @enchant.command(name='add', aliases=['adicionar'])
    async def _add(self, ctx, skill: str = None):
        """Comando usado pra encantar suas habilidades no rpg da Ashley
        Use ash enchant add numero_da_skill"""
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        if not update['rpg']['active']:
            embed = discord.Embed(
                color=self.bot.color,
                description='<:negate:721581573396496464>│``USE O COMANDO`` **ASH RPG** ``ANTES!``')
            return await ctx.send(embed=embed)

        if update['config']['battle']:
            msg = '<:negate:721581573396496464>│``VOCE ESTÁ BATALHANDO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if skill is None:
            msg = '<:negate:721581573396496464>│``VOCE PRECISA DIZER UMA SKILL PARA ENCANTAR``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        try:
            if 0 < int(skill) < 6:
                pass
            else:
                msg = '<:negate:721581573396496464>│``SKILL INVALIDA!``'
                embed = discord.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)
        except ValueError:
            msg = '<:negate:721581573396496464>│``SKILL INVALIDA!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        try:
            if update['inventory']['angel_stone'] >= 1:
                pass
            else:
                msg = '<:negate:721581573396496464>│``VOCE NÃO TEM ANGEL STONE!``'
                embed = discord.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)
        except KeyError:
            msg = '<:negate:721581573396496464>│``VOCE NÃO TEM ANGEL STONE!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if update['rpg']['skills'][int(skill) - 1] == limit:
            msg = '<:negate:721581573396496464>│``ESSA SKILL JA ATINGIU O ENCANTAMENTO MAXIMO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            return await ctx.send(embed=embed)

        if update['rpg']['skills'][int(skill) - 1] >= 10:
            try:
                if update['inventory']['angel_wing'] >= 1:
                    update['inventory']['angel_wing'] -= 1
                else:
                    msg = '<:negate:721581573396496464>│``VOCE NÃO TEM ANGEL WING, A PARTIR DO ENCANTAMENTO +10 VOCE ' \
                          'PRECISA DE 1 ANGEL STONE E 1 ANGEL WING!``'
                    embed = discord.Embed(color=self.bot.color, description=msg)
                    return await ctx.send(embed=embed)
            except KeyError:
                msg = '<:negate:721581573396496464>│``VOCE NÃO TEM ANGEL WING, A PARTIR DO ENCANTAMENTO +10 VOCE ' \
                      'PRECISA DE 1 ANGEL STONE E 1 ANGEL WING!``'
                embed = discord.Embed(color=self.bot.color, description=msg)
                return await ctx.send(embed=embed)

        update['inventory']['angel_stone'] -= 1
        await self.bot.db.update_data(data, update, 'users')
        data = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update = data

        self.up_chance = 0
        self.up_chance = self.chance_skill[skill][update['rpg']['skills'][int(skill) - 1]]
        chance = randint(1, 100)

        if chance < self.up_chance:
            update['rpg']['skills'][int(skill) - 1] += 1
            await self.bot.db.update_data(data, update, "users")

            msg = f"<:confirmed:721581574461587496>│🎊 **PARABENS** 🎉 {ctx.author.mention} ``SEU ENCATAMENTO PASSOU " \
                  f"PARA`` **+{update['rpg']['skills'][int(skill) - 1]}**"
            embed = discord.Embed(color=self.bot.color, description=msg)
            await ctx.send(embed=embed)

        elif chance == self.up_chance:
            msg = f'<:negate:721581573396496464>│{ctx.author.mention} ``SEU ENCATAMENTO FALHOU, MAS VOCE NAO REGREDIU' \
                  f' O SEU ENCANTAMENTO!``'
            embed = discord.Embed(color=self.bot.color, description=msg)
            await ctx.send(embed=embed)

        else:
            update['rpg']['skills'][int(skill) - 1] -= 1
            if update['rpg']['skills'][int(skill) - 1] < 0:
                update['rpg']['skills'][int(skill) - 1] = 0
            await self.bot.db.update_data(data, update, "users")

            msg = f'<:negate:721581573396496464>│{ctx.author.mention} ``SEU ENCATAMENTO QUEBROU, POR CONTA DISSO ' \
                  f'SEU ENCANTAMENTO REGREDIU PARA`` **+{update["rpg"]["skills"][int(skill) - 1]}**'
            embed = discord.Embed(color=self.bot.color, description=msg)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(EnchanterClass(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mENCHANTER\033[1;32m foi carregado com sucesso!\33[m')
