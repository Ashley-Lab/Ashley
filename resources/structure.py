user_data_structure = {
            "user_id": None,
            "guild_id": None,
            "user": {
                "experience": 0,
                "level": 1,
                "ranking": "Bronze",
                "titling": "Vagabond",
                "married": False,
                "married_at": None,
                "marrieding": False,
                "about": "Mude seu about, usando o comando \"ash about <text>\"",
                "stars": 0,
                "rec": 0,
                "commands": 0,
                "ia_response": True,
                "achievements": list()
            },
            "treasure": {
                "money": 0,
                "gold": 0,
                "silver": 0,
                "bronze": 0
            },
            "config": {
                "playing": False,
                "battle": False,
                "provinces": None,
                "vip": False,
                "roles": [],
                "points": 0
            },
            "moderation": {
                "credibility": {"ashley": 100, "guilds": [{"id": 0, "points": 100}]},
                "warns": [{"status": False, "author": None, "reason": None, "date": None, "point": 0}],
                "behavior": {"guild_id": 0, "historic": {"input": [], "output": []}},
                "notes": [{"guild_id": 0, "author": None, "date": None, "note": None}]
            },
            "rpg": {
                "Name": None,
                "vip": False,
                "Level": 1,
                "XP": 0,
                "Status": {
                    "con": 5,
                    "prec": 5,
                    "agi": 5,
                    "atk": 5,
                    "luk": 0,
                    "pdh": 0
                },
                "Class": 'Default',
                "artifacts": dict(),
                "relics": dict(),
                "img": None,
            },
            "pet": {
                "status": False,
                "pet_equipped": None,
                "pet_bag": list(),
                "pet_skin_status": None,
                "pet_skin": None
            },
            "inventory": {
                "medal": 0,
                "rank_point": 0,
                "coins": 10
            },
            "inventory_quest": dict(),
            "artifacts": dict(),
            "box": {"status": {"active": False, "secret": 0, "ur": 0, "sr": 0, "r": 0, "i": 0, "c": 0}},
            "cooldown": dict()
}

guild_data_structure = {
            "guild_id": None,
            "vip": False,
            "data": {
                "commands": 0,
                "lang": "pt",
                "ranking": "Bronze",
                "items": dict(),
                "accounts": 0,
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
                "log": False,
                "log_channel_id": None,
                "msg_delete": True,
                "msg_edit": True,
                "channel_edit_topic": True,
                "channel_edit_name": True,
                "channel_created": True,
                "channel_deleted": True,
                "channel_edit": True,
                "role_created": True,
                "role_deleted": True,
                "role_edit": True,
                "guild_update": True,
                "member_edit_avatar": True,
                "member_edit_nickname": True,
                "member_voice_entered": True,
                "member_voice_exit": True,
                "member_ban": True,
                "member_unBan": True,
                "emoji_update": True
            },
            "ia_config": {
                "auto_msg": False,
            },
            "rpg_config": {
                "rpg": False,
                "announcement": False,
                "announcement_id": None,
                "chat_farm": False,
                "chat_farm_id": None,
                "chat_battle": False,
                "chat_battle_id": None,
                "chat_pvp": False,
                "chat_pvp_id": None
            },
            "bot_config": {
                "ash_news": False,
                "ash_news_id": None,
                "ash_git": False,
                "ash_git_id": None,
                "ash_draw": False,
                "ash_draw_id": None,
            },
            "func_config": {
                "cont_users": False,
                "cont_users_id": None,
                "member_join": False,
                "member_join_id": None,
                "member_remove": False,
                "member_remove_id": None,
            },
            "moderation": {
                "status": False,
                "moderation_log": False,
                "moderation_channel_id": None,
                "bad_word": False,
                "bad_word_list": list(),
                "flood": False,
                "flood_channels": list(),
                "ping": False,
                "ping_channels": list(),
                "join_system": {
                    "join_system": False,
                    "join_system_channel_door": None,
                    "join_system_channel_log": None,
                    "join_system_role": None,
                },
                "prison": {
                    "status": False,
                    "prison_channel": None,
                    "prison_role": None,
                    "prisoners": {"id": {"time": 0, "reason": None, "roles": list()}}
                }
            },
            "command_locked": {
                "status": False,
                "while_list": list(),
                "black_list": list()
            },
            "receptions": dict()
}
