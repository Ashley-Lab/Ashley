import io
import json

from textwrap import indent
from contextlib import redirect_stdout
from traceback import format_exc
from discord.ext import commands
from resources.check import check_it
from resources.db import Database

with open("data/auth.json") as security:
    _auth = json.loads(security.read())


class EvalSintax(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @staticmethod
    def get_syntax_error(e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @staticmethod
    def cleanup_code(content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @check_it(no_pm=True, is_owner=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx))
    @commands.command(hidden=True)
    async def eval(self, ctx, *, body: str):
        """apenas desenvolvedores"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.guild,
            'guild': ctx.message.guild,
            'message': ctx.message,
            '_': self._last_result,
            'self': self
        }
        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        to_compile = 'async def func():\n%s' % indent(body, '  ')
        try:
            exec(to_compile, env)
        except SyntaxError as e:
            await ctx.message.add_reaction('❌')
            return await ctx.send(self.get_syntax_error(e))
        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except None:
            value = stdout.getvalue()
            if any([i in str(value) for i in [_auth['_t__ashley'], _auth['db_url']]]):
                return await ctx.send(f"<:alert_status:519896811192844288> | ``You crazy man?`` {ctx.author.mention}")
            await ctx.send('```py\n{}{}\n```'.format(value, format_exc()))
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except None:
                pass
            if ret is None:
                if value:
                    if any([i in str(value) for i in [_auth['_t__ashley'], _auth['db_url']]]):
                        return await ctx.send(
                            f"<:alert_status:519896811192844288> | ``You crazy man?`` {ctx.author.mention}")
                    await ctx.send('```py\n%s\n```' % value)
            else:
                self._last_result = ret
                if any([i in str(value) for i in [_auth['_t__ashley'], _auth['db_url']]]):
                    return await ctx.send(
                        f"<:alert_status:519896811192844288> | ``You crazy man?`` {ctx.author.mention}")
                if any([i in str(ret) for i in [_auth['_t__ashley'], _auth['db_url']]]):
                    return await ctx.send(
                        f"<:alert_status:519896811192844288> | ``You crazy man?`` {ctx.author.mention}")
                await ctx.send('```py\n%s%s\n```' % (value, ret))


def setup(bot):
    bot.add_cog(EvalSintax(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mEVALSINTAX\033[1;32m foi carregado com sucesso!\33[m')
