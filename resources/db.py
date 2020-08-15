import json
import discord
import datetime
import operator

from random import randint
from collections import Counter
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient as Client
from resources.utility import parse_duration, quant_etherny
from resources.structure import user_data_structure, guild_data_structure

with open("data/auth.json") as auth:
    _auth = json.loads(auth.read())

with open("data/config.json") as config:
    config = json.loads(config.read())

epoch = datetime.datetime.utcfromtimestamp(0)
cont = Counter()


class Database(object):
    def __init__(self, bot):
        self.bot = bot
        self._connect = Client(_auth['db_url'] + "?retryWrites=false", connectTimeoutMS=30000)
        self._database = self._connect[_auth['db_name']]

    # nao deve ser usado em comandos
    async def collection_data(self, db_name):
        return self._database[db_name]

    async def push_data(self, data, db_name):
        db = self._database[db_name]
        await db.insert_one(data)

    async def delete_data(self, data, db_name):
        db = self._database[db_name]
        await db.delete_one(data)

    async def update_data(self, data, update, db_name):
        db = self._database[db_name]
        await db.update_one({'_id': data['_id']}, {
            '$set': update,
        }, upsert=False)

    async def update_all_data(self, search, update, db_name):
        db = self._database[db_name]
        await db.update_many(search, {'$set': update})

    async def get_data(self, key, value, db_name):
        db = self._database[db_name]
        data = await db.find_one({key: value})
        if data is None:
            return None
        else:
            return data

    async def get_all_data(self, db_name):
        db = self._database[db_name]
        all_data = [data async for data in db.find()]
        return all_data

    async def update_all_db(self, db_users, db_guilds):
        all_users = await self.get_all_data("users")
        for data in all_users:
            update = data
            try:
                for k, v in db_users.items():
                    update[k] = v
                await self.update_data(data, update, "users")
            except KeyError:
                pass
        all_guilds = await self.get_all_data("guilds")
        for data in all_guilds:
            update = data
            try:
                for k, v in db_guilds.items():
                    update[k] = v
                await self.update_data(data, update, "guilds")
            except KeyError:
                pass

    async def get_announcements(self):
        db = self._database["announcements"]
        all_data = [data async for data in db.find()]
        return all_data

    # ----------------------------------- ============================ -----------------------------------
    #                               ITERAÇÕES DIRETAS COM O BANCO DE DADOS
    # ---------------------------------- ============================ -----------------------------------

    async def add_user(self, ctx):

        if await self.get_data("user_id", ctx.author.id, "users") is None:
            data = user_data_structure
            data["_id"] = ctx.author.id
            data["user_id"] = ctx.author.id
            data["guild_id"] = ctx.guild.id
            await self.push_data(data, "users")

    async def add_guild(self, guild, data):
        _data = guild_data_structure
        _data['_id'] = guild.id
        _data['guild_id'] = guild.id

        _data['log_config']['log'] = data.get("log", False)
        _data['log_config']['log_channel_id'] = data.get("log_channel_id", None)

        _data['ia_config']["auto_msg"] = data.get("auto_msg", False)

        _data['bot_config']["ash_news"] = data.get("ash_news", False)
        _data['bot_config']["ash_news_id"] = data.get("ash_news_id", None)
        _data['bot_config']["ash_git"] = data.get("ash_git", False)
        _data['bot_config']["ash_git_id"] = data.get("ash_git_id", None)
        _data['bot_config']["ash_draw"] = data.get("ash_draw", False)
        _data['bot_config']["ash_draw_id"] = data.get("ash_draw_id", None)

        _data['func_config']["cont_users"] = data.get("cont_users", False)
        _data['func_config']["cont_users_id"] = data.get("cont_users_id", None)
        _data['func_config']["member_join"] = data.get("member_join", False)
        _data['func_config']["member_join_id"] = data.get("member_join_id", None)
        _data['func_config']["member_remove"] = data.get("member_remove", False)
        _data['func_config']["member_remove_id"] = data.get("member_remove_id", None)

        if await self.get_data("guild_id", guild.id, "guilds") is None:
            await self.push_data(_data, "guilds")

    async def take_money(self, ctx, amount: int = 0):
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_user['treasure']['money'] -= amount
        update_guild_native['data']['total_money'] -= amount
        await self.bot.db.update_data(data_user, update_user, 'users')
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
        return f"<:confirmed:721581574461587496>│**{amount}** ``DE`` **Ethernyas** ``RETIRADOS COM SUCESSO!``"

    async def give_money(self, ctx, amount: int = 0):
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_user['treasure']['money'] += amount
        update_guild_native['data']['total_money'] += amount
        await self.bot.db.update_data(data_user, update_user, 'users')
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
        return f"<:confirmed:721581574461587496>│**{amount}** ``DE`` **Ethernyas** ``ADICIONADOS COM SUCESSO!``"

    async def add_money(self, ctx, amount, ext=False):

        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        change = randint(1, 100)
        msg = None
        answer = quant_etherny(amount)

        if not data_user['security']['status']:
            return '``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**'

        if data_user is not None:
            if update_user['user']['ranking'] == 'Bronze':
                await self.add_type(ctx, (answer['amount'] * 1), answer['list'])

                a = '{:,.2f}'.format(float(answer['amount']))
                b = a.replace(',', 'v')
                c = b.replace('.', ',')
                d = c.replace('v', '.')

                msg = f"**R${d}** de ``Ethernyas``"
            elif update_user['user']['ranking'] == 'Silver':
                if change <= 75:
                    await self.add_type(ctx, (answer['amount'] * 1), answer['list'])

                    a = '{:,.2f}'.format(float(answer['amount']))
                    b = a.replace(',', 'v')
                    c = b.replace('.', ',')
                    d = c.replace('v', '.')

                    msg = f"**R${d}** de ``Ethernyas``"
                else:
                    answer['list'][0] = (answer['list'][0] * 2)
                    answer['list'][1] = (answer['list'][1] * 2)
                    answer['list'][2] = (answer['list'][2] * 2)
                    await self.add_type(ctx, (answer['amount'] * 2), answer['list'])

                    a = '{:,.2f}'.format(float(answer['amount'] * 2))
                    b = a.replace(',', 'v')
                    c = b.replace('.', ',')
                    d = c.replace('v', '.')

                    msg = f"**R${d}** de ``Ethernyas``"
            elif update_user['user']['ranking'] == 'Gold':
                if change <= 75:
                    await self.add_type(ctx, (answer['amount'] * 1), answer['list'])

                    a = '{:,.2f}'.format(float(answer['amount']))
                    b = a.replace(',', 'v')
                    c = b.replace('.', ',')
                    d = c.replace('v', '.')

                    msg = f"**R${d}** de ``Ethernyas``"
                elif change <= 95:
                    answer['list'][0] = (answer['list'][0] * 2)
                    answer['list'][1] = (answer['list'][1] * 2)
                    answer['list'][2] = (answer['list'][2] * 2)
                    await self.add_type(ctx, (answer['amount'] * 2), answer['list'])

                    a = '{:,.2f}'.format(float(answer['amount'] * 2))
                    b = a.replace(',', 'v')
                    c = b.replace('.', ',')
                    d = c.replace('v', '.')

                    msg = f"**R${d}** de ``Ethernyas``"
                else:
                    answer['list'][0] = (answer['list'][0] * 3)
                    answer['list'][1] = (answer['list'][1] * 3)
                    answer['list'][2] = (answer['list'][2] * 3)
                    await self.add_type(ctx, (answer['amount'] * 3), answer['list'])

                    a = '{:,.2f}'.format(float(answer['amount'] * 3))
                    b = a.replace(',', 'v')
                    c = b.replace('.', ',')
                    d = c.replace('v', '.')

                    msg = f"**R${d}** de ``Ethernyas``"
            if ext:
                msg += f"\n``e a quantidade de pedras abaixo:`` " \
                       f"**{answer['list'][0]}**  {self.bot.money[0]} | " \
                       f"**{answer['list'][1]}**  {self.bot.money[1]} | " \
                       f"**{answer['list'][2]}**  {self.bot.money[2]}\n"
            return msg

    async def add_reward(self, ctx, list_):
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user

        if not data_user['security']['status']:
            return '``USUARIO DE MACRO / OU USANDO COMANDOS RAPIDO DEMAIS`` **USE COMANDOS COM MAIS CALMA JOVEM...**'

        response = '``Caiu pra você:`` \n'
        for item in list_:
            amount = randint(1, 3)
            try:
                update_user['inventory'][item] += amount
            except KeyError:
                update_user['inventory'][item] = amount
            response += f"{self.bot.items[item][0]} ``{amount}`` ``{self.bot.items[item][1]}``\n"
        await self.bot.db.update_data(data_user, update_user, 'users')
        response += '```dê uma olhada no seu inventario com o comando: "ash i"```'
        return response

    async def add_type(self, ctx, amount, ethernya):
        # DATA DO MEMBRO
        data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        update_user['treasure']['bronze'] += ethernya[0] * 2
        update_user['treasure']['silver'] += ethernya[1] * 2
        update_user['treasure']['gold'] += ethernya[2] * 2
        update_user['treasure']['money'] += amount * 2
        await self.bot.db.update_data(data_user, update_user, 'users')

        # DATA NATIVA DO SERVIDOR
        data_guild_native = await self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native['data']['total_bronze'] += ethernya[0] * 2
        update_guild_native['data']['total_silver'] += ethernya[1] * 2
        update_guild_native['data']['total_gold'] += ethernya[2] * 2
        update_guild_native['data']['total_money'] += amount * 2
        await self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')

        # DATA DO SERVIDOR ATUAL
        data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_guild = data_guild
        update_guild['treasure']['total_bronze'] += ethernya[0]
        update_guild['treasure']['total_silver'] += ethernya[1]
        update_guild['treasure']['total_gold'] += ethernya[2]
        update_guild['treasure']['total_money'] += amount
        await self.bot.db.update_data(data_guild, update_guild, 'guilds')

    async def is_registered(self, ctx, **kwargs):

        if ctx.message.webhook_id is not None:
            return True

        if ctx.guild is not None:
            data_guild = await self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            data_user = await self.bot.db.get_data("user_id", ctx.author.id, "users")

            update_user = data_user

            if data_guild is None:
                raise commands.CheckFailure('<:alert:739251822920728708>│``Sua guilda ainda não está registrada, por '
                                            'favor digite:`` **ash register guild** ``para cadastrar sua guilda '
                                            'no meu`` **banco de dados!**')

            if data_user is not None:
                try:
                    if kwargs.get("cooldown"):
                        time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() \
                                    - update_user["cooldown"][str(ctx.command)]
                        time_left = kwargs.get("time") - time_diff
                        if time_diff < kwargs.get("time"):
                            raise commands.CheckFailure(f'<:alert:739251822920728708>│**Aguarde**: `Você deve '
                                                        f'esperar` **{{}}** `para usar esse comando '
                                                        f'novamente!`'.format(parse_duration(int(time_left))))

                        if self.bot.guilds_commands[ctx.guild.id] > 50 and str(ctx.command) == "daily work" or \
                                str(ctx.command) != "daily work":
                            update_user['cooldown'][str(ctx.command)] = (datetime.datetime.utcnow()
                                                                         - epoch).total_seconds()
                except KeyError:
                    if self.bot.guilds_commands[ctx.guild.id] > 50 and str(ctx.command) == "daily work" or \
                            str(ctx.command) != "daily work":
                        try:
                            update_user['cooldown'][str(ctx.command)] = (datetime.datetime.utcnow()
                                                                         - epoch).total_seconds()
                        except KeyError:
                            update_user['cooldown'] = {str(ctx.command): (datetime.datetime.utcnow() -
                                                                          epoch).total_seconds()}

                if self.bot.guilds_commands[ctx.guild.id] > 50 and str(ctx.command) == "daily work" or \
                        str(ctx.command) != "daily work":
                    await self.bot.db.update_data(data_user, update_user, 'users')

                if kwargs.get("g_vip") and data_guild['vip']:
                    if kwargs.get("vip") and data_user['config']['vip']:
                        return True
                    elif kwargs.get("vip") and data_user['config']['vip'] is False:
                        if ctx.guild.id == 519894833783898112:
                            raise commands.CheckFailure("<:alert:739251822920728708>│``APENAS USUARIOS COM VIP ATIVO "
                                                        "PODEM USAR ESSE COMANDO``\n **Para ganhar seu vip diário use "
                                                        "ASH INVITE**")
                    return True
                elif kwargs.get("g_vip") and data_guild['vip'] is False:
                    raise commands.CheckFailure("<:alert:739251822920728708>│``APENAS SERVIDORES COM VIP ATIVO PODEM "
                                                "USAR ESSE COMANDO``\n **Para ganhar seu vip ATIVO DE SERVIDOR, O LIDER"
                                                " DA GUILDA precisa alcançar pelo menos 10 das 20 estrelas de "
                                                "recomendação**\n **OBS:** ``para ganhar recomendação é necessário usar"
                                                " o comando`` **ash daily rec** ``na pessoa que você deseja "
                                                "recomendar``")

                if kwargs.get("vip") and data_user['config']['vip']:
                    return True
                elif kwargs.get("vip") and data_user['config']['vip'] is False:
                    if ctx.guild.id == 519894833783898112:
                        raise commands.CheckFailure("<:alert:739251822920728708>│``APENAS USUARIOS COM VIP ATIVO "
                                                    "PODEM USAR ESSE COMANDO``\n **Para ganhar seu vip diário use "
                                                    "ASH INVITE**")
                    raise commands.CheckFailure("<:alert:739251822920728708>│``APENAS USUARIOS COM VIP ATIVO PODEM "
                                                "USAR ESSE COMANDO``\n **Para ganhar seu vip diário use ASH INVITE "
                                                "entre no meu canal de suporte e use o comando ASH VIP**")

                return True
            else:
                raise commands.CheckFailure(f'<:alert:739251822920728708>│``Você ainda não está registrado, '
                                            f'por favor use`` **ash register**.')
        else:
            return True


