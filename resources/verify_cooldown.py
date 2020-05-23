import datetime
epoch = datetime.datetime.utcfromtimestamp(0)


async def verify_cooldown(bot, _id, time_in_seconds, gift=False):

    data = await bot.db.get_data("_id", _id, "cooldown")

    if data is None:
        if not gift:
            data = {"_id": _id, "cooldown": (datetime.datetime.utcnow() - epoch).total_seconds()}
            await bot.db.push_data(data, "cooldown")
            return False
        return False

    update = data
    time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - update["cooldown"]

    if not gift:
        if time_diff < time_in_seconds:
            return False
    else:
        if time_diff > time_in_seconds:
            return False

    if not gift:
        update["cooldown"] = (datetime.datetime.utcnow() - epoch).total_seconds()
        await bot.db.update_data(data, update, "cooldown")
        return True

    await bot.db.delete_data({"_id": _id}, "cooldown")
    return True
