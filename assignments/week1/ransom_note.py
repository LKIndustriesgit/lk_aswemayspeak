import tracery
import random
from tracery.modifiers import base_english

rules = {
    "origin": "[pet:#p#] We have your #pet# #name#. \n #subsentence# \n #end# ",
    "p": ["dog", "cat", "spider"],
    "name": ["Johnny", "Peter", "Bello", "Friederike", "Carla", "XAEBT_0256"],
    "subsentence": "[money:#m#] If you don't send #money# € #timeanddate#, #badthings#.",
    "m": [str(random.randint(1,10000000)) for _ in range(50)],
    "timeanddate": "#date#, #time#",
    "date": ["by today", "by tomorrow", f"in {random.randint(2,29)} days"],
    "time": [f"{h:02d}:{m:02d}" for h in range(0,24) for m in range(0,60)],
    "badthings": ["bad things are going to happen", "we will eat it", "we will post bad pictures of it on instagram", "we will emotionally attack it"],
    "end": "The kidnappers."
    # "origin": "[myNoun:#n#] #myNoun.a.capitalize# #subsentence# #subsentence#.",
    # "n": ["rose","moon","apple"],
    # "subsentence": "is #myNoun.a#"
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)

for i in range(10):
    print(grammar.flatten("#origin#"))
    #safe / return output and randomise capitalisation afterwards


