import nltk
from nltk.corpus import words
import copy
import random
import os
import sys


class WordleBot():
    def __init__(self):
        """
        Use the `guess()` function that takes inputs of a list containing
        the indexes of each descriptor, a list of guesses the user has.
        """
        self.download_words_silently()

        # Get all 5-letter words
        self.word_bank = [word for word in words.words() if len(word) == 5]

        # Make all words lowercase
        self.word_bank = [word.lower() for word in self.word_bank]

        self.backup_word_bank = self.word_bank

    def download_words_silently(self):
        """
        Silence the terminal output for nltk download
        """
        # Suppress terminal output by redirecting both stdout and stderr
        with open(os.devnull, 'w') as fnull:
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            try:
                sys.stdout = fnull
                sys.stderr = fnull
                nltk.download('words', quiet=True)  # Suppress download output
            finally:
                # Restore original stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr

    def guess(self, green=[], yellow=[], gray=[], guesses=[]):
        '''
        `green` -> should be an entry of all places where letter is correct

        `yellow` -> should be an entry of all places where letter is correct
        but in the wrong place

        `gray` -> should be an entry of all places where letter is incorrect

        All entries should be in the form of a list containing string numbers
            ex: `["135"]`

        '''

        # Remove all words containing any of the gray letters
        remove = []

        gray_letters = self.check_gray_against_green_yellow(gray, green,
                                                            yellow, guesses)

        for word in self.word_bank:
            for letter in gray_letters:
                if letter in word:
                    remove.append(word)
                    break

        for word in remove:
            self.word_bank.remove(word)

        remove = []
        # Remove all letters that don't match with green
        for word in self.word_bank:
            if self.check_greens_against_word(green, guesses, word) is False:
                remove.append(word)

        for word in remove:
            self.word_bank.remove(word)

        # Check if word bank is empty
        if self.word_bank == []:
            return 'E'

        remove = []
        # Remove all words that don't comply with yellow
        for word in self.word_bank:
            if self.check_yellows_against_word(yellow, guesses, word) is False:
                remove.append(word)

        for word in remove:
            self.word_bank.remove(word)

        # Remove words that don't have any of the yellow letters
        remove = []

        yellow_letters = self.get_yellow_letters(yellow, guesses)

        yellow_letters = set(yellow_letters)
        self.word_bank = list(set(self.word_bank))

        # Check if word bank is empty
        if self.word_bank == []:
            return 'E'

        for word in self.word_bank:
            for letter in yellow_letters:
                if letter not in word:
                    remove.append(word)

        remove = set(remove)
        for word in remove:
            self.word_bank.remove(word)

        return random.choice(self.word_bank)

    def check_yellows_against_word(self, yellows, guesses, word):
        '''
        Returns `True` for a word that matches all the yellows

        Returns `False` for a word that doesn't
        '''
        # Copy to prevent anti aliasing
        copied_yellows = copy.deepcopy(yellows)

        for a in range(len(yellows)):
            a = int(a)
            for b in range(len(yellows[a])):
                b = int(b)
                if not word[int(yellows[a][b])] == guesses[a][int(yellows[a][b])]:
                    copied_yellows[a] = copied_yellows[a][1:]  # Remove first number
                    if not copied_yellows[a] == '':
                        return self.check_yellows_against_word(copied_yellows,
                                                               guesses, word)
                else:
                    return False

        if all(x == '' for x in copied_yellows):  # Check if all items empty
            return True

        return False

    def check_greens_against_word(self, greens, guesses, word):
        '''
        Returns `True` for a word that matches all the greens

        Returns `False` for a word that doesn't
        '''
        # Copy to prevent anti aliasing
        copied_greens = copy.deepcopy(greens)

        for a in range(len(greens)):
            a = int(a)
            for b in range(len(greens[a])):
                b = int(b)
                if word[int(greens[a][b])] == guesses[a][int(greens[a][b])]:
                    copied_greens[a] = copied_greens[a][1:]  # Remove first number
                    if not copied_greens[a] == '':
                        return self.check_greens_against_word(copied_greens,
                                                              guesses, word)
                else:
                    return False

        if all(x == '' for x in copied_greens):  # Check if all items empty
            return True

        return False

    def get_gray_letters(self, gray, guesses):
        gray_letters = []

        for i in range(len(gray)):
            for letter_place in gray[i]:
                letter_place = int(letter_place)
                gray_letters.append(guesses[i][letter_place])

        return gray_letters

    def get_yellow_letters(self, yellow, guesses):
        yellow_letters = []

        for i in range(len(yellow)):
            for letter_place in yellow[i]:
                letter_place = int(letter_place)
                yellow_letters.append(guesses[i][letter_place])

        return yellow_letters

    def check_gray_against_green_yellow(self, gray, green, yellow, guesses):
        '''
        Checks all gray letters against the green and yellow letters
        to make sure none of the green/yellow letters end up in the gray
        section aswell.

        Returns revised set of `gray_letters`
        '''

        green_letters = []

        for i in range(len(green)):
            for letter_place in green[i]:
                letter_place = int(letter_place)
                green_letters.append(guesses[i][letter_place])

        yellow_letters = self.get_yellow_letters(yellow, guesses)
        gray_letters = self.get_gray_letters(gray, guesses)

        combined = yellow_letters + green_letters

        for letter in combined:
            if letter in gray_letters:
                gray_letters.remove(letter)

        return gray_letters

    def calculate_gray_left(self, last_green, last_yellow):
        '''
        Calculates which numbers are left after the green and yellow have been
        entered.

        Both entries should be a string.
        '''

        combined = last_green + last_yellow
        total_numbers = '01234'
        gray = ''

        for number in total_numbers:
            if number not in combined:
                gray = gray + number

        return gray

    def word_fail(self, word):
        '''
        If a word is not in a word list, this function will remove it from the
        overall list.
        '''

        if word in self.word_bank:
            self.word_bank.remove(word)

    def reset(self):
        self.word_bank = self.backup_word_bank
