class WebhooksUpdate(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def on_webhooks_update(channel):
        return


def setup(bot):
    bot.add_cog(WebhooksUpdate(bot))
    print('\033[1;32mO evento \033[1;34mWEBHOOKS_UPDATE\033[1;32m foi carregado com sucesso!\33[m')
