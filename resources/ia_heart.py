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
        self.perc = percent
        self.conf = [0.0, 0.0]
        self.chance = False

    def calc_confidence(self, content, response):
        for n in range(len(content)):
            r_1 = len([name for name in set(content[n].lower().split()) if name in response.lower().split()])
            r_2 = len(response.lower().split())
            self.conf[n] = r_1 / r_2

    def get_response(self, c):
        r = clear_content(c)
        self.chance = False
        for script in self.scripts:
            for i in script:
                self.calc_confidence([c, r], i)
                if c == i or r == i or self.conf[0] >= self.perc or self.conf[1] >= self.perc:
                    self.chance = True
                if self.chance:
                    try:
                        return script[script.index(i) + 1]
                    except IndexError:
                        return None
        return None
