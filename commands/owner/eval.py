import io
import json
import traceback
import textwrap

from contextlib import redirect_stdout
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
    @commands.command(name='eval')
    async def eval(self, ctx, *, body: str):
        """Apenas desenvolvedores."""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            await ctx.message.add_reaction('❌')
            return await ctx.send(self.get_syntax_error(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            if e:
                pass
            value = stdout.getvalue()
            msg = f'```py\n{value}{traceback.format_exc()}\n```'.replace(_auth['_t__ashley'], "[CENSORED]")
            msg = msg.replace(_auth['db_url'], "[CENSORED]")
            await ctx.send(msg)
        else:
            value = stdout.getvalue()
            await ctx.message.add_reaction('\u2705')

            if ret is None:
                if value:
                    self._last_result = ret
                    msg = f'```py\n{value}\n```'.replace(_auth['_t__ashley'], "[CENSORED]")
                    msg = msg.replace(_auth['db_url'], "[CENSORED]")
                    await ctx.send(msg)
            else:
                self._last_result = ret
                msg = f'```py\n{value}{ret}\n```'.replace(_auth['_t__ashley'], "[CENSORED]")
                msg = msg.replace(_auth['db_url'], "[CENSORED]")
                await ctx.send(msg)


def setup(bot):
    bot.add_cog(EvalSintax(bot))
    print('\033[1;32m( 🔶 ) | O comando \033[1;34mEVALSINTAX\033[1;32m foi carregado com sucesso!\33[m')
