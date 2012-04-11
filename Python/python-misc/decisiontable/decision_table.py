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
    ~~~~~~~~~~~~~~~~~
    decision_table.py
    ~~~~~~~~~~~~~~~~~
    
    Small module to evaluate a given decision table as described in:
    
        http://en.wikipedia.org/wiki/Decision_table
        
    A table must be given as a Dict of the following form:
    
        table = {
            "conditions": ["cond_1", "cond_2", ... ],
            "actions": {"key_1": "action_1", ...},
            "rules": [
                [
                    [<boolean values or None>], 
                    [<keys of actions> or empty]
                ],
                ...
            ]
        }
    
    A `None` in the rules marks a 'don't care'-condition. The number of
    rule entries must match the number of conditions. The number of 
    actions is arbitrary but at least an empty list.
    
    As this structure can be easily transformed into JSON, the module
    provides a `load`-function for that purpose. You should in general
    use a JSON-file for providing a decision-table and not build it
    in your code!
    
    Hint: A `None` is translated into `null` in JSON!
    
    An example JSON-file could look like this. It shows the example
    from the english wikipedia entry:
    
        {
            "conditions": [
                "Printer does not print",
                "A red light is flashing",
                "Printer is unrecognised"
            ],
            "actions": {
                "power": "Check the power cable",
                "usb": "Check the printer-computer cable",
                "software": "Ensure printer software is installed",
                "ink": "Check/replace ink",
                "jam": "Check for paper jam"
            },
            "rules": [
                [
                    [true, true, true],
                    ["usb", "software", "ink"]
                ],
                [
                    [true, true, false],
                    ["ink", "jam"]
                ],
                [
                    [true, false, true],
                    ["power", "usb", "software"]
                ],
                [
                    [true, false, false],
                    ["jam"]
                ],
                [
                    [false, true, true],
                    ["software", "ink"]
                ],
                [
                    [false, true, false],
                    ["ink"]
                ],
                [
                    [false, false, true],
                    ["software"]
                ],
                [
                    [false, false, false],
                    []
                ]
            ]
        }

    .. moduleauthor::  Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import sys
import json
import argparse
from operator import eq
from itertools import starmap


def get_valid_indices(rule):
    """
    Generates an index of those entries in a rule, which are well
    definied. Skips 'don't care'-definitions.
    
    Example:

        (True, False, None) would result in [0, 1]
        (True, None, False) would result in [0, 2]
    
    :yields: int
    """
    for i, _ in enumerate(rule):
        if _ is not None:
            yield i


def is_equal(tuple_, rule):
    """
    Checks pairwise values of the given tuple and rule for equality.
    Skips 'don't care'-definitions in rule.
    
    :returns: True or False
    """
    return all(starmap(eq, (pair for index, pair 
                                 in enumerate(zip(tuple_, rule)) 
                                 if index in get_valid_indices(rule))))


def evaluate(tuple_, table):
    """
    Searches the corresponding rule from the ruleset to the given one.
    Raises an exception if no rule is found.
    
    :returns: index of the ruleset (int), list of action keys
    """
    rules = table["rules"]
    for index, item in enumerate(rules):
        rule, action_keys = item
        if is_equal(tuple_, rule):
            return index, action_keys
    raise Exception("No approriate rule found for {}!".format(tuple_))


def print_result(index, action_keys, table):
    rules, actions, conditions = map(table.get, ("rules", "actions",
                                                "conditions"))
    tuple_ = rules[index][0]
    print("Result:\n-------")
    print("{}. Rule ({}):".format(index+1, ", ".join(map(str, tuple_))))
    print("\nConditions:\n-----------")
    for i, value in enumerate(tuple_):
        print("{} {} ({})".format("*" if value else " ", conditions[i], value))
    print("\nActions:\n--------")
    print("\n".join([actions[key] for key in action_keys]) or "no action")


def load(filename):
    with open(filename, "r") as infile:
        return json.load(infile)


def str_to_booleans(value):
    return [{"T": True, "F": False}[_] for _ in value.upper()]


def main():
    parser = argparse.ArgumentParser(description='Evaluate a decision-table.')
    parser.add_argument('table', metavar="FILE", 
                        help='a JSON file of the decision-table')
    parser.add_argument('rule', metavar="RULE", help='a given rule as String. '
                                'Use "T" for "True" and "F" for "False". '
                                'For example "TTF" for True, True, False.')
    args = parser.parse_args()
    
    table = load(args.table)
    tuple_ = str_to_booleans(args.rule)
    index, action_keys = evaluate(tuple_, table)
    print_result(index, action_keys, table)


if __name__ == '__main__':
    main()
