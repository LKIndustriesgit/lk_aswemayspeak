import spacy
import random
from collections import Counter
nlp = spacy.load("en_core_web_md")

def nearest_neighbors(target, vocab, k=5):
    query = nlp(target)[0]
    scores = {}
    for w in vocab:
        if w == target:
            continue
        token = nlp.vocab[w]
        if token.has_vector:
            score = query.similarity(token)
            scores[w] = score
    top = sorted(scores.items(), key=lambda x: -x[1])[:k]

#random_choice, vocab_from_file, flag, guesses, transitions, tokens, top_names
random_choice = "Platos Republic"
with open("../final_project/books/" + random_choice, encoding="utf8") as f:
    text = f.read()
doc = nlp(text)

generic_replacements = {
    "PERSON": ["the man", "the woman", "Character", "Person", "the figure", "the stranger"]
}

anonymised_text = text
for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
    if ent.label_ == "PERSON":
        replacement = random.choice(generic_replacements["PERSON"])
        anonymised_text = (anonymised_text[:ent.start_char] +
                           replacement +
                           anonymised_text[ent.end_char:])

doc = nlp(anonymised_text)

vocab_from_file = list({
        token.text.lower()
        for token in doc
        if not token.is_stop and token.is_alpha and token.has_vector
    })

flag = False
guesses = 5
most_common_verb = [word for word in doc if word.pos_ == "VERB"]
most_common_noun = [word for word in doc if word.pos_ == "NOUN"]
most_common_adj = [word for word in doc if word.pos_ == "ADJ"]
most_common_pers = [word for word in doc if word.pos_ == "PERSON"]
word_count = Counter([token.text.lower() for token in doc if not token.is_stop and token.is_alpha and token.has_vector])
adj_counter = Counter([w.lemma_ for w in most_common_adj if w.lemma_.lower()])
noun_counter = Counter([w.lemma_ for w in most_common_noun if w.lemma_.lower()])
verb_counter = Counter([w.lemma_ for w in most_common_verb if w.lemma_.lower()])
person_counter = Counter([w.lemma_ for w in most_common_pers if w.lemma_.lower()])
print("most common words: \n")
print(word_count.most_common(10))
print("most common adjectives: \n")
print(adj_counter.most_common(10))
print("most common verbs: \n")
print(verb_counter.most_common(20))
print("most common nouns: \n")
print(noun_counter.most_common(20))
print("most common persons: \n")
print(person_counter.most_common(20))
game = input("want to word count guess? (y/n)")
if game == "y":
    Flag = True
if game == "n":
    print("goodbye!")
else:
    print("invalid!")
while flag:
    if guesses > 0:
        print("Guesses left: " + str(guesses))
        word = input(
            '\n(write "s" to stop. \nWord in the grammar of text: ').strip().lower()
        if word == "s":
            flag = False
        else:
            neighbor = nearest_neighbors(word, vocab_from_file, 5)
            print(neighbor)
            guesses -= 1
    else:
        result = True
        flag = False
