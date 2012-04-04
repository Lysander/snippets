/*
    ~~~~~~~~~~~~~~
    func_mapping.c
    ~~~~~~~~~~~~~~
    
    Simple demonstration program how to use function pointers in C.
    
    Copyright (C) 2011  Christian Hausknecht

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

*/

#include <stdio.h>
#include <string.h>


#define CALLS 3
/*
* struct for mapping a parameter string to a function
*/
struct funcmap {
    char name[10];
    void (*func)(void);
};

// dummy function
void bar(void) {
    printf("Bin in 'bar'\n");
}

// dummy function
void foo(void) {
    printf("Bin in 'foo'\n");
}


/*
* demonstrate how to iterate over a vector of functions
*/
void func_iterate() {
    printf("Funktions-Dispatcher:\n");
    // Array of functions
    void (*funcs[2])(void) = {foo, bar};
    for(int i=0; i<2; i++) {
        // call them iteratively
        funcs[i]();
    }
}


int main(int argc, char **argv) {

    // define our mapping
    struct funcmap dispatch[CALLS] = {
        {"foo", foo},
        {"bar", bar},
        {"index", bar}
    };
    
    if(argc != 2) {
        fprintf(stderr, "Aufruf: func [foo|bar|index|all]\n\n");
        return 1;
    }
    if(strcmp(argv[1], "all") == 0) {
        func_iterate();
    }
    else {
        for(int i=0; i<CALLS; i++) {
            if(strcmp(dispatch[i].name, argv[1]) == 0) {
                dispatch[i].func();
                return 0;
            }
        }
        fprintf(stderr, "Unbekannte Funktion '%s'\n\n", argv[1]);
        return 2;
    }
    return 0;
}
