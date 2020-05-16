import unicodedata


def clear_content(string):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', string)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return palavra_sem_acento


class HeartIA(object):
    def __init__(self, scripts, percent):
        self.scripts = scripts
        self.perc = percent
        self.conf = [0.0, 0.0, 0.0, 0.0]
        self.chance = False

    def calc_confidence(self, content, response):
        for n in range(len(content)):
            if n in [0, 1]:
                try:
                    r_1 = len([name for name in set(content[n].lower().split()) if name in response.lower().split()])
                    r_2 = len(response.lower().split())
                    self.conf[n] = r_1 / r_2
                except ZeroDivisionError:
                    self.conf[n] = 0.0
            else:
                try:
                    r_1 = len([name for name in set(response.lower().split()) if name in content[n].lower().split()])
                    r_2 = len(content[n].lower().split())
                    self.conf[n] = r_1 / r_2
                except ZeroDivisionError:
                    self.conf[n] = 0.0

    def get_response(self, c):
        r = clear_content(c)
        self.chance = False
        for script in self.scripts:
            for i in script:
                self.calc_confidence([c, r, c, r], i.lower())

                # verificar a confiança -------------------------------------------
                if c == i.lower() or r == i.lower():
                    self.chance = True
                if self.conf[0] >= self.perc and self.conf[2] >= self.perc:
                    if self.conf[1] >= self.perc and self.conf[3] >= self.perc:
                        self.chance = True
                # ----------------------------------------------------------------

                if self.chance:
                    try:
                        return script[script.index(i) + 1]
                    except IndexError:
                        return None
        return None
