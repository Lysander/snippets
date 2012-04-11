#!/usr/bin/env python2
# coding: utf-8

#
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       


"""
    ~~~~~~~~
    scale.py
    ~~~~~~~~
    
    A simple weight measurement tool.
    
    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
    
"""

from __future__ import division

import json
import argparse
import math
from datetime import date
from itertools import izip, chain
from operator import itemgetter


VALUE = itemgetter("value")
#CHANGE = itemgetter("change")


def calc_bmi(weight, height):
    """
    calculates the Body Mass index (BMI) of a person.
    Needs weight in Gramm and heightin cm.
    
    :returns: float
    """
    return 10 * weight / (height ** 2)


def weights(values):
    """
    iterates over the weight-entries of the database
    
    :returns: int
    """
    for item in values:
        yield item["value"]


def changes(values):
    """
    calculates a sequence with differences between each entry. It 
    starts with the zero difference as the first entry has no
    predecessor.
    
    :returns: list of differences
    """
    start = values[0]["value"]
    pairs = izip(chain((start,), weights(values)), weights(values))
    for a,b in pairs:
        yield b - a


def difference(values):
    """
    calculates the difference between the maximum and minimum weight
    entry.
    
    :returns: int
    """
    return VALUE(max(values, key=VALUE)) - VALUE(min(values, key=VALUE))


def average(values):
    """
    calculates the average loss of weight per day. Positive values
    represent a loss, negative values an increasement.
    
    :returns: float
    """
    return sum(changes(values)) / (len(values) - 1)


def get_limit(values, func=max):
    """
    searches an extreme value (``min`` oder ``max``) in database.
    
    :returns: string with describing text
    """
    return u"{} Gewicht: {value} am {date}".format(func.__name__, 
            **func(values, key=VALUE)) 


def dashboard(target, height, values):
    print u"--- Verlauf: ---"
    for item, change in izip(values, changes(values)):
        item["change"] = change
        print u"{date}: {value}, {change}".format(**item)
    print
    print "--- Extremwerte: ---"
    print get_limit(values, func=max)
    print get_limit(values, func=min)
    print
    print u"--- Durchschnitt: ---"
    avg = average(values)
    print u"{}g pro Tag {}".format(abs(avg), 
            "abgenommen" if avg < 0 else "zugenommen")
    diff = difference(values)
    print "Gewichts{} gesamt: {}g".format(
            "verlust" if diff > 0 else "zunahme", abs(diff))
    print
    print u"--- Zielwert: ---"
    rest = VALUE(values[-1]) - target
    print "Noch {}g bis zum Zielwert".format(rest)
    print "Noch {} Tage bis zum Erreichen".format(
            int(math.ceil(abs(rest / avg))))
    print "aktueller BMI: {}".format(calc_bmi(values[-1]["value"], height))
    

def add(values, value):
    values.append({"date": str(date.today()), "value": value})


def load(filename):
    try:
        with open(filename, "r") as infile:
            data = json.load(infile)
            return data["target"], data["height"], data["values"]
    except IOError:
        return {"target": 0, "height": 0, "values": []}


def dump(filename, target, height, values):
    data = {"target": target, "height": height, "values": values}
    with open(filename, "w") as outfile:
        return json.dump(data, outfile, indent=4)


def main():
    parser = argparse.ArgumentParser(description=u"A simple "\
            "weightening measurement software")
    parser.add_argument("filename", metavar="FILE",
            help=u"filename of JSON dump file with weight data.")
    parser.add_argument("--add", metavar="WEIGHT", type=int,
            help=u"add a new weight entry in Gramm.")
    args = parser.parse_args()
    
    
    target, height, values = load(args.filename)
    
    if args.add:
        add(values, args.add)
        dump(args.filename, target, height, values)
    
    dashboard(target, height, values)
    

if __name__ == '__main__':
    main()
