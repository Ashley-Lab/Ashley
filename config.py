import json

with open("data/translations.json", encoding="utf-8") as translations:
    translations = json.load(translations)

with open("data/items.json", encoding="utf-8") as items:
    items = json.load(items)

with open("data/icons.json", encoding="utf-8") as icons:
    icons = json.load(icons)

with open("data/pets.json", encoding="utf-8") as pets:
    pets = json.load(pets)

with open("data/answers.json", encoding="utf-8") as answers:
    answers = json.load(answers)

with open("data/cards.json", encoding="utf-8") as cards:
    cards = json.load(cards)

with open("data/ctf.json", encoding="utf-8") as ctf:
    ctf = json.load(ctf)

with open("data/riddles.json", encoding="utf-8") as riddles:
    riddles = json.load(riddles)

with open("data/config.json", encoding="utf-8") as config:
    config = json.load(config)

with open("data/palin.json", encoding="utf-8") as palin:
    palin = json.load(palin)

with open("data/questions.json", encoding="utf-8") as questions:
    questions = json.load(questions)

with open("data/reflect.json", encoding="utf-8") as reflect:
    reflect = json.load(reflect)

with open("data/salutation.json", encoding="utf-8") as salutation:
    salutation = json.load(salutation)

with open("data/staff.json", encoding="utf-8") as staff:
    staff = json.load(staff)

with open("data/thinker.json", encoding="utf-8") as thinker:
    thinker = json.load(thinker)

with open("data/poke.json", encoding="utf-8") as poke:
    poke = json.load(poke)

with open("data/forca.json", encoding="utf-8") as forca:
    forca = json.load(forca)

with open("data/battle.json", encoding="utf-8") as battle:
    battle = json.load(battle)

with open("data/skills.json", encoding="utf-8") as skills:
    skills = json.load(skills)

data = {"translations": translations, "items": items, "icons": icons, "pets": pets, "answers": answers, "cards": cards,
        "ctf": ctf, "riddles": riddles, "config": config, "palin": palin, "questions": questions, "reflect": reflect,
        "salutation": salutation, "staff": staff, "thinker": thinker, "poke": poke, "forca": forca, "battle": battle,
        "skills": skills}
