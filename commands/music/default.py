import discord
import asyncio
import itertools
import json
import math
import random
import youtube_dl

from discord.ext import commands
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from discord import opus
from resources.db import Database
from resources.check import check_it
from resources.utility import parse_duration
from collections import Counter

with open("resources/auth.json") as security:
    _auth = json.loads(security.read())

cont = Counter()
color = int(_auth['default_embed'], 16)
opus_libs_dll = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
youtube_dl.utils.bug_reports_message = lambda: ' '
last_search = {}


def load_opus_lib(opus_libs=None):
    if opus_libs is None:
        opus_libs = opus_libs_dll
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))


load_opus_lib()

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = int(data.get('duration'))

    def __str__(self):
        return f'**{self.title}** *[Duration: {parse_duration(self.duration)}]*'

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=True):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f'<:queue:519896839332560897>│``Dj.Ashley``\n```ini\n[Adicionei {data["title"]} para a lista de '
                       f'reprodução.]\nDuração: [{parse_duration(int(data.get("duration")))}]```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title'],
                    'duration': data['duration']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=True)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class SongQueue(asyncio.Queue):
    def __iter__(self):
        return self._queue.__iter__()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, value: int):
        self._queue.rotate(-value)
        self._queue.pop()
        self._queue.rotate(value - 1)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(itertools.islice(self._queue, index.start, index.stop, index.step))
        else:
            return self._queue[index]

    def __len__(self):
        return len(self._queue)

    @property
    def queue(self):
        return self._queue


