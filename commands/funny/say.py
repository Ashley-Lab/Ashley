import discord

from discord.ext import commands
from resources.check import check_it
from resources.db import Database


class SaySomething(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_it(no_pm=True)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.group(name='say', aliases=['diga'], invoke_without_command=True)
    async def say(self, ctx, *, msg: str = None):
        """comando usado pra ash enviar uma mensagem
        Use ash say <mensagem desejada>"""
        if ctx.invoked_subcommand is None:
            if msg is None:
                return await ctx.send('<:negate:520418505993093130>│``DIGITE ALGO PARA EU FALAR``')
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                pass
            finally:
                await ctx.send('```{}```'.format(msg.upper()))

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @say.command(name='channel', aliases=['canal'])
    async def _channel(self, ctx, channel: commands.TextChannelConverter, *, text: str = None):
        """apenas desenvolvedores"""
        if text is None:
            return await ctx.send('<:negate:520418505993093130>│``DIGITE ALGO PARA EU FALAR``')
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        finally:
            await channel.send('```{}```'.format(text.upper()))


def setup(bot):
    bot.add_cog(SaySomething(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mDIGA\033[1;32m foi carregado com sucesso!\33[m')
