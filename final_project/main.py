# adding an algorithm for cutting out names somehow?
# Somehow increasing the clues given at each guess
# Is the sentence real or generated? With SpaCy sentence structure for each Book
# Better wrapping it all up into one game with more replayability
# Including more books, uploading own books somehow?, score, leaderboard. More like Wordle? (Random book upload should already work) (Making Leaderboard global?)
# Comparing similar sentences from different books (Which is which?)?
# For better sentence generation: Increasing word relation structure to four instead of bigram
# do research on bigrams
# Using word ranking from week 3 to find representative word for. Would have to be unusual words just typical
# for the book (Different levels: 0.0-0.4;0.5-0.8; 0.9-1)
# Compare word frequency in book with frequency in English literature in general (finding library)
# Focus on
# noun chunks entity detection (finding way to detect the right words ex. scotland yard not seen as name – combining it with frequency)
# first make analysis and then think about which words are dangerous and which arent
# somehow making parameters to automate the noun chunk elimination
# but checking first myself
# disclaimer for custom books (certain workflows only happening on my prechosen books)
# look into gamification?
# gioving them false information ex. three generated sentences, two give clues, one is wrong!
# Adding the time it took to play instead of the time you finished playing. Maybe some kind of timer but not too annyoing
# Maybe saying if youre ta<king too long
# also rewarding in the end if someone is great to not just opunish them^

# guess only works if correct letter by letter and capitalisation.
# Ask if tutorial is needed at the beginning
# add quadrigrams
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import time
import random
from collections import defaultdict
from collections import Counter
from datetime import datetime
import os
import json
print("loading game...")
nlp = spacy.load("en_core_web_md")
books = [ ]
os.listdir("books")
for b in os.listdir("books"):
    books.append(b)


TICK = 1.5
clues = 0
d = False
random_choice = None
vocab_from_file = []
top_names = []
flag = False

