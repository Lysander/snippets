/*
    ~~~~~~~
    coins.c
    ~~~~~~~
    
    Simple program that calculates the optimal portfolio of coins from a
    given amount of money.
    
    Copyright (C) 2010  Christian Hausknecht

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
#include <stdlib.h>

#define COIN_COUNT 7

// possible amounts of Euo(€) coins
int coins[COIN_COUNT] = {200, 100, 50, 10, 5, 2, 1};


int *calc_change(int amount) {
    int *result = (int*)malloc(sizeof(int) * COIN_COUNT);
    int index;
    for(index = 0; index < COIN_COUNT; index++) {
        result[index] = 0;
        while(amount >= coins[index]) {
            amount -= coins[index];
            result[index]++;
        }
    }
    return result;
}


int main(int argc, char *argv[]) {
    if(argc != 2) {
        printf("Usage: coins AMOUNT\n");
        return 1;
    }
    
    int amount = atoi(argv[1]);
    printf("Ihr Geldbetrag %d -> ", amount);
    
    int *result = calc_change(amount);
    int index;
    for(index=0; index < COIN_COUNT; index++) {
        printf("%d x %d  ", coins[index], result[index]);
    }
    puts("");

    return EXIT_SUCCESS;
}
