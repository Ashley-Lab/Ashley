class ChannelDelete(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_guild_channel_delete(channel):
        return


def setup(bot):
    bot.add_cog(ChannelDelete(bot))
    print('\033[1;32mO evento \033[1;34mCHANNEL_DELETE\033[1;32m foi carregado com sucesso!\33[m')
