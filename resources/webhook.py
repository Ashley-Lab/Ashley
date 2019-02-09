import json
import requests

from datetime import datetime


class WebHook:
    def __init__(self, url: str, message: str = None, embed: dict = None):
        self.url = url
        self.message = message
        self.embed = embed
        self.tempo = datetime.now().strftime("[%d/%m/%y - %H:%M]")

    def converter_json(self):
        payload = {'embeds': []}
        if self.message:
            payload['content'] = self.message
        if self.embed:
            payload['embeds'].append(self.embed)
        return json.dumps(payload)

    def send_(self):
        headers = {"Content-Type": "application/json"}
        req = requests.post(self.url, headers=headers, data=self.converter_json())
        if not req.ok:
            print(f"\033[1;32m{self.tempo} \033[1;34mErro\033[1;32m ao enviar dados para o Webhook\33[m\n"
                  f"{self.url[:75]}...")
        else:
            print(f"\033[1;32m{self.tempo} \033[1;34mDados enviados\033[1;32m para o Webhook\33[m\n{self.url[:75]}...")
