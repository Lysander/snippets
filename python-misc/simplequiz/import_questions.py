#!/usr/bin/env python

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
    Small script for importing questions from a similar project:
    
        https://bitbucket.org/peekpeak/pyquiz/wiki/Home
    
    Just copy the table body from the "edit"-Mode in a text file and run this
    script.
    
    Thanks for suggesting me those repository!
    
    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import csv
import json
import argparse


def import_questions(filename):
    questions = []
    with open(filename, "r", newline="") as infile:
        reader = csv.reader(infile, delimiter="|")
        for row in reader:
            questions.append(
                {
                    "question": row[3].strip(),
                    "options": list(map(lambda s: s.strip(), row[4:8]))
                })
    return questions


def dump(questions, filename):
    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(questions, outfile, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Import Script.")
    parser.add_argument("csvfilename", metavar="CSVFILE", 
                        help="Input filename with CSV data")
    parser.add_argument("jsonfilename", metavar="JSONFILE", 
                        help="Output filename with JSON data")
    args = parser.parse_args()
    
    dump(import_questions(args.csvfilename), args.jsonfilename)


if __name__ == "__main__":
    main()
