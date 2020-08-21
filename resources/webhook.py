import json
import aiohttp

from datetime import datetime


class Webhook:
    def __init__(self, url: str, message: str = None, embed: dict = None):
        self.url = url
        self.message = message
        self.embed = embed
        self.time = datetime.now().strftime("[%d/%m/%y - %H:%M]")

    def to_json(self):
        payload = {'embeds': []}
        if self.message:
            payload['content'] = self.message
        if self.embed:
            payload['embeds'].append(self.embed)
        return json.dumps(payload)

    async def send(self):
        headers = {"Content-Type": "application/json"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(self.url, data=self.to_json()) as response:
                if response.status >= 400:
                    print(f"\n\033[1;30m( ❌ ) | {self.time} \033[1;34mErro\033[1;30m ao enviar dados para o Webhook "
                          f"\033[1;31m{f'com o status: {response.status}'}...\33[m\n")
