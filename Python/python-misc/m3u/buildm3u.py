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
    ~~~~~~~~
    buildm3u
    ~~~~~~~~
    
    Small script that generates a '*.m3u'-file by scanning recursivly
    from a given directory from different music files recognized by their
    suffixes.
    
    .. moduleauthor::  Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import os
import fnmatch
import argparse
from random import shuffle

MUSIC_FORMATS = ("mp3", "ogg", "wav", "flac")


def generate_playlist(dirname, extensions=MUSIC_FORMATS):
    patterns = list(extensions) + [ext.upper() for ext in extensions]
    playlist = []
    for root, dirs, files in os.walk(dirname):
        for pattern in patterns:
            playlist.extend(fnmatch.filter(files, "*.{}".format(pattern)))
    return playlist


def main():
    parser = argparse.ArgumentParser(description="Generates m3u-playlists by\
                                     scanning a given directory recursivly.")
    parser.add_argument("basedir", help="directory to be scanned")
    parser.add_argument("outfile", help="m3u File")
    parser.add_argument("-a", "--append", action="store_true", 
                        help="append to an existing m3u File")
    parser.add_argument("-s", "--shuffle", action="store_true", 
                        help="shuffle the playlist")
    args = parser.parse_args()

    playlist = generate_playlist(args.basedir)
    
    if args.shuffle:
        shuffle(playlist)
    
    mode = "a" if args.append else "w"
    with open(args.outfile, mode) as handler:
        for entry in playlist:
            handler.write("{}\n".format(entry))


if __name__ == "__main__":
    main()
