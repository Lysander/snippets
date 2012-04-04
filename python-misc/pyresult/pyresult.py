#! /usr/bin/env python2
# -*- coding: utf-8 -*-

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
    ~~~~~~~~
    pyresult
    ~~~~~~~~
    
    a simple script that extracts some sport results from an european
    tv-channel.
    
    TODO: Add support for snooker :-)
    
    .. moduleauthor::  Christian Hausknecht <christian.hausknecht@gmx.de>
"""

from urllib import urlencode
from urllib2 import urlopen
from lxml import etree
from StringIO import StringIO
import sys


#
# URL of the data source
#
URL = u"http://de.eurosport.yahoo.com/"

#
# mapping for the node to fetch from the DOM tree for each kind of sport
#
RESTAB = {
    u"result": u"""//div[@id="ep-livemod-results"]""",
    u"live": u"""//div[@id="ep-livemod-live"]"""
}

#
# kind of boards
#
BOARDS = RESTAB.keys()


class Sport(object):
    """
    baseclass for sport results
    """
    sport = u"Allgemein"

    def __init__(self, summary):
        self.summary = summary


class Tennis(Sport):
    """
    class for tennis alike sport results
    """
    sport = u"Tennis"

    def __init__(self, summary, players, score):
        self.summary = summary
        self.players = players
        self.score = score

    def __str__(self):
        return u"""(%s) %s: %s (%s)""" % (self.sport, self.players, self.score,
            self.summary)


class Football(Sport):
    """
    class for football alike sport results
    """
    sport = u"Fußball"

    def __init__(self, summary, home, score, away):
        self.summary = summary
        self.home = home
        self.score = score
        self.away = away


    def __str__(self):
        return u"""(%s) %s | %s | %s (%s)""" % (self.sport, self.home, self.score,
            self.away, self.summary)


class Motor(Sport):
    """
    class for motor sports alike sport results
    """
    sport = u"Motor"

    def __init__(self, summary, position, team):
        self.summary = summary
        self.position = position
        self.team = team


    def __str__(self):
        return u"""(%s) %s, %s (%s)""" % (self.sport, self.position,
            self.team, self.summary)


def get_ballsports(sport, summary, sportnode):
    """
    this function fetches all result data from the result tree
    for all different kind of ballsports
    """
    result = []
    #print sport, summary
    restb = sportnode.xpath(u"""./tbody/tr/td""")
    #print "restb", restb
    for res in [elem.xpath(u"""./a/span""") for elem in restb]:
        #print [t.text for t in res]
        if sport == u"football":
            result.append(Football(summary=summary, home=res[0].text,
                score=res[1].text, away=res[2].text)
            )
        elif sport == u"tennis":
            result.append(Tennis(summary=summary, players=res[0].text,
                score=res[1].text)
            )
    return result


def get_motorsports(sport, summary, sportnode):
    """
    this function fetches all result data from the result tree
    for all different kind of motorsports
    """
    result = []
    #print sport, summary
    restb = sportnode.xpath(u"""./tbody/tr""")
    #print "restb", restb
    for res in [elem for elem in restb]:
        #print res, res[0], res[1]
        result.append(Motor(summary=summary, position=res[0].text,
            team=res[1][0].text))
    return result


def get_results(tree, board="result"):
    """
    extract the score table from the result tree, select the
    kind of the actual sport event and calls an appropriate function
    to parse the special kind of results
    """
    result = []
    root = tree.getroot()
    # Result Tabellen Knoten
    resnodes = root.xpath(RESTAB[board])
    # check kind of result
    for resnode in resnodes:
        sportnodes = root.xpath("""%s/table[@class="football" or\
            @class="tennis" or @class="motor"]""" % RESTAB[board])
        #print sportnodes
        for sportnode in sportnodes:
            #print sportnode
            sport = sportnode.get(u"class")
            summary = sportnode.get(u"summary")
            result += {
                    u"tennis": get_ballsports,
                    u"football": get_ballsports,
                    u"motor": get_motorsports,
                }.get(sport)(summary=summary, sport=sport, sportnode=sportnode)
    return result


def get_tree(url):
    """
    gets main page from eurosport and returns the parse-tree
    """
    page = urlopen(url).read()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(page), parser)
    return tree


def main():
    tree = get_tree(url=URL)
    for board in BOARDS:
        print "Board: %s" % board
        results = get_results(tree=tree, board=board)
        for row in results:
            print u"%s".encode("utf-8") % row


if __name__ == "__main__":
    main()
