import json
import discord
import datetime
import pymongo

from resources.translation import t_
from discord.ext import commands
from pymongo import MongoClient
from random import randint

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

epoch = datetime.datetime.utcfromtimestamp(0)


class Database(object):
    def __init__(self, bot):
        self.bot = bot
        self._data_brute = MongoClient(_auth['db_url'], connectTimeoutMS=30000)
        self._conn = self._data_brute.get_database(_auth['db_name'])

    def push_data(self, data, db_name):
        db = self._conn.get_collection(db_name)
        db.insert_one(data)

    def update_data(self, data, update, db_name):
        db = self._conn.get_collection(db_name)
        db.update_one({'_id': data['_id']}, {
            '$set': update
        }, upsert=False)

    def update_all_data(self, search, update, db_name):
        db = self._conn.get_collection(db_name)
        db.update_many(search, {'$set': update})

    def get_data(self, key, value, db_name):
        db = self._conn.get_collection(db_name)
        data = db.find_one({key: value})
        if data is None:
            return None
        else:
            return data

    def get_all_data(self, db_name):
        db = self._conn.get_collection(db_name)
        data = db.find()
        return data

    def get_announcements(self):
        db = self._conn.get_collection("announcements")
        return db.find()

    def get_channel_data(self, channel_id):
        db = self._conn.get_collection("channels")
        data = db.find_one({"channel_id": channel_id})
        if data is None:
            data = {"channel_id": channel_id,
                    "channel_state": 0}
            self.push_data(data, "channels")
            return data
        else:
            return data

    def delete_channels(self):
        db = self._conn.get_collection("channels")
        deleted = db.delete_many({})
        print("\033[1;31m", deleted.deleted_count, " \033[1;30mregistros de canais bloqueados pela IA deletados.\33[m")

    def add_user(self, ctx, **data):
        db_name = data.get("db_name", "users")
        data = {
            "user_id": ctx.author.id,
            "user_name": ctx.author.name,
            "guild_id": ctx.guild.id,
            "guild_name": ctx.guild.name,
            "guild_icon_url": ctx.guild.icon_url,
            "config": {
                "tournament": False,
                "playing": False,
                "battle": False,
                "provinces": None,
                "vip": False,
                "vip_class": None,
                "roles": [],
                "points": 0
            },
            "user": {
                "experience": 0,
                "level": 1,
                "ranking": "Bronze",
                "titling": None,
                "background": data.get("background", None),
                "married": False,
                "winner": 0,
            },
            "status": {
                "STR": 1,
                "CON": 1,
                "DEX": 1,
                "INT": 1,
                "LUC": 1,
                "PDH": 0,
                "rpg_class": data.get("rpg_class", None),
                "attribute_class": 1
            },
            "treasure": {
                "money": 0,
                "gold": 0,
                "silver": 0,
                "bronze": 0
            },
            "inventory": {
                "medal": 0,
                "rank_point": 0,
                "coins": 10
            },
            "royal": {
                "royal": data.get("royal", False),
                "victories": 0,
                "defeats": 0,
                "draws": 0,
                "points": 0,
                "team": "default",
                "deck": "common",
                "matches": 0
            },
            "cup": {
                "cup": data.get("cup", False),
                "victories": 0,
                "defeats": 0,
                "draws": 0,
                "points": 0,
                "team": "default",
                "deck": "common",
                "matches": 0
            },
            "cooldown": {}
        }
        if self.get_data("user_id", ctx.author.id, db_name) is None:
            self.push_data(data, db_name)

    def add_guild(self, guild, data):
        if guild.owner.name is None:
            owner_name = 'Não Identificado'
            owner_id = 0
        else:
            owner_name = guild.owner.name
            owner_id = guild.owner.id
        db_name = data.get("db_name", "guilds")
        new_data = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "guild_owner_id": owner_id,
            "guild_owner_name": owner_name,
            "vip": False,
            "data": {
                "lang": "pt",
                "ranking": "Bronze",
                "items": dict(),
                "accounts": 0,
                "currency": _auth['default_money'],
                "total_money": 0,
                "total_gold": 0,
                "total_silver": 0,
                "total_bronze": 0,
            },
            "treasure": {
                "total_money": 0,
                "total_gold": 0,
                "total_silver": 0,
                "total_bronze": 0
            },
            "log_config": {
                "log": data.get("log", False),
                "log_channel_id": data.get("log_channel_id", None),
                "msg_delete": data.get("msg_delete", True),
                "msg_edit": data.get("msg_edit", True),
                "channel_edit_topic": data.get("channel_edit_topic", False),
                "channel_edit_name": data.get("channel_edit_name", False),
                "channel_created": data.get("channel_created", False),
                "channel_deleted": data.get("channel_deleted", False),
                "member_edit_avatar": data.get("member_edit_avatar", False),
                "member_edit_nickname": data.get("member_edit_nickname", False),
                "member_voice_entered": data.get("member_voice_entered", False),
                "member_voice_exit": data.get("member_voice_exit", False),
                "member_ban": data.get("member_ban", False),
                "member_unBan": data.get("member_unBan", False),
                "member_kick": data.get("member_kick", False),
                "emoji_update": data.get("emoji_update", False)
            },
            "ia_config": {
                "auto_msg": data.get("auto_msg", False),
                "auto_conversation": data.get("auto_conversation", False),
                "help_system": data.get("help_system", False)
            },
            "rpg_config": {
                "rpg": data.get("rpg", False),
                "announcement": data.get("announcement", False),
                "announcement_id": data.get("announcement_id", None),
                "chat_farm": data.get("chat_farm", False),
                "chat_farm_id": data.get("chat_farm_id", None),
                "chat_battle": data.get("chat_battle", False),
                "chat_battle_id": data.get("chat_battle_id", None),
                "chat_pvp": data.get("chat_pvp", False),
                "chat_pvp_id": data.get("chat_pvp_id", None)
            },
            "bot_config": {
                "ash_news": data.get("ash_news", False),
                "ash_news_id": data.get("log", None),
                "ash_git": data.get("ash_news_id", False),
                "ash_git_id": data.get("ash_git_id", None)
            },
            "func_config": {
                "cont_users": data.get("cont_users", False),
                "cont_users_id": data.get("cont_users_id", None),
                "member_join": data.get("member_join", False),
                "member_join_id": data.get("member_join_id", None),
                "member_remove": data.get("member_remove", False),
                "member_remove_id": data.get("member_remove_id", None)
            },
            "warn_config": {
                "warn": data.get("warn", False),
                "warn_channel_id": data.get("warn_channel_id", None),
                "bad_word": data.get("bad_word", False)
            },
            "royal_config": {
                "royal": data.get("royal", False),
                "members": [],
                "victories": 0,
                "defeats": 0,
                "draws": 0,
                "points": 0
            },
            "cup_config": {
                "cup": data.get("cup", False),
                "members": [],
                "victories": 0,
                "defeats": 0,
                "draws": 0,
                "points": 0
            }
        }
        if self.get_data("guild_id", guild.id, db_name) is None:
            self.push_data(new_data, db_name)

    async def take_money(self, ctx, coin, amount: int = 0):
        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        data_guild_native = self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        if coin == "bronze":
            update_user['treasure'][coin] -= amount
            update_guild_native['data']['total_' + str(coin)] -= amount
            self.bot.db.update_data(data_user, update_user, 'users')
            self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            return f"<:confirmado:519896822072999937>│**{amount}** ``DE`` **{coin}** ``RETIRADOS COM SUCESSO!``"
        elif coin == "silver":
            update_user['treasure'][coin] -= amount
            update_guild_native['data']['total_' + str(coin)] -= amount
            self.bot.db.update_data(data_user, update_user, 'users')
            self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            return f"<:confirmado:519896822072999937>│**{amount}** ``DE`` **{coin}** ``RETIRADOS COM SUCESSO!``"
        elif coin == "gold":
            update_user['treasure'][coin] -= amount
            update_guild_native['data']['total_' + str(coin)] -= amount
            self.bot.db.update_data(data_user, update_user, 'users')
            self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            return f"<:confirmado:519896822072999937>│**{amount}** ``DE`` **{coin}** ``RETIRADOS COM SUCESSO!``"
        else:
            return "<:alert_status:519896811192844288>│``OPÇÃO DE MOEDA ERRADA... ESCOLHA ENTRE:`` **gold**, " \
                   "**silver** ``OU`` **gold**"

    async def give_money(self, ctx, coin, amount):
        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        data_guild_native = self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        if coin == "bronze":
            update_user['treasure'][coin] += amount
            update_guild_native['data']['total_' + str(coin)] += amount
            self.bot.db.update_data(data_user, update_user, 'users')
            self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            return f"<:confirmado:519896822072999937>│**{amount}** ``DE`` **{coin}** ``ADICIONADOS COM SUCESSO!``"
        elif coin == "silver":
            update_user['treasure'][coin] += amount
            update_guild_native['data']['total_' + str(coin)] += amount
            self.bot.db.update_data(data_user, update_user, 'users')
            self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            return f"<:confirmado:519896822072999937>│**{amount}** ``DE`` **{coin}** ``ADICIONADOS COM SUCESSO!``"
        elif coin == "gold":
            update_user['treasure'][coin] += amount
            update_guild_native['data']['total_' + str(coin)] += amount
            self.bot.db.update_data(data_user, update_user, 'users')
            self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')
            return f"<:confirmado:519896822072999937>│**{amount}** ``DE`` **{coin}** ``ADICIONADOS COM SUCESSO!``"
        else:
            return "<:alert_status:519896811192844288>│``OPÇÃO DE MOEDA ERRADA... ESCOLHA ENTRE:`` **gold**, " \
                   "**silver** ``OU`` **gold**"

    async def add_money(self, ctx, amount):

        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        change = randint(1, 100)

        if data_user is not None:
            if update_user['user']['ranking'] == 'Bronze':
                await self.add_bronze(ctx, amount)
            elif update_user['user']['ranking'] == 'Silver':
                if change <= 50:
                    await self.add_bronze(ctx, amount)
                else:
                    await self.add_bronze(ctx, amount)
                    await self.add_silver(ctx, amount)
            elif update_user['user']['ranking'] == 'Gold':
                if change <= 33:
                    await self.add_bronze(ctx, amount)
                elif change <= 66:
                    await self.add_bronze(ctx, amount)
                    await self.add_silver(ctx, amount)
                else:
                    await self.add_bronze(ctx, amount)
                    await self.add_silver(ctx, amount)
                    await self.add_gold(ctx, amount)

    async def add_bronze(self, ctx, amount):
        # DATA DO MEMBRO
        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        update_user['treasure']['bronze'] += amount
        total = 1 * update_user['treasure']['bronze']
        total += 10 * update_user['treasure']['silver']
        total += 100 * update_user['treasure']['gold']
        update_user['treasure']['money'] = total
        self.bot.db.update_data(data_user, update_user, 'users')

        # DATA NATIVA DO SERVIDOR
        data_guild_native = self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native['data']['total_bronze'] += amount
        total = 1 * update_guild_native['data']['total_bronze']
        total += 10 * update_guild_native['data']['total_silver']
        total += 100 * update_guild_native['data']['total_gold']
        update_guild_native['data']['total_money'] = total
        self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')

        # DATA DO SERVIDOR
        data_guild = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_guild = data_guild
        update_guild['treasure']['total_bronze'] += amount // 2
        total = 1 * update_guild['treasure']['total_bronze']
        total += 10 * update_guild['treasure']['total_silver']
        total += 100 * update_guild['treasure']['total_gold']
        update_guild['treasure']['total_money'] = total
        self.bot.db.update_data(data_guild, update_guild, 'guilds')

    async def add_silver(self, ctx, amount):
        # DATA DO MEMBRO
        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        update_user['treasure']['silver'] += amount
        total = 1 * update_user['treasure']['bronze']
        total += 10 * update_user['treasure']['silver']
        total += 100 * update_user['treasure']['gold']
        update_user['treasure']['money'] = total
        self.bot.db.update_data(data_user, update_user, 'users')

        # DATA NATIVA DO SERVIDOR
        data_guild_native = self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native['data']['total_silver'] += amount
        total = 1 * update_guild_native['data']['total_bronze']
        total += 10 * update_guild_native['data']['total_silver']
        total += 100 * update_guild_native['data']['total_gold']
        update_guild_native['data']['total_money'] = total
        self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')

        # DATA DO SERVIDOR
        data_guild = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_guild = data_guild
        update_guild['treasure']['total_silver'] += amount // 2
        total = 1 * update_guild['treasure']['total_bronze']
        total += 10 * update_guild['treasure']['total_silver']
        total += 100 * update_guild['treasure']['total_gold']
        update_guild['treasure']['total_money'] = total
        self.bot.db.update_data(data_guild, update_guild, 'guilds')

    async def add_gold(self, ctx, amount):
        # DATA DO MEMBRO
        data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")
        update_user = data_user
        update_user['treasure']['gold'] += amount
        total = 1 * update_user['treasure']['bronze']
        total += 10 * update_user['treasure']['silver']
        total += 100 * update_user['treasure']['gold']
        update_user['treasure']['money'] = total
        self.bot.db.update_data(data_user, update_user, 'users')

        # DATA NATIVA DO SERVIDOR
        data_guild_native = self.bot.db.get_data("guild_id", data_user['guild_id'], "guilds")
        update_guild_native = data_guild_native
        update_guild_native['data']['total_gold'] += amount
        total = 1 * update_guild_native['data']['total_bronze']
        total += 10 * update_guild_native['data']['total_silver']
        total += 100 * update_guild_native['data']['total_gold']
        update_guild_native['data']['total_money'] = total
        self.bot.db.update_data(data_guild_native, update_guild_native, 'guilds')

        # DATA DO SERVIDOR
        data_guild = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
        update_guild = data_guild
        update_guild['treasure']['total_gold'] += amount // 2
        total = 1 * update_guild['treasure']['total_bronze']
        total += 10 * update_guild['treasure']['total_silver']
        total += 100 * update_guild['treasure']['total_gold']
        update_guild['treasure']['total_money'] = total
        self.bot.db.update_data(data_guild, update_guild, 'guilds')

    async def is_registered(self, ctx, **kwargs):
        if ctx.guild is not None:
            data_guild = self.bot.db.get_data("guild_id", ctx.guild.id, "guilds")
            data_user = self.bot.db.get_data("user_id", ctx.author.id, "users")

            update_user = data_user

            if data_guild is None:
                raise commands.CheckFailure('<:negate:520418505993093130>│``Sua guilda ainda não está registrada, por '
                                            'favor digite:`` **ash register guild** ``para cadastrar sua guilda '
                                            'no meu`` **banco de dados!**')

            if data_user is not None:
                try:
                    if kwargs.get("cooldown"):
                        time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - \
                                    update_user["cooldown"][str(ctx.command)]

                        if time_diff < kwargs.get("time"):
                            raise commands.CheckFailure(f'<:negate:520418505993093130>│**Aguarde**: `Você deve '
                                                        f'esperar` **{{:.2f}}** `horas para usar esse comando '
                                                        f'novamente!`'.format((kwargs.get("time") -
                                                                               time_diff) / 3600))
                        if self.bot.guilds_commands[ctx.guild.id] > 50 or str(ctx.command) != "daily work":
                            update_user['cooldown'][str(ctx.command)] = (datetime.datetime.utcnow()
                                                                         - epoch).total_seconds()
                except KeyError:
                    if self.bot.guilds_commands[ctx.guild.id] > 50 or str(ctx.command) != "daily work":
                        try:
                            update_user['cooldown'][str(ctx.command)] = (datetime.datetime.utcnow()
                                                                         - epoch).total_seconds()
                        except KeyError:
                            update_user['cooldown'] = {str(ctx.command): (datetime.datetime.utcnow() -
                                                                          epoch).total_seconds()}

                if self.bot.guilds_commands[ctx.guild.id] > 50 or str(ctx.command) != "daily work":
                    self.bot.db.update_data(data_user, update_user, 'users')

                if kwargs.get("vip") and data_guild['vip']:
                    return True
                elif kwargs.get("vip") and data_guild['vip'] is False:
                    raise commands.CheckFailure("<:negate:520418505993093130>│``APENAS GUILDS PARCEIRAS PODEM USAR "
                                                "ESSE COMANDO``")

                return True
            else:
                raise commands.CheckFailure(t_(ctx, f'<:negate:520418505993093130>│``Você ainda não está registrado, '
                                                    f'por favor use`` **ash registro** ``ou`` **ash register**.',
                                               "guilds"))
        else:
            return True


