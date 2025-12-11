import spacy
import time
import random

print("loading game...")
nlp = spacy.load("en_core_web_md")

books = [
    'At the Mountains of Madness',
    'The Picture of Dorian Gray',
    'Frankenstein',
    'The Jungle Book',
    'Platos Republic',
]

# global state for one game
guesses = 3
random_choice = None
vocab_from_file = []
flag = False

def nearest_neighbors(target, vocab, k=5):
    """
    Find the nearest neighbors of a target word within a vocab
    vocab needs to be a list of strings
    """
    query = nlp(target)[0]  # token
    scores = {}
    for w in vocab:
        if w == target:  # skip the same word
            continue
        token = nlp.vocab[w]
        if token.has_vector:
            score = query.similarity(token)
            scores[w] = score
    top = sorted(scores.items(), key=lambda x: -x[1])[:k]
    return top

def gamestart():
    global random_choice, vocab_from_file, flag, guesses
    random_choice = random.choice(books)
    with open("../week5/books/" + random_choice, encoding="utf8") as f:
        text = f.read()
    # you can clean this later; for now keep your split
    vocab_from_file = text.split(" ")
    flag = True
    guesses = 3

def play_game():
    global flag, guesses

    gamestart()

    print("++++++++++++++++++++++++++++++++++")
    print("Welcome to the Book Guessing Game!")
    time.sleep(1)
    print("You will have to guess a random book out of 5 available by the tone used")
    time.sleep(1)
    print("You can enter 3 words and the AI will find equivalent words taken from the book in question")
    time.sleep(1)
    print("Afterwards, you will have to guess the book!")
    time.sleep(1)
    print("You didnt understand this tutorial?")
    time.sleep(0.5)
    print("Well, just try learning by doing, I guess!")
    print("List of books:")
    print(books)

    result = False

    while flag:
        if guesses > 0:
            print("Guesses left: " + str(guesses))
            word = input('\n(write "s" to stop)\nWord in the grammar of text: ').strip().lower()
            if word == "s":
                flag = False
            else:
                neighbor = nearest_neighbors(word, vocab_from_file, 5)
                print(neighbor)
                guesses -= 1
        else:
            result = True
            flag = False

    if result:
        print("Which of the following books is the one in question:")
        print(books)
        book = input("Guess: ")
        if book == random_choice:
            print("You guessed correctly!")
            print("You won.")
        else:
            print("You didn't guess correctly!")
            print("The correct book was " + random_choice)
    print("Thank you for playing!")

# main loop
while True:
    play_game()
    restart = input("Do you want to play again? (y/n) ").strip().lower()
    if restart == "y":
        continue
    elif restart == "n":
        break
    else:
        print("Unknown input, exiting.")
        break

print("goodbye")
