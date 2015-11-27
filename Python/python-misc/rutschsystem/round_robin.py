#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010 - 2015 Christian Hausknecht (christian.hausknecht@gmx.de)

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

"""
    ~~~~~~~~~~~
    round_robin
    ~~~~~~~~~~~
    
    creates all matches of one group of players so that every player has one
    match against every other one of his group.
"""

__author__ = "Christian Hausknecht (christian.hausknecht@gmx.de)"
__version__ = "0.1"

from collections import deque
from itertools import chain, islice
from pprint import pprint

def round_robin(group, filler="leer"):
    """
    Implementiert den ''round robin'' Algorithmus. S. dazu auch:
    https://de.wikipedia.org/wiki/Rutschsystem
    
    Kernidee ist das Rotieren aller Teilnehmer, bis auf den Gruppenkopf.
    
    Beispiel: group = [1, 2, 3, 4, 5, 6]
    
    1. Durchgang:
    1 2 3
    6 5 4
    (Die Partien stehen in den Spalten codiert, also "1 gegen 6", "2 gegen 5" 
    und "3 gegen 4")
    
    Nun rotieren nach rechts, die 1 bleibt aber stehen!    
    1   2 → 3
      ↗     ↓
    6 ← 5 ← 4
           
    2. Durchgang:
    1 6 2
    5 4 3
    
    Nun wieder rotieren...
    1   6 → 2
      ↗     ↓
    5 ← 4 ← 3
    
    3. Durchgang:
    1 5 6
    4 3 2
    
    usw.
    
    :param group: Liste einer Gruppe
    :param filler: Füll-Objekt bei ungeraden Gruppen
    
    :returns: Liste von Durchgängen
    """
    rounds = []
    igroup = iter(group)
    head = [next(igroup)]
    tail = deque(igroup)
    if not len(tail) % 2:
        tail.append(filler)
    round_count = len(tail)
    matches = (round_count + 1) // 2
    for _ in range(round_count):
        rounds.append(list(zip(islice(chain(head, tail), 0, matches),
                                islice(reversed(tail), 0, None))))
        tail.rotate()
    return rounds

    
def simple_test():
    teams = {
        1: u"Bayern München",
        2: u"Werder Bremen",
        3: u"TSG 1899 Hoffenheim",
        4: u"Bayer Leverkusen",
        5: u"Schalke 04",
        6: u"Hamburger SV",
        7: u"Hannover 96"
    }
    rounds = round_robin(teams.keys())
    for index, round in enumerate(rounds):
        print()
        print("Runde {0}".format(index))
        print("-" * 40)
        for team_a, team_b in round:
            print("{0} vs. {1}".format(teams.get(team_a, "Freilos"),
                                        teams.get(team_b, "Freilos")))
            

def main():
    pprint(round_robin(range(1, 7)))
    print()
    simple_test()
    
    
if __name__ == "__main__":
    main()
