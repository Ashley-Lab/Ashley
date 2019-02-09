class RoleCreate(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_guild_role_create(role):
        return


def setup(bot):
    bot.add_cog(RoleCreate(bot))
    print('\033[1;32mO evento \033[1;34mROLE_CREATE\033[1;32m foi carregado com sucesso!\33[m')
