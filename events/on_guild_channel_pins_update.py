class ChannelPinUpdate(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_guild_channel_pins_update(channel, last_pin):
        return


def setup(bot):
    bot.add_cog(ChannelPinUpdate(bot))
    print('\033[1;32mO evento \033[1;34mCHANNEL_PINS_UPDATE\033[1;32m foi carregado com sucesso!\33[m')
