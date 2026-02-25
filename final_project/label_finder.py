# I used this file to find fitting words in the lovecraft text.
# Now Im using it for my final project for additional text analysis

import spacy # importing spacy for text analysis
from spacy.lang.en.stop_words import STOP_WORDS # importing stop words for filtering
from collections import Counter # importing counter for counting most common words
import random # importing random for anonymisation logic

nlp = spacy.load('en_core_web_md') # initialising AI

with open("../final_project/books//The Jungle Book", encoding="utf8") as f:
    text = f.read()  # opening a book of my choice
full_doc = nlp(text) # runnig text through AI

# also using the replacements and the filtered words
generic_replacements = {
    "PERSON": ["the man", "the woman", "character", "person", "the figure", "the stranger"]
}
filtered_words = ["shoggoth", "sibyl", "chapter", "section", "socrates,—those", "polemarchus,—thrasymachu",
                  "polemarchus", "lachesis", "sophist", "hellene", "kaa", "nag"]
# Afterwards, I would add undesired words to this list, and maybe repeat the whole procedure
anonymised_text = text
for ent in sorted(full_doc.ents, key=lambda e: e.start_char, reverse=True):
    if ent.label_ == "PERSON":
        replacement = random.choice(generic_replacements["PERSON"])
        anonymised_text = (anonymised_text[:ent.start_char] +
                           replacement +
                           anonymised_text[ent.end_char:])
        # Anonymising it, see main.py
anonymised_doc = nlp(anonymised_text)
capitalised_nouns = [
    token.lemma_.lower()
    for token in anonymised_doc
    if (token.pos_ == "NOUN"  # if token labled as noun
        and token.text[0].isupper()  # if it is capitalised
        and token.lemma_.lower() not in STOP_WORDS  # and not a stop word
        and token.lemma_.lower() not in generic_replacements["PERSON"])  # and not a generic replacement
]
cap_counter = Counter(capitalised_nouns)  # count the most often used capitalised nouns (Names not anonymised yet)
print("\n most common caps: \n")
print(cap_counter.most_common(20))  # listing them
