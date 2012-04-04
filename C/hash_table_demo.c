/*
    ~~~~~~~~~~~~~~~~~
    hash_table_demo.c
    ~~~~~~~~~~~~~~~~~
    
    Simple demonstration program how to use the hash table 'object' from the
    famous Glib project. It maps command line options to functions in order
    to simulate a dynamic, controllable program logic.
    
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


/*
* compile with:
*   gcc `pkg-config --cflags --libs glib-2.0` hash_table_demo.c -o hash_table_demo
*/

#include <stdio.h>
#include <glib.h>


/* dummy function */
void bar(void) {
    printf("Bin in 'bar'\n");
}


/* another dummy function */
void foo(void) {
    printf("Bin in 'foo'\n");
}


/* call back function for g_hash_table_foreach()
*  TODO: Check out why this doesn't work:
*        (*value)();
*/
void execute(gpointer key, gpointer value, gpointer user_data) {
    gpointer (*func)();
    func = value;
    func();
}

/* TODO: change command line parsing to Glib-helpers */
int main(int argc, char **argv) {

    // TODO: inform better about the hashing-methods
    GHashTable *mapping = g_hash_table_new(g_str_hash, g_str_equal);
    g_hash_table_insert(mapping, g_strdup("foo"), foo);
    g_hash_table_insert(mapping, g_strdup("bar"), bar);
    
    if(argc != 2) {
        fprintf(stderr, "Aufruf: func [foo|bar|all]\n\n");
        return 1;
    }

    if(strcmp(argv[1], "all") == 0) {
        g_hash_table_foreach(mapping, execute, NULL);
    }
    else {
        gpointer (*func)() = g_hash_table_lookup(mapping, g_strdup(argv[1]));
        if(func != NULL) {
            func();
        }
        else {
            printf("Unzulässiger Parameter!\n");
            return 2;
        }
    }

    return 0;
}
