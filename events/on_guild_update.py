class GuildUpdate(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_guild_update(before, after):
        return


def setup(bot):
    bot.add_cog(GuildUpdate(bot))
    print('\033[1;32mO evento \033[1;34mGUILD_UPDATE\033[1;32m foi carregado com sucesso!\33[m')
