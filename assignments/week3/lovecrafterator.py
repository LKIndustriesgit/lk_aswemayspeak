# this is meant to be an ironic attempt at copying H. P. Lovecrafts' style and condesing it to its bare minimum
import tracery as tr
import spacy as spacy
import random
from tracery.modifiers import base_english

text = open("../week3/hpl").read()
nlp = spacy.load("en_core_web_md")
full_doc = nlp(text)

def flatten_subtree(st):
    return "".join([w.text_with_ws for w in st]).strip()

def phrases_with_word(word):
    phrases = []
    for sent in full_doc.sents:
        if word in sent.text:
            phrases.append(sent.text.replace("\n", " ").strip())
    return phrases


nouns = set()
verbs = set()
adjectives = set()

for token in full_doc:
    if token.is_stop or token.is_punct or token.is_space:
        continue
    if token.pos_ == "NOUN":
        nouns.add(token.lemma_.lower())
    elif token.pos_ == "VERB":
        verbs.add(token.lemma_.lower())
    elif token.pos_ == "ADJ":
        adjectives.add(token.lemma_.lower())


names = set()
for ent in full_doc.ents:
    if ent.label_ in ("PERSON", "ORG"):
        names.add(ent.text.strip())


nouns = list(nouns)
verbs = list(verbs)
adjectives = list(adjectives)
names = list(names)
##adjs and nouns found through label_finder.py
NEGATIVE_ADJ_SET = {
    'monstrous', 'unknown', 'dead', 'strange', 'terrible', 'primal', 'nameless', 'bad','mad', 'fantastic', 'dark',
}

OLD_ADJ_SET = {
    "old", "ancient",
}

MONSTER_NOUN_SET = {
    "monster", "thing", "specimen", "horror",
}
#these were too hard to find, so i used mainly my own
NEGATIVE_VERB_SET = {
    "kill", "devour", "haunt", "corrupt", "destroy",
    "torment", "curse", "encounter", "study", "infect", "consume"
}

scary_adjs = [a for a in adjectives if a in NEGATIVE_ADJ_SET] #or ["horrible", "hideous"]
old_adjs = [a for a in adjectives if a in OLD_ADJ_SET] #or ["ancient", "eldritch"]
monster_nouns = [n for n in nouns if n in MONSTER_NOUN_SET] #or ["monster", "horror", "thing"]
negative_verbs = [v for v in verbs if v in NEGATIVE_VERB_SET] #or ["devour", "haunt", "destroy"]

deeds = []
for v in negative_verbs:
    some_noun = random.choice(nouns)
    deeds.append(f"{v} the {some_noun}")
if_phrases = phrases_with_word("If")
...
rules = {
    "origin": "#title# \n #intro# \n #doctor_intro.capitalize#. \n #evil.capitalize#. \n #end#. ",
    "title": "The #adj# #noun#",
    "adj": adjectives,
    "noun": nouns,
    "intro": if_phrases,
    "doctor_intro": "I am #education# #name#",
    "education": ["dr.", "prof.", "sir", "dr. dr.", "king (I recently found out that my family happens to be royal)"],
    "name": names,
    "evil": "the #scary# #old# #monster# #did# #stuff#",
    "scary": scary_adjs,
    "old": old_adjs,
    "monster": monster_nouns,
    "did": ["did", "once did", "secretly did"],
    "stuff": deeds,
    "end": "Now I am #consequence#",
    "consequence": ["dead", "insane"],
}

grammar = tr.Grammar(rules)
grammar.add_modifiers(base_english)

for i in range(5):
    print(grammar.flatten("#origin#"))
    print("\n --------------- \n")