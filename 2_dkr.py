# Name          : Piustonen Sophia
# Collaborators : -
# Time spent    : I spent 3 evenings, because while working I was making big pauses to eat:)

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
          'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
          'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1,
          'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0}

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")

    infile = open(WORDLIST_FILENAME, 'r')
    wordlist = []
    for line in infile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.
    The score for a word is the product of two components:
    The first component is the sum of the points for letters in the word.
    The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played
    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    result = 0
    count = 0
    word_lower = word.lower()
    for letter in word_lower:
        count += VALUES[letter]
    result = max(7 * len(word) - 3 * (n - len(word)), 1)
    return result * count


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')
    print()


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    hand['*'] = 1
    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    hand_1 = hand.copy()
    for lit_letter in word.lower():
        if lit_letter in hand_1 and hand_1.get(lit_letter, 0) > 0:
            hand_1[lit_letter] -= 1
    return hand_1


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    word = word.lower()
    if "*" in word:
        for vowel in VOWELS:
            if word.replace("*", vowel) in word_list:
                return True
        else:
            return False
    elif word in word_list:
        for little_letter in word:
            if little_letter not in hand or word.count(little_letter) > hand[little_letter]:
                return False
        else:
            return True
    else:
        return False


def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """

    count = 0
    for n in hand:
        count += hand[n]
    return count


def play_hand(hand, word_list, count_points):
    """
    Allows the user to play the given hand, as follows:

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """

    while calculate_handlen(hand) != 0:
        print("Current Hand:", end=" ")
        display_hand(hand)
        inputings = input("Enter word, or “!!” to indicate that you are finished: ")
        if is_valid_word(inputings, hand, word_list):
            count_points += get_word_score(inputings, calculate_handlen(hand))
            print(f"With the word ' {inputings} 'you've got {get_word_score(inputings, calculate_handlen(hand))}"
                  f" points Scores:  {count_points} points)")
            print(" ")
        elif inputings == "!!":
            break
        else:
            print("This is not valid word. Please choose another word", "\n")
        hand = update_hand(hand, inputings)
    else:
        print()
        print("Ran out of letters.")
    return count_points


def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    try:
        letter_to_be_changed = hand[letter]
    except:
        return hand

    is_true = True
    while is_true:
        new = random.choice(string.ascii_letters.lower())
        if new not in hand:
            del hand[letter]
            hand.update({new: letter_to_be_changed})
            is_true = False

        continue

    return hand


def play_game(word_list):
    """
    Allow the user to play a series of hands
    word_list: list of lowercase strings
    """
    true_value_sec_chnc = True
    true_value_changing_letter = True
    all_points = 0
    number_of_hands = int(input("Input the total number of hands: "))
    while number_of_hands != 0:
        hand = deal_hand(HAND_SIZE)
        print("Current hand: ", end=" ")
        display_hand(hand)
        if true_value_changing_letter and true_value_sec_chnc:
            answer = input("Would you like to substitute a letter?(yes/no): ")
            if answer == "yes":
                letter_to_be_changed = input("Choose the letter to be changed, please: \n")
                hand = substitute_hand(hand, letter_to_be_changed)
                true_value_changing_letter = False
        hand_points = play_hand(hand, word_list, 0)
        if true_value_sec_chnc:
            second_chance = input("Do you want to replay this hand?(yes/no): ")
            if second_chance == 'yes':
                hand_points = play_hand(hand, word_list, 0)
                true_value_sec_chnc = False
            else:
                print("Total score for this hand: ", hand_points)
        all_points += hand_points
        number_of_hands -= 1

    print("Total score:", all_points, end=" ")
    return all_points


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