class DataInteraction(object):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db

    def get_language(self, guild: str):
        data = self.db.get_data("guild_id", guild, "guilds")
        lang = data["data"].get("lang", "pt")
        return lang

    def set_language(self, guild: str, language):
        data = self.db.get_data("guild_id", guild, "guilds")
        update = data
        update['data'].__delitem__("lang")
        update["data"].__setitem__("lang", language)
        self.db.update_data(data, update, "guilds")

    async def add_experience(self, message, exp):
        record = self.db.get_data("user_id", message.author.id, "users")
        update = record
        if record is not None:
            try:
                if message.author.id == record["user_id"]:
                    time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - record["user"]['xp_time']
                    if time_diff >= 60:
                        change = randint(1, 200)
                        if 10 < update['user']['level'] < 20 and update['user']['ranking'] is not None:
                            if change == 200 and update['user']['ranking'] == "Bronze":
                                update['user']['ranking'] = "Silver"
                                update['inventory']['coins'] += 20
                                if not message.guild.id == 425864977996578816:
                                    try:
                                        await message.channel.send(
                                            '🎊 **PARABENS** 🎉 {} ``você upou para o ranking`` **{}** ``e ganhou a``'
                                            ' **chance** ``de garimpar prata a partir de agora e`` **+20** ``Fichas '
                                            'para jogar``'.format(message.author, "Silver"))
                                    except discord.errors.Forbidden:
                                        pass
                        elif 20 < update['user']['level'] < 30 and update['user']['ranking'] is not None:
                            if change == 200 and update['user']['ranking'] == "Silver":
                                update['user']['ranking'] = "Gold"
                                update['inventory']['coins'] += 20
                                if not message.guild.id == 425864977996578816:
                                    try:
                                        await message.channel.send(
                                            '🎊 **PARABENS** 🎉 {} ``você upou para o ranking`` **{}** ``e ganhou a``'
                                            ' **chance** ``de garimpar ouro a partir de agora e`` **+20** ``Fichas para'
                                            ' jogar``'.format(message.author, "Gold"))
                                    except discord.errors.Forbidden:
                                        pass
                        update['user']['experience'] += exp * update['user']['level']
                        update["user"]['xp_time'] = (datetime.datetime.utcnow() - epoch).total_seconds()
                        self.db.update_data(record, update, "users")
            except KeyError:
                if message.author.id == record["user_id"]:
                    update["user"]['xp_time'] = (datetime.datetime.utcnow() - epoch).total_seconds()
                    self.db.update_data(record, update, "users")

    async def level_up(self, message):
        data = self.db.get_data("user_id", message.author.id, "users")
        update = data
        if data is not None:
            if message.author.id == data["user_id"]:
                experience = update['user']['experience']
                lvl_anterior = update['user']['level']
                lvl_now = int(experience ** (1 / 5))
                if lvl_anterior < lvl_now:
                    update['user']['level'] = lvl_now
                    update['status']['PDH'] += 1
                    update['inventory']['coins'] += 10
                    self.db.update_data(data, update, "users")
                    if not message.guild.id == 425864977996578816:
                        try:
                            await message.channel.send('🎊 **PARABENS** 🎉 {} ``você upou para o level`` **{}** ``e '
                                                       'ganhou`` **1** ``ponto de habilidade e`` **+10** ``Fichas para '
                                                       'jogar``'.format(message.author, lvl_now))
                        except discord.errors.Forbidden:
                            pass

    async def add_battle(self, ctx):
        data = self.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data is not None:
            if ctx.author.id == data["user_id"]:
                update['config']['battle'] = True
                update['config']['provinces'] = str(ctx.channel)
                self.db.update_data(data, update, "users")

    async def remove_battle(self, ctx):
        data = self.db.get_data("user_id", ctx.author.id, "users")
        update = data
        if data is not None:
            if ctx.author.id == data["user_id"]:
                update['config']['battle'] = False
                update['config']['provinces'] = None
                self.db.update_data(data, update, "users")

    async def add_announcement(self, ctx, announce):
        date = datetime.datetime(*datetime.datetime.utcnow().timetuple()[:6])
        data = {
            "user_id": ctx.author.id,
            "user_name": ctx.author.name,
            "data": {
                "announce": announce,
                "date": "{}".format(date)
            }
        }
        self.db.push_data(data, "announcements")
        await ctx.send('<:confirmado:519896822072999937>│``Anuncio cadastrado com sucesso!``')

    def get_rank_xp(self, limit):
        data = self.db.get_all_data("users")
        rank = "\n".join([str(self.bot.get_user(int(x.get("user_id")))).replace("'", "").replace("#", "_") +
                          ': ' + str(x['user'].get("experience")) for x
                          in data.limit(limit).sort("user", pymongo.DESCENDING)])
        return rank

    def get_rank_level(self, limit):
        data = self.db.get_all_data("users")
        rank = "\n".join([str(self.bot.get_user(int(x.get("user_id")))).replace("'", "").replace("#", "_") +
                          ': ' + str(x['user'].get("level")) for x
                          in data.limit(limit).sort("user", pymongo.DESCENDING)])
        return rank

    def get_rank_money(self, limit):
        data = self.db.get_all_data("users")
        rank = "\n".join([str(self.bot.get_user(int(x.get("user_id")))).replace("'", "").replace("#", "_") +
                          ': ' + str(x['treasure'].get("money")) for x
                          in data.limit(limit).sort("treasure", pymongo.DESCENDING)])
        return rank

    def get_rank_gold(self, limit):
        data = self.db.get_all_data("users")
        rank = "\n".join([str(self.bot.get_user(int(x.get("user_id")))).replace("'", "").replace("#", "_") +
                          ': ' + str(x['treasure'].get("gold")) for x
                          in data.limit(limit).sort("treasure", pymongo.DESCENDING)])
        return rank

    def get_rank_silver(self, limit):
        data = self.db.get_all_data("users")
        rank = "\n".join([str(self.bot.get_user(int(x.get("user_id")))).replace("'", "").replace("#", "_") +
                          ': ' + str(x['treasure'].get("silver")) for x
                          in data.limit(limit).sort("treasure", pymongo.DESCENDING)])
        return rank

    def get_rank_bronze(self, limit):
        data = self.db.get_all_data("users")
        rank = "\n".join([str(self.bot.get_user(int(x.get("user_id")))).replace("'", "").replace("#", "_") +
                          ': ' + str(x['treasure'].get("bronze")) for x
                          in data.limit(limit).sort("treasure", pymongo.DESCENDING)])
        return rank

    def get_rank_point(self, limit):
        data = self.db.get_all_data("users")
        rank = "\n".join([str(self.bot.get_user(int(x.get("user_id")))).replace("'", "").replace("#", "_") +
                          ': ' + str(x['config'].get("points")) for x
                          in data.limit(limit).sort("config", pymongo.DESCENDING)])
        return rank

    def add_vip(self, **kwargs):
        try:
            if kwargs.get("help", False):
                return "Keys: type (users or guilds), Key ID = (user_id or guild_id), state (1 or 0),"
            if kwargs.get("type") == "users":
                data = self.db.get_data("user_id", kwargs.get("user_id"), "users")
                update = data
                if kwargs.get("state", False):
                    update['config']['vip'] = True
                else:
                    update['config']['vip'] = False
                self.db.update_data(data, update, "users")
                return "ESTADO DE VIP ALTERADO COM SUCESSO"
            elif kwargs.get("type") == "guilds":
                data = self.db.get_data("guild_id", kwargs.get("guild_id"), "guilds")
                update = data
                if kwargs.get("state", False):
                    update['vip'] = True
                else:
                    update['vip'] = False
                self.db.update_data(data, update, "guilds")
                return "ESTADO DE VIP ALTERADO COM SUCESSO"
            else:
                return "Tipo Inexistente, use (type='guilds' or type='users')!"
        except KeyError:
            return "Você uma chave no dicionário, reveja todos os campos e tente novamente!"

    def add_field(self, **kwargs):
        try:
            if kwargs.get("help", False):
                return "Keys: type (users or guilds), two_key (true or false), key_1, key_2, content"
            if kwargs.get("type") == "users":
                all_data = self.bot.db.get_all_data("users")
                for data in all_data:
                    update = data
                    if kwargs.get("two_key", False):
                        update[kwargs.get("key_1")][kwargs.get("key_2")] = kwargs.get("content")
                    else:
                        update[kwargs.get("key_1")] = kwargs.get("content")
                    self.bot.db.update_data(data, update, "users")
            elif kwargs.get("type") == "guilds":
                all_data = self.bot.db.get_all_data("guilds")
                for data in all_data:
                    update = data
                    if kwargs.get("key_2", False):
                        update[kwargs.get("key_1")][kwargs.get("key_2")] = kwargs.get("content")
                    else:
                        update[kwargs.get("key_1")] = kwargs.get("content")
                    self.bot.db.update_data(data, update, "guilds")
            else:
                return "Tipo Inexistente, use (type='guilds' or type='users')!"
        except KeyError:
            return "Você uma chave no dicionário, reveja todos os campos e tente novamente!"