class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume', 'repeat',
                 'search', 'cont_')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = SongQueue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = .5
        self.current = None
        self.repeat = False
        self.search = None
        self.cont_ = {}

        ctx.bot.loop.create_task(self.player_loop(ctx))

    async def player_loop(self, ctx):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):
                    if self.repeat and last_search[ctx.guild.id] is not None:
                        if ctx.guild.id not in self.cont_:
                            self.cont_[ctx.guild.id] = 0
                        if self.cont_[ctx.guild.id] == len(last_search[ctx.guild.id]):
                            self.cont_[ctx.guild.id] = 0
                        self.search = str(last_search[ctx.guild.id][self.cont_[ctx.guild.id]])
                        self.cont_[ctx.guild.id] += 1
                        source = await YTDLSource.create_source(ctx, self.search, loop=self.bot.loop, download=True)
                        await self.queue.put(source)
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)
            except IndexError:
                continue

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except IndexError as e:
                    await self._channel.send(f'Ocorreu um erro ao processar sua música.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source
            try:
                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            except AttributeError:
                pass
            except discord.errors.ClientException:
                pass

            if self.queue is not None:
                self.np = await self._channel.send(f'<:play:519896828091564033>│**Tocando agora:** `{source.title}` '
                                                   f'\nsolicitado por `{source.requester}`\n'
                                                   f'Duração: **{parse_duration(source.duration)}**')
            await self.next.wait()

            if not self.repeat:
                self.cont_[ctx.guild.id] = 0
                last_search[ctx.guild.id] = list()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

            if len(self.queue) == 0 and not self.repeat:
                await ctx.send('<:alert_status:519896811192844288>│``As músicas acabaram!``'
                               ' **COLOQUE OUTRA MUSICA!**', delete_after=20)

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class GuildState:

    def __init__(self):
        self.skip_votes = set()

    @staticmethod
    def is_requester(ctx):
        return ctx.voice_client.source.requester == ctx.author


class MusicDefault(commands.Cog):
    __slots__ = ('bot', 'players', 'states')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.states = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def _vote_skip(self, channel, member):
        state = self.get_state(channel.guild)
        state.skip_votes.add(member)
        users_in_channel = len([member for member in channel.members if not member.bot])
        if (float(len(state.skip_votes)) / users_in_channel) >= 0.5:
            channel.guild.voice_client.stop()

    def get_state(self, guild):
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    @staticmethod
    async def __local_check(ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='connect', aliases=['join', 'entrar'])
    async def _connect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise commands.CheckFailure('<:oc_status:519896814225457152>│``Nenhum canal para participar. '
                                            'Por favor, especifique um canal válido ou entre em um!``')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise commands.CheckFailure(f'<:oc_status:519896814225457152>│Mover para o canal: '
                                            f'<{channel}> tempo esgotado.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise commands.CheckFailure(f'<:oc_status:519896814225457152>│Conectando ao canal: '
                                            f'<{channel}> tempo esgotado.')

        await ctx.send(f'<:on_status:519896814799945728>│Conectado a: **{channel}**', delete_after=20)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='play', aliases=['sing', 'tocar'])
    async def play_(self, ctx, *, search: str = "Ashley escape the fate"):
        await ctx.trigger_typing()
        vc = ctx.voice_client

        if not vc:
            last_search[ctx.guild.id] = list()
            await ctx.invoke(self._connect)

        player = self.get_player(ctx)

        if ctx.guild.id not in last_search:
            last_search[ctx.guild.id] = list()
        last_search[ctx.guild.id].append(search)
        if last_search[ctx.guild.id] is not None:
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=True)
            await player.queue.put(source)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='pause', aliases=['pausar'])
    async def pause_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não estou tocando nada!``',
                                  delete_after=20)
        elif vc.is_paused():
            return
        state = self.get_state(ctx.guild)
        if ctx.channel.permissions_for(ctx.author).administrator or state.is_requester(ctx):
            vc.pause()
            await ctx.send(f'<:pause:519896824622874634>│**`{ctx.author}`**: Pausou a música!', delete_after=20)
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você não tem permissão para fazer isso!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='resume', aliases=['voltar', 'retornar'])
    async def resume_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não estou tocando nada!``',
                                  delete_after=20)
        elif not vc.is_paused():
            return

        state = self.get_state(ctx.guild)
        if ctx.channel.permissions_for(ctx.author).administrator or state.is_requester(ctx):
            vc.resume()
            await ctx.send(f'<:play:519896828091564033>│**`{ctx.author}`**: Retomou a música!', delete_after=20)
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você não tem permissão para fazer isso!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='skip', aliases=['pular', 'passar'])
    async def skip_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não estou tocando nada!``',
                                  delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        state = self.get_state(ctx.guild)
        if ctx.channel.permissions_for(ctx.author).administrator or state.is_requester(ctx):
            vc.stop()
            await ctx.send(f'<:point:519896842192814110>│**`{ctx.author}`**: Pulou a música!', delete_after=20)
        else:
            client = ctx.guild.voice_client
            channel = client.channel
            users_in_channel = len([member for member in channel.members if not member.bot])
            await self._vote_skip(channel, ctx.author)
            required_votes = math.ceil(0.5 * users_in_channel)
            await ctx.send(f"<:alert_status:519896811192844288>│{ctx.author.mention} ``Votou para pular`` "
                           f"**({len(state.skip_votes)}/{required_votes} Votos)**", delete_after=20)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='queue', aliases=['q', 'playlist', 'lista'])
    async def queue_info(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não estou conectado à nenhum canal '
                                  'de voz!``', delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não há mais músicas enfileiradas.``',
                                  delete_after=20)

        upcoming = list(itertools.islice(player.queue.queue, 0, 5))

        try:
            cont['list'] = 0
        except KeyError:
            pass

        def counter():
            global cont
            cont['list'] += 1
            return cont['list']

        if not player.repeat:
            fmt = '\n'.join(f'**[{counter()}]**`{_["title"]}` **duration** '
                            f'`{parse_duration(int(_["duration"]))}`' for _ in upcoming)
        else:
            fmt = '\n'.join([f'**[{counter()}]** : ``{_}`` **duration** '
                             f'`{parse_duration(int(_["duration"]))}`' for _ in last_search[ctx.guild.id]])
        embed = discord.Embed(title=f'<:queue:519896839332560897>│**Lista de Reprodução**: '
                                    f'``Atualmente há {len(upcoming)} em espera!``', description=fmt,
                              color=color)
        embed.set_thumbnail(
            url="http://icons.iconarchive.com/icons/raindropmemory/summer-love-cicadas/256/Music-1-icon.png")
        embed.set_footer(text="Ashley ® Todos os direitos reservados.")
        await ctx.send(embed=embed)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='shuffle', aliases=['embaralhar'])
    async def _shuffle(self, ctx):
        state = self.get_player(ctx)

        if len(state.queue) == 0:
            return await ctx.send('<:alert_status:519896811192844288>│``Não há itens na lista``', delete_after=20)

        if ctx.channel.permissions_for(ctx.author).administrator:
            state.queue.shuffle()
            await ctx.send(f'<:on_status:519896814799945728>│``Lista embaralhada com sucesso!``', delete_after=20)
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você não tem permissão para fazer isso!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='remove', aliases=['remover'])
    async def _remove(self, ctx, index=-1):
        state = self.get_player(ctx)

        if len(state.queue) == 0:
            return await ctx.send('<:alert_status:519896811192844288>│``Não há itens na lista``', delete_after=20)
        elif index == -1:
            return await ctx.send('<:alert_status:519896811192844288>│``Você precisa dizer um item para remover da '
                                  'lista``', delete_after=20)
        try:
            index = int(index)
        except ValueError:
            return await ctx.send('<:oc_status:519896814225457152>│``Você precisa digitar um numero!``')

        if ctx.channel.permissions_for(ctx.author).administrator:
            state.queue.remove(index)
            await ctx.send(f'<:on_status:519896814799945728>│``Item removido com sucesso!``', delete_after=20)
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você não tem permissão para fazer isso!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='clear', aliases=['limpar'])
    async def _clear(self, ctx):
        state = self.get_player(ctx)

        if len(state.queue) == 0:
            return await ctx.send('<:alert_status:519896811192844288>│``Não há itens na lista``', delete_after=20)

        if ctx.channel.permissions_for(ctx.author).administrator:
            state.queue.clear()
            last_search[ctx.guild.id] = list()
            await ctx.send(f'<:on_status:519896814799945728>│``Lista esvaziada com sucesso!``', delete_after=20)
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você não tem permissão para fazer isso!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='repeat', aliases=['repetir'])
    async def _repeat(self, ctx):
        state = self.get_state(ctx.guild)
        if ctx.channel.permissions_for(ctx.author).administrator or state.is_requester(ctx):
            player = self.get_player(ctx)
            player.repeat = not player.repeat
            await ctx.send(f'<:on_status:519896814799945728>│``repetição '
                           f'{"habilitada" if player.repeat else "desabilitada"} '
                           f'com sucesso!``', delete_after=20)
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você não tem permissão para fazer isso!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing', 'tocando'])
    async def now_playing_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não estou conectado à nenhum canal '
                                  'de voz!``', delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não estou tocando nada!``',
                                  delete_after=20)

        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(f'<:play:519896828091564033>│**Tocando agora:** `{vc.source.title}` \n'
                                   f'<:point:519896842192814110>│Requerido por`{vc.source.requester}` \n'
                                   f'Duração: **{parse_duration(vc.source.duration)}**', delete_after=20)

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float = 100.0):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não estou conectado à nenhum canal '
                                  'de voz!``', delete_after=20)

        if not 0 < vol < 101:
            return await ctx.send('<:oc_status:519896814225457152>│``Por favor insira um valor entre 1 e 100.``',
                                  delete_after=20)

        player = self.get_player(ctx)
        state = self.get_state(ctx.guild)
        if ctx.channel.permissions_for(ctx.author).administrator or state.is_requester(ctx):
            if vc.source:
                vc.source.volume = vol / 100
            player.volume = vol / 100
            await ctx.send(f'<:volume:519896822093971457>│**`{ctx.author}`**: Definiu o volume para **{vol}%**',
                           delete_after=20)
        else:
            await ctx.send('<:oc_status:519896814225457152>│``Você não tem permissão para fazer isso!``')

    @check_it(no_pm=True)
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    @commands.check(lambda ctx: Database.is_registered(ctx, ctx, vip=True))
    @commands.command(name='stop', aliases=['parar'])
    async def stop_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('<:alert_status:519896811192844288>│``Atualmente não estou tocando nada!``',
                                  delete_after=20)
        else:
            state = self.get_state(ctx.guild)
            if state.is_requester(ctx) is None:
                await self.cleanup(ctx.guild)
                return await ctx.send('<:stop:519896823196942336>│``Todas as músicas foram paradas!``',
                                      delete_after=20)
            if ctx.channel.permissions_for(ctx.author).administrator or state.is_requester(ctx):
                await ctx.send('<:stop:519896823196942336>│``Todas as músicas foram paradas!``',
                               delete_after=20)
                await self.cleanup(ctx.guild)
                last_search[ctx.guild.id] = list()
            else:
                await ctx.send('<:oc_status:519896814225457152>│``Você não tem permissão para fazer isso!``')


def setup(bot):
    bot.add_cog(MusicDefault(bot))
    print('\033[1;32mOs comandos de \033[1;34mMUSICAS\033[1;32m foram carregados com sucesso!\33[m')
