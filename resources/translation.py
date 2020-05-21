from config import data as config


async def t_(ctx, translation, db_name="guilds"):
    if ctx.guild is not None:
        data = await ctx.bot.db.get_data("guild_id", ctx.guild.id, db_name)
        if data is not None:
            lang = data["data"].get("lang", "pt")
            currency = data["data"].get("currency", config['config']['default_money'])

            # troca o nome da moeda padrao para a customizavel do servidor
            if lang == "pt":
                return translation.replace(config['config']['default_money'], currency)

            try:
                translation_ = ctx.bot.translations[translation][lang]
                return translation_.replace(config['config']['default_money'], currency)
            except None:
                return translation.replace(config['config']['default_money'], currency)

    return translation
