# This is just a file for testing purposes,
# so the code is not perfectly clean and mostly just copied from my final project
import spacy # spacy for text corpus analysis
import random # for the generic replacements
from collections import Counter # for counting most common words in labels

nlp = spacy.load("en_core_web_md") # loading the NLP AI

# nearst neighbor code, copied from main.py
def nearest_neighbors(target, vocab, k=5):  # semantic similarity nearest neighbors, as seen in week 3
    query = nlp(target)[0]  # running the word chosen by player through the AI
    scores = {}  # empty dict for scores
    for w in vocab:  # searching every word in the book
        if w == target:  # skipping the chosen word itself in the book (avoiding same words seen as "similar")
            continue
        token = nlp.vocab[w]  # getting the token of the word
        if token.has_vector:
            score = query.similarity(token)  # analysing its similarity
            scores[w] = score  # saving the similarity score
    top = sorted(scores.items(), key=lambda x: -x[1])[:k]  # sorting the vocab by score and getting the top 5 (k = 5)

    return top  # returning them in game



random_choice = "Platos Republic" # predefining the random choice for analysis purposes
with open("../final_project/books/" + random_choice, encoding="utf8") as f:
    text = f.read()
doc = nlp(text) # running book through NLP

# replacement logic from main.py
generic_replacements = {
    "PERSON": ["the man", "the woman", "Character", "Person", "the figure", "the stranger"]
}  # using this generic replacements for character names

anonymised_text = text  # putting book content into new var to distiguish between anonymised and pre-anonymised text
for ent in sorted(doc.ents, key=lambda e: e.start_char,
                  reverse=True):  # sorting the vocab after SpaCy entities (persons, adjectives, verbs)
    # reversing it is important because text length changes through anonymisation. If the last word is changed first,
    # no detected entities before it are affected by differing length
    if ent.label_ == "PERSON":  # If a word is part of the person label
        replacement = random.choice(
            generic_replacements["PERSON"])  # randomly choose a generic person descriptor from the list
        anonymised_text = (
                anonymised_text[:ent.start_char] +  # the text before the detected entity
                replacement +  # putting the replacement in between
                anonymised_text[ent.end_char:]  # the text after the detected entity
        )

doc = nlp(anonymised_text)  # running the anonymised text through the NLP AI

vocab_from_file = list({  # preparing all of the text for the semantic similarity algorithm
    token.text.lower()  # putting every word in lower case
    for token in doc  # if it is part of the anonymised text run through the AI
    if not token.is_stop and token.is_alpha and token.has_vector
    # and if its not a stop word, if it consists of letters (alpha) and has a relation to the other words (vector)
})

flag = False # flag because I wanted a guessing loop in here too
guesses = 5 # back when I still limited the guesses
most_common_verb = [word for word in doc if word.pos_ == "VERB"] # finding different labels types in text corpus
most_common_noun = [word for word in doc if word.pos_ == "NOUN"] # (all words in doc that are labled as:)
most_common_adj = [word for word in doc if word.pos_ == "ADJ"]
most_common_pers = [word for word in doc if word.pos_ == "PERSON"]
# counting all vectors which are not stop words but consist of letters and have an actual vector relation (all words)
word_count = Counter([token.text.lower() for token in doc if not token.is_stop and token.is_alpha and token.has_vector])
adj_counter = Counter([w.lemma_ for w in most_common_adj if w.lemma_.lower()])  # counting and sorting all words which are in the adj label
noun_counter = Counter([w.lemma_ for w in most_common_noun if w.lemma_.lower()])
verb_counter = Counter([w.lemma_ for w in most_common_verb if w.lemma_.lower()])
person_counter = Counter([w.lemma_ for w in most_common_pers if w.lemma_.lower()])
print("most common words: \n")
print(word_count.most_common(10)) # listing the top 10 words
print("most common adjectives: \n")
print(adj_counter.most_common(10))
print("most common verbs: \n")
print(verb_counter.most_common(20)) # listing the top 20 words
print("most common nouns: \n")
print(noun_counter.most_common(20))
print("most common persons: \n")
print(person_counter.most_common(20))
game = input("want to word count guess? (y/n)") # little guess logic for testing too
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
