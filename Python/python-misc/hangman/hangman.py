#!/usr/bin/env python2
# coding: utf-8

#
#  Copyright (C) 2010  Christian Hausknecht
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    ~~~~~~~~~~
    hangman.py
    ~~~~~~~~~~
    
    Simple module that implements the well known Hangman game.
    
    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import argparse
from random import choice
from string import ascii_lowercase


WORDS = [
    u"Salamipizza",
    u"Linienschiff",
    u"Python"
]


def get_masked_word(word, guessed_chars):
    """
    function to compute the representation of the word with empty spaces ('_') 
    at positions where the char is not yet guessed.
    
    :params word: unicode string to guess
    :params guessed_chars: list of unicode chars
    
    :returns: unicode
    """
    return u"".join(char if char.lower() in guessed_chars else "_" 
                    for char in word)


def play(word, lifes):
    """
    core game function. The player is asked for entering a char in order to
    accomplish the searched word as long as lifes is not zero. For each fail
    guess lifes is decreased by one.
    
    If the word is guessed, it returns `True`. 
    If all lifes are lost returns `False`.
    
    :param word: unicode string of the word to guess
    :param lifes: int of fail gusses one has
    
    :returns: bool
    """
    guessed_chars = set()
    needed_chars = set(word.lower())
    print "Suchwort: {}".format(get_masked_word(word, guessed_chars))
    while lifes:
        print u"Geratene Buchstaben: {}, Leben: {}"\
                .format(get_masked_word(ascii_lowercase, guessed_chars), lifes)
        guessed_char = raw_input(u"\nDein naechster Buchstabe? ").lower()
        guessed_chars.add(unicode(guessed_char))
        print "\nSuchwort: {}".format(get_masked_word(word, guessed_chars))
        if not guessed_char in word.lower():
            lifes -= 1
        # "<=" is the `issubset` operator!
        if needed_chars <= guessed_chars:
            return True
    return False


def main():
    parser = argparse.ArgumentParser("Play a game of 'hangman'")
    parser.add_argument("-l", "--lifes", type=int, default=5,
                        help="lifes you have for guessing one word.")
    
    args = parser.parse_args()

    word = choice(WORDS)
    win_state = play(word, args.lifes)
    
    # just a pretty evaluation of a game :-)
    print {
        True: u"\nGratulation, du hast das Wort erraten!",
        False: u"\nDas war wohl nichts! Das Wort hieß: {0}"\
                .format(get_masked_word(word, ascii_lowercase))
    }[win_state]


if __name__ == "__main__":
    main()
