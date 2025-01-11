from wordle_bot import WordleBot

bot = WordleBot()

green = []
yellow = []
gray = []
guesses = []

guesses.append(input("Please enter your first guess: "))
green.append(input("Please enter the places of green letters (ex: AudIO -> 034): "))
yellow.append(input("Please enter the places of yellow letters (ex: AudIO -> 034): "))
gray.append(bot.calculate_gray_left(green[-1], yellow[-1]))

fail = 'None'

for i in range(5):
    while not (fail == '' or fail[0] == '/'):
        chosen_word = bot.guess(green, yellow, gray, guesses)

        if chosen_word == 'E':
            print('ERROR: Word not listed')
            exit()

        fail = input(f'Try the word (if word fails, type a letter and press enter. If you have a different word, type "/<your_word>"): {chosen_word}')
        bot.word_fail(chosen_word)

    if not fail == '':
        if fail[0] == '/':
            guesses.append(fail[1:])  # Adds everything except the first char (/)
    else:
        guesses.append(chosen_word)
    fail = 'None'
    green.append(input("Please enter the places of green letters (ex: AudIO -> 034): "))
    yellow.append(input("Please enter the places of yellow letters (ex: AudIO -> 034): "))
    gray.append(bot.calculate_gray_left(green[-1], yellow[-1]))
