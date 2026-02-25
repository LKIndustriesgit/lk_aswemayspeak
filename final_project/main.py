# main code for book guesser
# libraries:
import spacy  # For book style analysis
from spacy.lang.en.stop_words import STOP_WORDS  # filtering out stop words
import time  # for counting time and freezing it (text scrolling)
import random  # for random book choice
from collections import Counter  # for counting how often a word appears in the text (most common word listing)
import os  # For accessing book folder (custom book support)
import json  # For generating an external leaderboard file working throughout different runs of the program
import markovify  # For sentence generation (real ngrams!!!)

print("loading game...")  # to show the player that something is actually happening
nlp = spacy.load("en_core_web_md")  # Loading the NLP AI
books = []
os.listdir("books")  # finding content of books folder
for b in os.listdir("books"):
    books.append(b)  # adding all contents to empty books list

# constants and variables that need definitions
TICK = 2.5  # Pace of tutorial
clues = 0
d = False  # whether player has used most common word listing  (one time use)
random_choice = None  # to be filled with chosen book from list
vocab_from_file = []  # Here, the words from the book in question will be saved for semantic similarity analysis


# creating the leaderboard as a class, because classes can have different functions related to one object
class LeaderBoard:
    def __init__(self):
        self.entries = []  # the object itself is a list
        try:
            with open("leaderboard.json", "r", encoding="utf-8") as f:
                board = json.load(f)  # fillable with leaderboard JSON file, if content available
            self.entries = board
        except json.JSONDecodeError:
            self.entries = []  # otherwise, the list stays empty

    def add(self, name, book, score):  # adding entries to leaderboard
        self.entries.append(
            {"name": name, "book": book, "clues": score, "time": elapsed, }
            # all important information is already saved in vars, time is saved the moment one tries to guess the book
        )
        self.entries.sort(
            key=lambda e: (-e["clues"], -e["time"]))  # sorting the leaderboard after fewest clues and fastest time
        with open("leaderboard.json", "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2)  # opening the leaderboard to add the new entries, this time as 'w',
            # even creating a new file if no file exists in the first place

    def show(self):  # actually depicting the leaderboard ingame
        print("––– LEADERBOARD –––")
        for i, e in enumerate(self.entries,
                              start=1):  # gives each entry a number, starting with 1 (entries are already sorted)
            t = e.get("time")  # gets the time variable from the entries
            minutes = int(t // 60)  # converts it to minutes
            seconds = round(t % 60, 1)  # takes the remainder and lists it as seconds
            time_str = f"{minutes}:{seconds:5.1f}"  # putting both together and
            # depicting the seconds always with five characters (a bit more visually consistent)
            # and one number after the decimal point (guesses can get fast if youre good)
            print(
                f"{i}. {e['name']} | {e['book']} | clues= {e['clues']} | time= {time_str}")  # one whole eladerboard line


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


def gamestart():  # actual logic of starting a game
    global random_choice, vocab_from_file, tokens, doc, anonymised_text  # making global variables accessible inside of the game logic
    random_choice = random.choice(books)  # chosing the book in question
    with open("../final_project/books/" + random_choice, encoding="utf8") as f:
        text = f.read()
    doc = nlp(text)  # running it through AI

    generic_replacements = {
        "PERSON": ["the man", "the woman", "Character", "Person", "the figure", "the stranger"]
    }  # using this generic replacements for character names
    stop_extras = ["Baloo", "Bagheera", "Two Tails", "shoggoth", "sibyl", "chapter", "section", "socrates,—those",
                   "polemarchus,—thrasymachu", "polemarchus", "lachesis", "sophist", "hellene", "kaa",
                   "nag", "jungle"]  # all missed person names and too easy words I encounter + words from algorithm
    # during testing will be added here
    anonymised_text = text  # putting book content into new var to distiguish between anonymised and pre-anonymised text
    for ent in sorted(doc.ents, key=lambda e: e.start_char,
                      reverse=True):  # sorting the vocab after SpaCy entities (persons, adjectives, verbs)
        # reversing it is important because text length changes through anonymisation. If the last word is changed first,
        # no detected entities before it are affected by differing length
        if ent.label_ == "PERSON" or ent.text.lower() in stop_extras:  # If a word is part of the undesired words (names and extra stop words)
            replacement = random.choice(
                generic_replacements["PERSON"])  # randomly choose a generic person descriptor from the list
            anonymised_text = (
                    anonymised_text[:ent.start_char] +  # the text before the detected entity
                    replacement +  # putting the replacement in between
                    anonymised_text[ent.end_char:]  # the text after the detected entity
            )

    doc = nlp(anonymised_text)  # running the anonymised text through the NLP AI
    STOP_WORDS.update(
        stop_extras)  # also updating the stop words with the new words – important for listing the most common words
    vocab_from_file = list({  # preparing all of the text for the semantic similarity algorithm
        token.text.lower()  # putting every word in lower case
        for token in doc  # if it is part of the anonymised text run through the AI
        if not token.is_stop and token.is_alpha and token.has_vector
        # and if its not a stop word, if it consists of letters (alpha) and has a relation to the other words (vector)
    })


# GAMEPLAY LOOP
def play_game():
    global clues, d, anonymised_text  # porting the clues, usage of word list (d) and the book text to the gameplay loop
    won = False  # resetting winning loop
    flag2 = False  # resetting leaderboard loop
    result = False  # resetting whether the player has given a guess
    gamestart()  # calling the last funtion
    lb = LeaderBoard()  # creating a leaderboard object
    text_model = markovify.Text(anonymised_text, state_size=3)  # creating a markov trigram model for text generation
    print("++++++++++++++++++++++++++++++++++")
    print("Welcome to the Book Guessing Game!")
    tut = True  # tutorial loop
    while tut:
        tutorial = input("Do you want a tutorial? (y/n)")
        if tutorial == "y":
            print("You will have to guess a random book out of 5 available by the tone used")
            time.sleep(TICK)  # text kind of naturally appearing
            print("You can gain insights through different actions, each penalising you with clue points")
            time.sleep(TICK)
            print("The less clue points you have, the better")
            time.sleep(TICK)
            print(
                "1. Action: Entering words to the AI. It will find 5 words out of the book semantically most related to it")
            time.sleep(TICK * 2)
            print("The NLP AI will assign a number to these words based on how strongly it thinks they fit to the word")
            time.sleep(TICK)
            print("Example:")
            print(
                "word = house. Words by AI = 'Mansion' (1.003), 'castle' (0.921), \n 'room' (0.850), 'shed' (0.842), 'live' (0.770)")
            print("conclusion: The book has a setting with castles and mansions in it")
            input("Press ENTER to continue...")  # input pauses to not make the text overwhelming
            print(
                "stop words (common non-descriptive words like 'I' and 'the') are filtered out of the book, as they do not add any evidence")
            time.sleep(TICK)
            print("So are character names like 'Dorian Gray' or 'Frankenstein', as they give too much insight")
            time.sleep(TICK)
            print("They are instead replaced by generic character descriptions like 'The Person' or 'woman'")
            time.sleep(TICK)
            print("The first type of action is worth 0.5 clues per use")
            time.sleep(TICK)
            print("Alternatively, you can let the game generate a sentence containing words of the book")
            time.sleep(TICK)
            print("The sentence is nonsentical, but it can give you insight on the books tone (its worth 1 clue)")
            input("Press ENTER to continue...")
            print(
                "finally, you can let the program list you the 5 most used non-stop words of the book (2 clues penalty)")
            time.sleep(TICK)
            print("If you guess the book correctly, your score will be saved on a leaderboard")
            time.sleep(TICK)
            print(
                "The game will also keep track of the the time it took you to guess the correct book, and it will warn you if you take too long")
            time.sleep(TICK * 2)
            print("So you better hurry!")
            time.sleep(TICK)
            print("You didnt understand this tutorial?")
            time.sleep(TICK * 0.5)
            print("Well, just try learning by doing, I guess!")
            time.sleep(TICK * 0.5)
            print("List of books:")
            print(books)
            print("You can add your own books into the 'book' folder for more replayability")
            time.sleep(TICK)
            print("(some features may not be as optimised for this)")
            break
        elif tutorial == "n":
            break
        else:
            print("Unknown command, try again.")

    word_count = Counter(  # creating a word counter for most common words
        [token.text.lower() for token in doc if not token.is_stop and token.is_alpha and token.has_vector])
    # only counting tokens of the anonymised text if they are not a stop word, but consist of letters (alpha), and have relations to other tokens (vector)
    start = time.perf_counter()  # starting the counter to meassure the time played

    # gameplay loop
    flag = True  # starting the gameplay loop
    while flag:

        print("Clues used: " + str(clues))
        word = input(
            '\n(write "s" to name the book in question, write "c" to see a generated sentence in style, write "d" to see the most popular non-stop words of the book \nWord in the grammar of text: ').strip().lower()
        if word == "s":
            result = True  # switching to result loop if user tries to guess book
            flag = False
            global elapsed
            elapsed = time.perf_counter() - start  # stopping the gameplay time (elapsed time - start time = time taken)
        if word == "c":
            print(text_model.make_sentence(
                tries=100))  # generating an ngram, with 100 tries so that no empty sentences appear
            clues += 1
        if word == "d":
            if not d:
                print("most common words: \n")
                print(word_count.most_common(10))  # listing the most common words through the counting logic
                clues += 2
                d = True  # remembering that this action has already been done to prevent the player from getting redundant information
            else:
                print("you have already requested the most common words!")

        else:  # if the player enters a word which is none of the above
            if len(word) > 1:  # if it's longer than a single letter (important, as the commands above kept also triggering the semantic similarity logic)
                neighbor = nearest_neighbors(word, vocab_from_file,
                                             5)  # generating the five nearest neighbors (see nearest neighbors logic above)
                print(neighbor)
                clues += 0.5
        if time.perf_counter() - start > 300 and not result:
            print("HURRY UP! You are too slow.")  # a warning after 5 minutes

    # guessing logic
    while result:
        print("Which of the following books is the one in question:")
        print(books)  # listing all books again to remind player of possible answers
        book = input("Guess: ")
        if book.lower() == random_choice.lower():  # comparing lower versions of words to prevent losing because of capitalisation mistakes
            print("You guessed correctly!")
            print("You won.")
            won = True
            result = False
        if book.lower() not in (b.lower() for b in
                                books):  # player can guess again if his answer is not part of the books – preventing spelling mistakes
            print("Your guess seems not to be on the list. Did you spell it correctly?")
        else:
            if book.lower() != random_choice.lower():  # only if the book is part of the list, but not the book in question
                print("You didn't guess correctly!")
                print("The correct book was " + random_choice)
                won = False  # you lose
                result = False
    print("Thank you for playing!")

    # winning logic
    if won:
        flag2 = True
    while flag2:
        # leaderboard loop
        scoring = input("do you want to safe your score?(y/n)")
        if scoring == "y":
            user_name = input("What is your username? ")
            lb.add(user_name, random_choice, clues)  # adding all saved information + username to leaderboard
            lb.show()  # showing the leaderboard once
            flag2 = False  # breaking leaderboard logic
        if scoring == "n":
            print("Ok. Thank you for playing!")
            flag2 = False
    flag = False  # breaking gameplay loop


# main game loop
while True:
    # resetting clues and common words action at the beginning of games
    clues = 0
    d = False
    play_game()  # gameplay function
    restart = input("Do you want to play again? (y/n) ").strip().lower()  # both Y/N and y/n possible
    if restart == "y":
        continue
    elif restart == "n":
        break
    else:
        print("Unknown input, exiting.")
        break

print("goodbye")
