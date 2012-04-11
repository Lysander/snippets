#!/usr/bin/env python2
# coding: utf-8

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
    ~~~~~~~~~~~
    sparqllexer
    ~~~~~~~~~~~
    
    A small module I wrote for my diploma thesis in 2009 / 2010, which dealt
    about semantic technologies like OWL, SPARQL and related technologies.
    
    This module contains lexer definitions for various semantic formats for 
    the famous 'sphinx' syntax highlighting tool, which are:
    
        - SPARQL
        - Turtle
        - Manchester Syntax
    
    And at least - not directly related to semantic languages - a lexer for:
    
        - LDraw
    
    a CAD Tool for designing digital LEGO(R) models.
    
    Please note that there are by far not complete or perfect. I just 
    implemented everything I needed. Feel free to accomplish this task or
    use this as a basic for writing a more sophisticated lexer :-)
    
    .. moduleauthor::  Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import re

# pygments specific imports
from pygments.lexer import RegexLexer, bygroups, using
from pygments.token import Text, Comment, Keyword, Punctuation, Name, \
                            Operator, String, Number
from pygments.lexers.templates import DjangoLexer


__all__ = ["SPARQLLexer", "TurtleLexer", "ManchesterLexer", "LDrawLexer"]


class SPARQLLexer(RegexLexer):
    """
    Lexer for the SPARQL Query Language for RDF
    """

    name = 'SparQL'
    aliases = ['sparql']
    filenames = ['*.sparql']

    flags = re.IGNORECASE
    tokens = {
        'root': [
            #(r'\{\{.*\}\}', Punctuation, 'tpl'),
            (r'#.*?\n', Comment.Single),
            (r'\b(BASE|SELECT|ORDER|BY|FROM|GRAPH|STR|isURI|sameTERM|'
             r'PREFIX|CONSTRUCT|LIMIT|FROM|NAMED|OPTIONAL|LANG|isIRI|'
             r'DESCRIBE|OFFSET|WHERE|UNION|LANGMATCHES|isLITERAL|'
             r'ASK|DISTINCT|FILTER|DATATYPE|REGEX|REDUCED|a|BOUND)\b',
             Keyword),
            (r'\?[A-Za-z0-9_]+', Name.Variable),
            # this is not SparQL like, but usefull for jinja2 like vars
            (r'(\{\{[A-Za-z0-9_]+\}\})([.;]*)', bygroups(Name.Variable, 
             Punctuation)),
            (r'(\w+)(:)(\S+)', 
             bygroups(Name.Namespace, Operator, Text)),
            (r'[A-Za-z]+:', Name.Namespace),
            (r'<http[\w+\d+:/#\.\-_\{\}]+>', String.Other),
            (r'(true|false)', Name.Constant),
            (r'[0-9]+', Number.Integer),
            (r'[0-9]*\.[0-9]+(e[+-][0-9]+)', Number.Float),
            (r"'(''|[^'])*'", String.Single),
            (r'"(""|[^"])*"', String.Double),
            (r'[\{\}\(\)\.;,]', Punctuation),
            (r'[<=>&\^]', Operator),
            (r'[\w\d_]+', Name.Function),
            (r'\s+', Text)
        ],
        'tpl': [
            ('\{\{', Punctuation),
            ('\}\}', Punctuation, '#pop')
        ]
    }


class TurtleLexer(RegexLexer):
    """
    Lexer for the Turtle notation for RDF
    """

    name = 'Turtle'
    aliases = ['turtle']
    filenames = ['*.turtle']

    flags = re.IGNORECASE
    tokens = {
        'root': [
            (r'#.*?\n', Comment.Single),
            (r'(@)(prefix)', bygroups(Operator.Word, Keyword)),
            (r'\w+://\S+', String.Other),
            (r'type|range|domain|subPropertyOf', Name.Builtin),
            (r'(\w+)(:)(\w+)', 
                bygroups(Name.Namespace, Punctuation, Text)),
            (r'(\w+)(:)', bygroups(Name.Namespace, Punctuation)),
            (r'[0-9]+', Number.Integer),
            (r'[0-9]*\.[0-9]+(e[+-][0-9]+)', Number.Float),
            (r"'(''|[^'])*'", String.Single),
            (r'"(""|[^"])*"', String.Double),
            (r'[\{\}\(\)\.;,^^]', Punctuation),
            (r'\w+', Name.Function),
            (r'\s+', Text)
        ]
    }


class ManchesterLexer(RegexLexer):
    """
    Lexer for the Manchester notation for OWL
    """

    name = 'Manchester'
    aliases = ['manchester']
    filenames = ['*.manchester']

    flags = re.IGNORECASE
    tokens = {
        'root': [
            (r'#.*?\n', Comment.Single),
            (r'(@)(prefix)', bygroups(Operator, Keyword)),
            (r'(\w+)(:)(\w*)',
                bygroups(Name.Namespace, Punctuation, Text)),
            (r'<http[\w+\d+:/#\.\-_]+>', String.Other),
            (r'class|prefix|SubClassOf|EquivalentOf|Individual|Types|Facts'
                '|DisjointWith|int|true|false',
                Keyword),
            (r'some|and|or|value', Operator.Word),
            (r'[0-9]+', Number.Integer),
            (r'[0-9]*\.[0-9]+(e[+-][0-9]+)', Number.Float),
            (r"'(''|[^'])*'", String.Single),
            (r'"(""|[^"])*"', String.Double),
            (r'[\{\}\(\)\.;:,\^\^]', Punctuation),
            (r'\w+', Text),
            (r'\s+', Text)
        ]
    }


class LDrawLexer(RegexLexer):
    """
    Lexer for LDraw files
    """

    name = 'LDraw'
    aliases = ['ldraw']
    filenames = ['*.ldr']

    flags = re.IGNORECASE
    tokens = {
        'root': [
            (r'0', Number),
            (r'.*', String)
        ],
        'zero': [
            ('Author|Name', Keyword),
            (':', Punctuation),
            ('$', Text, '#pop')
        ]
    }
