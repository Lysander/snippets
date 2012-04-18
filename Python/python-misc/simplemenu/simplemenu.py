#!/usr/bin/env python

"""
    ~~~~~~~~~~~~~
    simplemenu.py
    ~~~~~~~~~~~~~

    Very simple approach to implement a generic, but easy to use menu system
    with basic Python data types.
    
    Each menu consists of this tuple (or list) structure:
    
        (
            ("text to be shown", <function object>),
            ("another item text", <another function object>),
            (..., ...),
            ...
        )
        
    To be more generic, each 'callable' can be used as second argument.
    
    The user can choose via an computed index, which action should be
    triggered by the core function `handle_menu`.

    This is esspecially written for beginners, so there is no magic like
    `functools.partial` or some clojures to create demo functions.

    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import sys

#
# Some little demo functions that does not have any sensefull functionality.
# We just need something that "does" something
#

def foo():
    print("Bin in 'foo'")

    
def bar(): 
    print("Bin in 'bar'")
    

#
# Core functions of our simple menu system
#
    
def print_menu(menu):
    """
    Function that prints our menu items. It adds an numeric index to each
    item in order to make that the choosebale index for the user.
    
    :param menu: tuple with menu definition
    """
    for index, item in enumerate(menu, 1):
        print("{}  {}".format(index, item[0]))

        
def get_user_input(menu):
    """
    This function implements a simple user input with validation. As the
    input data should match with existing menu items, we check, if the value
    is valid.

    :param menu: tuple with menu definition
    
    :returns: int
    """
    while True:
        try:
            choice = int(input("Ihre Wahl?: ")) - 1
            if choice in range(len(menu)):
                return choice
            else:
                raise IndexError
        except (ValueError, IndexError):
            print("Bitte nur Zahlen aus dem Bereich")


def handle_menu(menu):
    """
    Core function of our menu system. It handles the complete process of
    printing the menu, getting the user input and calling the corresponding
    function.
    
    :param menu: tuple with menu definition
    """
    while True:
        print_menu(menu)
        choice = get_user_input(menu)
        menu[choice][1]()

    
def main():
    # just some demonstration menu structure:
    menu = (
        ("Foo", foo),
        ("Bar", bar),
        # here is some 'magic'. As `sys.exit` takes one parameter and our
        # 'normal' functions do not, we create an anonymous function using
        # the `lambda` keyword. If you do not understand this yet, just take
        # it for granted.
        ("Exit", lambda: sys.exit(0))
    )
    
    # run the menu-"handler" :-)
    handle_menu(menu)


if __name__ == "__main__":
    main()
