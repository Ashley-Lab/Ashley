import re
import unicodedata


def clear_content(string):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', string)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z \\\]', '', palavra_sem_acento)


class HeartIA(object):
    def __init__(self, scripts, percent):
        self.scripts = scripts
        self.percent = percent
        self.confidence = float(0.0)

    def calc_confidence(self, content, response):
        r_1 = len([name for name in content.upper().split() if name in response.upper().split()])
        r_2 = len(response.upper().split())
        self.confidence = float(r_1 / r_2)

    def get_response(self, content):
        response = clear_content(content)
        chance = False
        for script in self.scripts:
            for i in script:
                if content == i or response == i:
                    chance = True
                self.calc_confidence(content, i)
                if self.confidence >= self.percent:
                    chance = True
                self.calc_confidence(response, i)
                if self.confidence >= self.percent:
                    chance = True
                if chance:
                    try:
                        return script[script.index(i) + 1]
                    except IndexError:
                        return None
                return None
