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

guesses = 3
random_choice = None
vocab_from_file = []
flag = False

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
    global random_choice, vocab_from_file, flag, guesses
    random_choice = random.choice(books)
    with open("../week5/books/" + random_choice, encoding="utf8") as f:
        text = f.read()
    doc = nlp(text)
    vocab_from_file = list({
        token.text.lower()
        for token in doc
        if not token.is_stop and token.is_alpha and token.has_vector
    })
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
    print("You can enter 3 words and the AI will find 5 equivalent words taken from the book in question")
    time.sleep(1)
    print("The NLP AI will assign a number to these words based on how strongly it thinks they fit to the word")
    time.sleep(1)
    print("Afterwards, you will have to guess the book!")
    time.sleep(1)
    print("Example:")
    print("word = house. Words by AI = 'Mansion' (1.003), 'castle' (0.921), \n 'room' (0.850), 'shed' (0.842), 'live' (0.770)")
    print("conclusion: The book has a setting with castles and mansions in it")
    time.sleep(1)
    print("stop words (common non-descriptive words like 'I' and 'the') are filtered out of the book, as they do not add any evidence")
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
