#!/usr/bin/env python
# if you don't use Arch Linux then chnage the She-bang to `python3`

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# 

"""
    ~~~~~~~~~~
    simplequiz
    ~~~~~~~~~~
    
    Simple Module that enables one to play a quiz like those typical
    quizshows on TV.
    
    Questions can be loaded from an external JSON-File.
    
    A questionpool consists of a list of questions. Each question is
    defined by a dictionary like this:
    
        {
            "question": "question text", 
            "options": [correct_answer, false_answer_1, false_answer_2, ...]
        }
    
    The right answer must always be the at the first index of the list.
    
    You can have arbitrary amount of answers. The maximum is simply 
    limited by the length of your naming pattern. This pattern could
    be static, like the well knwon "ABCD" one, or even dynamic and increasing
    each level one avances. like "123" for the first level, "1234" for the
    second level and so on.
    
    You can limit the amount of questions via an iterable `levels` in the
    `play` function. Think of amounts of money that can be won for example.
    
    This module is delivered with some demo questions, so one can play
    immediately. Have fun :-)

    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import argparse
import random
import itertools


DEMO_QUESTIONS = [
    {
        "question": "Was ist eine Programmiersprache?",
        "options": ["Python", "Boa", "Natter", "Viper", "Blindschleiche"]
    },
    {
        "question": "In welcher deutschen Stadt wurde der Reichstag verhüllt?",
        "options": ["Berlin", "Hamburg", "Bonn", "Duisburg", "Köln", "Bremen"]
    },
    {
        "question": "Wann gewann die deutsche Herren Fußballnationalmannschaft"
                    " keinen WM- / EM-Titel?",
        "options": ["1986", "1990", "1954", "1996", "1972", "1980"]   
    },
    {
        "question": "Welches war das Flagschiff von Lord Nelson während der"
                    " Schlacht von Kopenhagen 1802?",
        "options": ["Elephant", "Victory", "Captain", "Agamemmnon", 
                    "Foudroyant"]   
    }
]


def set_answers(questions):
    """
    Determines the correct answer from the given "raw questions". The correct
    answer must be stored as first element of the option list for simplicity.
    One has to call this every time before passing the question list to the
    `play` function. Removes the correct answer from the `options` list.
    
    :param question: the raw list of questions
    
    :returns: the updated list of questions with the `answer` entry.
    """
    for question in questions:
        question["answer"] = question["options"].pop(0)


def load(filename):
    """
    This function just loads the questions from a JSON file, accomplishes
    the correct answers for each question dictionary and returns the whole
    question list.
    
    :param filename: path to the JSON file.
    
    :returns: list of questions
    """
    with open(filename, "r") as infile:
        return set_answers(json.load(infile))

        
def simple_ai(prompt, numbering):
    """
    Simple function that enables the computer to play the game itsself.

    :param prompt: string that is printed as prompt.
    :param numbering: the numbering iterable
    
    :returns: the string chosen by the computer
    """
    choice = random.choice(numbering)
    print(prompt, choice)
    return choice


def get_user_input(prompt, numbering):
    """
    Gets the user input and validates, whether it is covered by the
    numbering string.
    
    This is default input function for the human player.
    
    :param prompt: string that is printed as prompt.
    :param numbering: the numbering iterable
    
    :returns: the string given by the user
    """
    while True:
        user_input = input(prompt).upper()
        if user_input in numbering:
            return user_input
        else:
            print("Nur Eingaben aus dem Bereich '{}' erlaubt".format(
                  ",".join(numbering)))


def abcd_numbering():
    """
    The 'classic' numbering for a famous quizshow ;-)
    """
    return "ABCD"
    

def word_numbering():
    """
    Just a proove of concept that numbering functions with all kind of objects.
    """
    return ["ONE", "TWO", "THREE", "FOUR"]


def increasing_numbering(start):
    """
    Generates a function that generates a string with numeric numbers 
    starting at `start`. The generated function increases the numbers at 
    each call.
    """
    def count():
        for n in itertools.count(start + 1):
            yield "".join(map(str, range(1, n)))
    return count().__next__


def get_random_options(all_options, answer, numbering):
    """
    Generates a list of answer options from the given options. Merges the
    shuffled sub list with the correct answer and shuffles that list again
    resulting in a complete random option list containing the correct answer.
    
    The size depends on the length of the numbering string.
    
    :returns: list
    """
    random.shuffle(all_options)
    options = all_options[:len(numbering)-1]
    options.append(answer)
    random.shuffle(options)
    return options

    
def play(questions, levels, input_func, numbering_func):
    """
    The core game function. It poses a question and evaluates the given answer
    until all levels are accomplished.
    
    :param questions: list of questions
    :param levels: iterable of levels
    :param input_func: callable that delivers one item of the numbering as
                       return value. Takes a info string and the numbering 
                       string as parameters.
    :param numbering_func: a callable which delivers an iterable of indices,
                           which are used to prefix each answering option and
                           determine the given answer.
    """
    random.shuffle(questions)
    for level, question in zip(levels, questions):
        print("\nFür {}€: {}\n".format(level, question["question"]))
        numbering = numbering_func()
        options = get_random_options(question["options"], question["answer"],
                                     numbering)
        choices = dict(zip(numbering, options))
        answer_char = numbering[options.index(question["answer"])]
        for char in numbering:
            print("  {}) {}".format(char, choices[char]))
        user_input = input_func("\nIhre Wahl? ", numbering)
        if choices[user_input] != question["answer"]:
            print("\nFalsch! Antwort {} wäre richtig gewesen. "
                  "Sie haben leider verloren.".format(answer_char))
            return
        else:
            print("\nRichtige Antwort! Weiter zu nächsten Frage")
    print("\nGlückwunsch! Sie haben {}€ gewonnen.".format(level))


def main():
    parser = argparse.ArgumentParser(description='Ein einfaches Quiz.')
    parser.add_argument('-q', "--questions", metavar="FILE", 
                        help='a JSON file with questions')
    parser.add_argument("-ai", action="store_true", 
                        help="Let the Computer play")
    parser.add_argument("-n", "--numbering", metavar="NUMBERING", 
                        choices=["ABCD", "WORD", "INC"], default="ABCD",
                        help="The numbering function."
                             "Chose one of %(choices)s (default: %(default)s)")
    args = parser.parse_args()
    
    # set up the questions
    if args.questions:
        questions = load(args.questions)
    else:
        questions = DEMO_QUESTIONS
        set_answers(questions)
    
    # set up the input function (human or computer)
    if args.ai:
        input_func = simple_ai
    else:
        input_func = get_user_input
        
    # set up the naming scheme
    numbering_func = {
        "ABCD": abcd_numbering,
        "WORD": word_numbering,
        "INC": increasing_numbering(2)
    }[args.numbering]
    
    # play the game :-)
    play(questions, (100, 200, 500, 1000), input_func, numbering_func)


if __name__ == "__main__":
    main()