from discord.ext import commands
# importação dos scripts de ia (texto)
from ia.scripts import ia
# importação das libs do chatbot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


class IaInteractions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scripts = [ia.about_me, ia.concept, ia.deeping, ia.introduction]
        self.heart = ChatBot('Guardians', read_only=True)
        self.trainer = ListTrainer(self.heart)
        for script in self.scripts:
            self.trainer.train(script)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and str(message.author.id) not in self.bot.blacklist:
            data_guild = self.bot.db.get_data("guild_id", message.guild.id, "guilds")
            user_data = self.bot.db.get_data("user_id", message.author.id, "users")
            if data_guild is not None and user_data is not None:
                if '?' in message.content:
                    response = self.heart.get_response(message.content)
                    if float(response.confidence) >= 0.5:
                        await message.channel.send(f"**{message.author.name}**\n ``{response}``")


def setup(bot):
    bot.add_cog(IaInteractions(bot))
    print('\033[1;33m( 🔶 ) | O evento \033[1;34mIA_INTERACTIONS\033[1;33m foi carregado com sucesso!\33[m')
