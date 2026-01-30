# I used this file to find fitting words in the lovecraft text.
# I knew no way to label them so I had to do it kind of manually (still with help of things learned in lesson)
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
nlp = spacy.load('en_core_web_md')

text = open("../week5/books/At the Mountains of Madness").read()
full_doc = nlp(text)

#all_words =  [token for token in full_doc if token.is_alpha]
#word_count = Counter([w.text for w in all_words])
#print("most common words: \n")
#print(word_count.most_common(10))

all_words_without_sw = [word for word in all_words if word.text.lower() not in STOP_WORDS]
#print(len(all_words), len(all_words_without_sw))
#word_count = Counter([w.text for w in all_words_without_sw])
#print("\n most common words (without stop words): \n")
#print(word_count.most_common(20))

#most_common_adj = [word for word in all_words_without_sw if word.pos_ == "ADJ"]
#stop_extras = ["great", "certain", "high", "vast", "new", "low", "antarctic", "long", "small", "early", "general", "large", "curious", "upper", "little", "black", "present", "poor", "good", ]
#STOP_WORDS.update(stop_extras)
#adj_counter = Counter([w.lemma_ for w in most_common_adj if w.lemma_.lower() not in STOP_WORDS])
#print("\n most common adjectives: \n")
#print(adj_counter.most_common(20))

#most_common_noun = [word for word in all_words_without_sw if word.pos_ == "NOUN"]
#stop_extras = ["foot", "city", "mountain", "camp", "land", "place", "time", "world", "plane", "ice", "sculpture", "course", "wind", "year", "sea", "point", "wall", "rock", "man", ]
#STOP_WORDS.update(stop_extras)
#noun_counter = Counter([w.lemma_ for w in most_common_noun if w.lemma_.lower() not in STOP_WORDS])
#print("\n most common nouns: \n")
#print(noun_counter.most_common(20))

most_common_verb = [word for word in all_words_without_sw if word.pos_ == "VERB"]
stop_extras = ["find", "come", "think", "leave", "know", "look", "form", "tell", "begin", "try", "reach", "bring", "rise", "send", "lead", "work", "exist", "feel", "man",
               "point", "appear", 'suggest','build', 'turn', 'fly', 'accord', 'hold', 'lie', 'decide',
               ]
STOP_WORDS.update(stop_extras)
verb_counter = Counter([w.lemma_ for w in most_common_verb if w.lemma_.lower() not in STOP_WORDS])
print("\n most common verb: \n")
print(verb_counter.most_common(20))