class DataInteraction(object):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db

    async def get_language(self, guild: str):
        data = await self.db.get_data("guild_id", guild, "guilds")
        lang = data["data"].get("lang", "pt")
        return lang

    async def set_language(self, guild: str, language):
        data = await self.db.get_data("guild_id", guild, "guilds")
        update = data
        update['data'].__delitem__("lang")
        update["data"].__setitem__("lang", language)
        await self.db.update_data(data, update, "guilds")

    async def add_experience(self, message, exp):
        data = await self.db.get_data("user_id", message.author.id, "users")
        update = data

        if data is None:
            return

        if update["user"]['xp_time'] is None:
            update["user"]['xp_time'] = datetime.datetime.today()

        if (datetime.datetime.today() - update["user"]['xp_time']).seconds > 5:
            update['user']['experience'] += exp * update['user']['level']
            update["user"]['xp_time'] = datetime.datetime.today()

        if 10 < update['user']['level'] < 20 and update['user']['ranking'] is not None:
            if randint(1, 200) == 200 and update['user']['ranking'] == "Bronze":
                update['user']['ranking'] = "Silver"

                try:
                    update['inventory']['coins'] += 1000
                except KeyError:
                    update['inventory']['coins'] = 1000

                    await message.channel.send('🎊 **PARABENS** 🎉 {} ``você upou para o ranking`` **{}** '
                                               '``e ganhou a`` **chance** ``de garimpar mais ethernyas '
                                               'e`` **+1000** ``Fichas``'.format(message.author, "Silver"))

        elif 20 < update['user']['level'] < 30 and update['user']['ranking'] is not None:
            if randint(1, 200) == 200 and update['user']['ranking'] == "Silver":
                update['user']['ranking'] = "Gold"

                try:
                    update['inventory']['coins'] += 2000
                except KeyError:
                    update['inventory']['coins'] = 2000

                    await message.channel.send('🎊 **PARABENS** 🎉 {} ``você upou para o ranking`` **{}** ``e ganhou '
                                               'a`` **chance** ``de garimpar mais eternyas do que o ranking passado '
                                               'e`` **+2000** ``Fichas``'.format(message.author, "Gold"))

        experience = update['user']['experience']
        lvl_anterior = update['user']['level']
        lvl_now = int(experience ** 0.2)
        if lvl_anterior < lvl_now:
            update['user']['level'] = lvl_now

            try:
                update['inventory']['coins'] += 200
            except KeyError:
                update['inventory']['coins'] = 200

            await message.channel.send('🎊 **PARABENS** 🎉 {} ``você upou para o level`` **{}** ``e ganhou`` **+200** '
                                       '``Fichas``'.format(message.author, lvl_now))

        await self.db.update_data(data, update, "users")

    async def add_xp(self, ctx, exp):
        data = await self.db.get_data("user_id", ctx.author.id, "users")
        update = data

        update['rpg']['XP'] += exp
        experience = update['rpg']['XP']
        lvl_anterior = update['rpg']['Level']
        lvl_now = int(experience ** 0.2)
        if lvl_anterior < lvl_now:
            update['rpg']['Level'] = lvl_now
            update['rpg']['Status']['pdh'] += 1

            try:
                update['inventory']['coins'] += 200
            except KeyError:
                update['inventory']['coins'] = 200

            await ctx.send('🎊 **PARABENS** 🎉 {} ``você upou para o level`` **{},** ``ganhou`` **+200** '
                           '``Fichas e +1 PDH (olhe o comando \"ash skill\")``'.format(ctx.author.mention, lvl_now))

        await self.db.update_data(data, update, "users")

    async def add_battle(self, ctx):
        data = await self.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data is not None:
            if ctx.author.id == data["user_id"]:
                update['config']['battle'] = True
                update['config']['provinces'] = str(ctx.channel)
                await self.db.update_data(data, update, "users")

    async def remove_battle(self, ctx):
        data = await self.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data is not None:
            if ctx.author.id == data["user_id"]:
                update['config']['battle'] = False
                update['config']['provinces'] = None
                await self.db.update_data(data, update, "users")

    async def add_announcement(self, ctx, announce):
        date = datetime.datetime(*datetime.datetime.utcnow().timetuple()[:6])
        data = {
            "_id": ctx.author.id,
            "data": {
                "status": False,
                "announce": announce,
                "date": "{}".format(date)
            }
        }
        await self.db.push_data(data, "announcements")
        await ctx.send('<:confirmed:721581574461587496>│``Anuncio cadastrado com sucesso!``\n```AGUARDE APROVAÇÃO```')
        pending = self.bot.get_channel(619969149791240211)
        msg = f"{ctx.author.id}: **{ctx.author.name}** ``ADICIONOU UM NOVO ANUNCIO PARA APROVAÇÃO!``"
        await pending.send(msg)

    async def get_rank_xp(self, limit):
        global cont
        data = await self.db.get_all_data("users")
        dict_ = dict()
        for _ in data:
            dict_[str(_.get('user_id'))] = _['user'].get('experience')
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        cont['list'] = 0

        def money_(money):
            a = '{:,.0f}'.format(float(money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            return d

        def counter():
            cont['list'] += 1
            return cont['list']

        rank = "\n".join([str(counter()) + "º: " +
                          str(await self.bot.fetch_user(int(sorted_x[x][0]))).replace("'", "").replace("#", "_") +
                          " > " + str(money_(sorted_x[x][1])) for x in range(limit)])
        return rank

    async def get_rank_level(self, limit):
        global cont
        data = await self.db.get_all_data("users")
        dict_ = dict()
        for _ in data:
            dict_[str(_.get('user_id'))] = _['user'].get('level')
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        cont['list'] = 0

        def money_(money):
            a = '{:,.0f}'.format(float(money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            return d

        def counter():
            cont['list'] += 1
            return cont['list']

        rank = "\n".join([str(counter()) + "º: " +
                          str(await self.bot.fetch_user(int(sorted_x[x][0]))).replace("'", "").replace("#", "_") +
                          " > " + str(money_(sorted_x[x][1])) for x in range(limit)])
        return rank

    async def get_rank_money(self, limit):
        global cont
        data = await self.db.get_all_data("users")
        dict_ = dict()
        for _ in data:
            dict_[str(_.get('user_id'))] = _['treasure'].get('money')
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        cont['list'] = 0

        def money_(money):
            a = '{:,.2f}'.format(float(money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            return d

        def counter():
            global cont
            cont['list'] += 1
            return cont['list']

        rank = "\n".join([str(counter()) + "º: " +
                          str(await self.bot.fetch_user(int(sorted_x[x][0]))).replace("'", "").replace("#", "_") +
                          " > R$ " + str(money_(sorted_x[x][1])) for x in range(limit)])
        return rank

    async def get_rank_gold(self, limit):
        global cont
        data = await self.db.get_all_data("users")
        dict_ = dict()
        for _ in data:
            dict_[str(_.get('user_id'))] = _['treasure'].get('gold')
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        cont['list'] = 0

        def money_(money):
            a = '{:,.0f}'.format(float(money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            return d

        def counter():
            cont['list'] += 1
            return cont['list']

        rank = "\n".join([str(counter()) + "º: " +
                          str(await self.bot.fetch_user(int(sorted_x[x][0]))).replace("'", "").replace("#", "_") +
                          " > " + str(money_(sorted_x[x][1])) for x in range(limit)])
        return rank

    async def get_rank_silver(self, limit):
        global cont
        data = await self.db.get_all_data("users")
        dict_ = dict()
        for _ in data:
            dict_[str(_.get('user_id'))] = _['treasure'].get('silver')
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        cont['list'] = 0

        def money_(money):
            a = '{:,.0f}'.format(float(money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            return d

        def counter():
            cont['list'] += 1
            return cont['list']

        rank = "\n".join([str(counter()) + "º: " +
                          str(await self.bot.fetch_user(int(sorted_x[x][0]))).replace("'", "").replace("#", "_") +
                          " > " + str(money_(sorted_x[x][1])) for x in range(limit)])
        return rank

    async def get_rank_bronze(self, limit):
        global cont
        data = await self.db.get_all_data("users")
        dict_ = dict()
        for _ in data:
            dict_[str(_.get('user_id'))] = _['treasure'].get('bronze')
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        cont['list'] = 0

        def money_(money):
            a = '{:,.0f}'.format(float(money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            return d

        def counter():
            cont['list'] += 1
            return cont['list']

        rank = "\n".join([str(counter()) + "º: " +
                          str(await self.bot.fetch_user(int(sorted_x[x][0]))).replace("'", "").replace("#", "_") +
                          " > " + str(money_(sorted_x[x][1])) for x in range(limit)])
        return rank

    async def get_rank_point(self, limit):
        global cont
        data = await self.db.get_all_data("users")
        dict_ = dict()
        for _ in data:
            if _['config'].get('points') is not None:
                dict_[str(_.get('user_id'))] = _['config'].get('points')
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        cont['list'] = 0

        def money_(money):
            a = '{:,.0f}'.format(float(money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            return d

        def counter():
            cont['list'] += 1
            return cont['list']

        rank = "\n".join([str(counter()) + "º: " +
                          str(await self.bot.fetch_user(int(sorted_x[x][0]))).replace("'", "").replace("#", "_") +
                          " > " + str(money_(sorted_x[x][1])) for x in range(limit)])
        return rank

    async def get_rank_commands(self, limit):
        global cont
        data = await self.db.get_all_data("users")
        dict_ = dict()
        for _ in data:
            dict_[str(_.get('user_id'))] = _['user'].get('commands', 0)
        sorted_x = sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)
        cont['list'] = 0

        def money_(money):
            a = '{:,.0f}'.format(float(money))
            b = a.replace(',', 'v')
            c = b.replace('.', ',')
            d = c.replace('v', '.')
            return d

        def counter():
            cont['list'] += 1
            return cont['list']

        rank = "\n".join([str(counter()) + "º: " +
                          str(await self.bot.fetch_user(int(sorted_x[x][0]))).replace("'", "").replace("#", "_") +
                          " > " + str(money_(sorted_x[x][1])) for x in range(limit)])
        return rank

    async def add_vip(self, **kwargs):
        if kwargs.get("target") == "users":
            data = await self.db.get_data("user_id", kwargs.get("user_id"), "users")
            update = data
            if kwargs.get("state"):
                update['config']['vip'] = True
            else:
                update['config']['vip'] = False
            await self.db.update_data(data, update, "users")
        elif kwargs.get("target") == "guilds":
            data = await self.db.get_data("guild_id", kwargs.get("guild_id"), "guilds")
            update = data
            if kwargs.get("state"):
                update['vip'] = True
            else:
                update['vip'] = False
            await self.db.update_data(data, update, "guilds")
