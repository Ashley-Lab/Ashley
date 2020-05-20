import datetime
epoch = datetime.datetime.utcfromtimestamp(0)


async def verify_cooldown(bot, _id, time_in_seconds):
    data = await bot.db.get_data("_id", _id, "cooldown")
    if data is None:
        data = {"_id": _id, "cooldown": (datetime.datetime.utcnow() - epoch).total_seconds()}
        await bot.db.push_data(data, "cooldown")
        return False
    else:
        update = data
        time_diff = (datetime.datetime.utcnow() - epoch).total_seconds() - update["cooldown"]
        if time_diff < time_in_seconds:
            update['cooldown'] = (datetime.datetime.utcnow() - epoch).total_seconds()
            await bot.db.update_data(data, update, 'cooldown')
            return False
        update['cooldown'] = (datetime.datetime.utcnow() - epoch).total_seconds()
        await bot.db.update_data(data, update, 'cooldown')
        return True