class LeaderBoard:
    def __init__(self):
        self.entries = []
        try:
            with open("leaderboard.json", "r", encoding="utf-8") as f:
                board = json.load(f)
            self.entries = board
        except json.JSONDecodeError:
            self.entries = []
    def add(self, name, book, score):

        played_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entries.append(
            {"name": name, "book": book, "clues": score, "time": played_at}
        )
        self.entries.sort(key=lambda e: (-e["clues"], e["time"]), reverse=True)
        with open("leaderboard.json", "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2)

    def show(self):
        print("––– LEADERBOARD –––")
        for i, e in enumerate(self.entries, start=1):
            print(f"{i}. {e['name']} | {e['book']} | clues: {e['clues']} | time: {e['time']}")

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

    return top

def gamestart():
    global random_choice, vocab_from_file, flag, clues, transitions, tokens, top_names, doc
    random_choice = random.choice(books)
    with open("../final_project/books/" + random_choice, encoding="utf8") as f:
        text = f.read()
    doc = nlp(text)

    generic_replacements = {
        "PERSON": ["the man", "the woman", "Character", "Person", "the figure", "the stranger"]
    }

    anonymized_text = text
    for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
        if ent.label_ == "PERSON":
            replacement = random.choice(generic_replacements["PERSON"])
            anonymized_text = (anonymized_text[:ent.start_char] +
                               replacement +
                               anonymized_text[ent.end_char:])

    doc = nlp(anonymized_text)
    stop_extras = ["Baloo", "Two Tails", ] # all missed person names and too easy words i encounter
    STOP_WORDS.update(stop_extras) # during testing will be added here
    vocab_from_file = list({
        token.text.lower()
        for token in doc
        if not token.is_stop and token.is_alpha and token.has_vector
    })
    flag = True
    clues = 0
    tokens = [t.text for t in doc if not t.is_space]
    transitions = defaultdict(list)
    for w1, w2 in zip(tokens, tokens[1:]):
        transitions[w1].append(w2)
def generate_sentence(max_len=20):
    current = random.choice([w for w in tokens if w[0].isupper()])
    sentence = [current]

    for _ in range(max_len - 1):
        next_words = transitions.get(current)
        if not next_words:
            break
        current = random.choice(next_words)
        sentence.append(current)
        if current.endswith(('.', '!', '?')):
            break

    return " ".join(sentence)

def play_game():
    global flag, clues, d
    won = False
    flag2 = False
    gamestart()
    lb = LeaderBoard()
    print("++++++++++++++++++++++++++++++++++")
    print("Welcome to the Book Guessing Game!")
    time.sleep(TICK)
    print("You will have to guess a random book out of 5 available by the tone used")
    time.sleep(TICK)
    print("You can gain insights through different actions, each penalising you with clue points")
    time.sleep(TICK)
    print("The less clue points you have, the better")
    time.sleep(TICK)
    print("1. Action: Entering words to the AI. It will find 5 words out of the book semantically most related to it")
    time.sleep(TICK)
    print("The NLP AI will assign a number to these words based on how strongly it thinks they fit to the word")
    time.sleep(TICK)
    print("Example:")
    print("word = house. Words by AI = 'Mansion' (1.003), 'castle' (0.921), \n 'room' (0.850), 'shed' (0.842), 'live' (0.770)")
    print("conclusion: The book has a setting with castles and mansions in it")
    time.sleep(TICK)
    print("stop words (common non-descriptive words like 'I' and 'the') are filtered out of the book, as they do not add any evidence")
    time.sleep(TICK)
    print("This is worth 0.5 clues per use")
    time.sleep(TICK)
    print("Alternatively, you can let the game generate a sentence containing words of the book")
    time.sleep(TICK)
    print("The sentence is nonsentical, but it can give you insight on the books tone (its worth 1 clue)")
    time.sleep(TICK)
    print("finally, you can let the program list you the 5 most used non-stop words of the book (2 clues penalty)")
    time.sleep(TICK)
    print("You didnt understand this tutorial?")
    time.sleep(TICK * 0.5)
    print("Well, just try learning by doing, I guess!")
    print("List of books:")
    print(books)
    print("You can add your own books into the 'book' folder for more replayability")
    time.sleep(TICK)
    print("(some features may not be as optimised for this)")


    result = False
    word_count = Counter(
        [token.text.lower() for token in doc if not token.is_stop and token.is_alpha and token.has_vector])
    while flag:

        print("Clues used: " + str(clues))
        word = input('\n(write "s" to name the book in question, write "c" to see a generated sentence in style, write "d" to see the most popular non-stop words of the book \nWord in the grammar of text: ').strip().lower()
        if word == "s":
            result = True
            flag = False
        if word == "c":
            print(generate_sentence())
            clues += 1
        if word == "d":
            if not d:
                print("most common words: \n")
                print(word_count.most_common(10))
                clues += 2
                d = True
            else:
                print("you have already requested the most common words!")

        else:
            neighbor = nearest_neighbors(word, vocab_from_file, 5)
            print(neighbor)
            clues += 0.5


    while result:
        print("Which of the following books is the one in question:")
        print(books)
        book = input("Guess: ")
        if book.lower() == random_choice.lower():
            print("You guessed correctly!")
            print("You won.")
            won = True
            result = False
        if book.lower() not in (b.lower() for b in books):
            print("Your guess seems not to be on the list. Did you spell it correctly?")
        else:
            print("You didn't guess correctly!")
            print("The correct book was " + random_choice)
            won = False
            result = False
    print("Thank you for playing!")
    if won:
        flag2 = True
    while flag2:
        scoring = input("do you want to safe your score?(y/n)")
        if scoring == "y":
            user_name = input("What is your username? ")
            lb.add(user_name, random_choice, clues)
            lb.show()
            flag2 = False
        if scoring == "n":
            print("Ok. Thank you for playing!")
            flag2 = False
    flag = False


while True:
    play_game()
    restart = input("Do you want to play again? (y/n) ").strip().lower()
    if restart == "y":
        clues = 0
        d = False
        continue
    elif restart == "n":
        break
    else:
        print("Unknown input, exiting.")
        break

print("goodbye")
