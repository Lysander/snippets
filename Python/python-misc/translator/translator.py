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
    ~~~~~~~~~~~~~
    translator.py
    ~~~~~~~~~~~~~
    
    simple module to translate each characters of a given text into a
    predefined other character. That is implemented by a simple state machine.
    
    It was inspired by the pygments way to implement a lexer:
    http://pygments.org/docs/lexerdevelopment/
    
    A lexer is represented as a dict, with the following structure:

        - state_name:   default and first state has to be named always "root"
                        each state conssists of arbitrary tuples, which
                        represent rules.
        
        A rule consists of the following elements:
        
            - RegExp that must be matched by the given character
            - Charakter that should replace original character, or "#token"
              if you want to keep original character.
            - command to change a state; with possibilities:
                None:           if no change should happen
                "state_name"    change to state with "state_name"
                "#pop"          jump back to last state
    
    Example call:
    ~~~~~~~~~~~~~
    
        echo 'Hallo Welt "hier nicht"' | ./translator.py
        Hallo;Welt;"hier nicht"
    
    
    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>    
"""

import sys
import re
import argparse
import json

#
# default lexer:
# simply subsitute a "Space" by a semicolon but not inside '"'-marked Strings
#
demo_lexer = {
    "root": [
        (r'"', "#token", "string"),
        (r' ', ";", None),
        (r'.', "#token", None)
    ],
    "string": [
        (r'"', "#token", "#pop"),
        (r'.', "#token", None)
    ]
}


def load(filename):
    """
    loads a lexer definition from a JSON file.
    
    :params filename: name of the JSON file.
    
    :returns: dict (lexer)
    """
    with open(filename, "r") as infile:
        return json.load(infile)


def translate(iterable, lexer):
    """
    core function that inherits the state machine.
    
    :params iterable: a iterable (string) that should be transformed
    :params lexer: a dict with the lexer definition
    
    :yields: the transformed token (string)
    """
    stack = []
    state = "root"
    for token in iterable:
        for rules in lexer[state]:
            pattern, value, change = rules
            if re.match(pattern, token, re.DOTALL):
                # Assign replacement character
                replacement = token if value == "#token" else value
                # check if there should be a state change
                if change == "#pop":
                    state = stack.pop()
                elif change:
                    stack.append(state)
                    state = change
                break
        # No rule matched; could also yield a default char then
        else:
            raise Exception(u"No Rule found for token '{}' in state '{}'!"\
                            .format(repr(token), state))
        yield replacement


def main():
    parser = argparse.ArgumentParser("Simple state machine.")
    parser.add_argument("-l", "--lexer",
                        help="JSON file with a lexer definition.")
    parser.add_argument("infile", nargs="?", type=argparse.FileType("r"),
                        default=sys.stdin)
    parser.add_argument("outfile", nargs="?", type=argparse.FileType("w"),
                        default=sys.stdout)

    args = parser.parse_args()
    
    if args.lexer:
        lexer = load(args.lexer)
    else:
        lexer = demo_lexer
    
    for line in args.infile:
        args.outfile.write("".join(translate(line, lexer)))
    
    #TODO: Check if this is really needed?
    args.infile.close()
    args.outfile.close()


if __name__ == "__main__":
    main()
