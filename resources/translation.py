import json

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())


def t_(ctx, translation, db_name="guilds"):
    if ctx.guild is not None:
        data = ctx.bot.db.get_data("guild_id", ctx.guild.id, db_name)
        if data is not None:
            lang = data["data"].get("lang", "pt")
            currency = data["data"].get("currency", _auth['default_money'])

            # troca o nome da moeda padrao para a customizavel do servidor
            if lang == "pt":
                return translation.replace(_auth['default_money'], currency)

            try:
                translation_ = ctx.bot.translations[translation][lang]
                return translation_.replace(_auth['default_money'], currency)
            except None:
                return translation.replace(_auth['default_money'], currency)

    return translation
