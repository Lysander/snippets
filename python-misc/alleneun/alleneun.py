#!/usr/bin/env python2
# coding: utf-8

#
#  Copyright (C) 2011  Christian Hausknecht
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
    ~~~~~~~~~~~
    alleneun.py
    ~~~~~~~~~~~
    
    A simple but tricky little game I implemented after discussing a topic
    in this forum thread:
    
        http://forum.ubuntuusers.de/post/3889807/
    
    Goal of the game ist to fill a 3x3 square with completly with markers.
    Each turn the player is asked for a X and Y coordinate to define the
    position where you want to put your marker. All fields in horizontal
    and vertical direction from this field are filled in the following way:
    
        - if a field was empty so far, it gets marked
        - if a field was allready marked, it gets empty again
    
    Here is an example:
    
        0 O O O
        1 O O O
        2 O O O
        0 1 2
        X-Pos: 1
        Y-Pos: 1

        0 O X O
        1 X X X
        2 O X O
        0 1 2        
        X-Pos: 0
        Y-Pos: 0

        0 X O X
        1 O X X
        2 X X O
        0 1 2
    
    The game ends if all fields are filled with markers.
    
    There is a simple AI, which just plays a allready found solution ;-)
    
    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

from itertools import chain, count
from argparse import ArgumentParser


SIZE = 3
EMPTY, FILLED = "O", "X"
CHANGE = {EMPTY: FILLED, FILLED: EMPTY}
CHECK = {EMPTY: False, FILLED: True}


def invert(board, pos):
    x, y = pos
    for offset in xrange(1, 3):
        xmod = (x + offset) % SIZE 
        ymod = (y + offset) % SIZE
        board[ymod][x] = CHANGE[board[ymod][x]]
        board[y][xmod] = CHANGE[board[y][xmod]]
    board[y][x] = CHANGE[board[y][x]]

    
def all_filled(board):
    return all(CHECK[value] for value in chain.from_iterable(board))


def create_board(fill_value=EMPTY):
    return [[fill_value]*SIZE for _ in xrange(3)]

    
def print_board(board):
    print
    for index, line in enumerate(board):
        print "{} {}".format(index, " ".join(line))
    print "  {}".format(" ".join(str(i) for i in xrange(3)))


def ai():
    """
    Simple AI-function with fixed solution.
    """
    def f():
        for pos in ((1, 1), (0, 0), (2, 2), (2, 0), (0, 2)):
            yield pos
    return f().next


def play_human():
    while True:
        try:
            x = int(raw_input("X-Pos: ")) % SIZE
            y = int(raw_input("Y-Pos: ")) % SIZE
        except ValueError:
            print "Bitte nur Integerwerte zwischen 0 und 2 eingeben!"
        else:
            return x, y


def play(player_func):
    board = create_board()
    print_board(board)
    for counter in count(1):
        pos = player_func()
        print "You chose ({}, {})".format(*pos)
        invert(board, pos)
        print_board(board)
        if all_filled(board):
            print "You won in {} moves.".format(counter)
            return


def main():
    parser = ArgumentParser("Play a game of 'all nine'")
    parser.add_argument("-p", "--player", choices=["human", "ai"], 
            default="human", help="Play as 'human' (default) "
                                  "or let the 'ai' play the game.")
    args = parser.parse_args()
    
    play({"human": play_human, "ai": ai()}[args.player])

    
if __name__ == "__main__":
    main()
