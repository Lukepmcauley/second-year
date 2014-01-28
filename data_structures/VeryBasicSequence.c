/*
* Implementing from the ADT VeryBasicSequence
* from Inf-2B Data Structures & Alogrithms Lecutre 4
* Luke McAuley
* 27/1/14
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define START_SIZE 10 
#define GROWTH_FACTOR 2

typedef struct VeryBasicSequence{
    int * array;
    int lowest_unused;
    int size;
} VeryBasicSequence;

/*
* Initializes VBS
*/
VeryBasicSequence * create(){
    VeryBasicSequence * temp = malloc(sizeof(VeryBasicSequence));
    temp->array = malloc(sizeof(int) * START_SIZE);
    temp->size = START_SIZE;
    temp->lowest_unused = 0;
    return temp;
}

int elemAtRank(VeryBasicSequence * vbs, int r){
    return vbs->array[r];
}

void replaceAt(VeryBasicSequence * vbs, int r, int e){
    vbs->array[r] = e; 
}

/*
*   Inserts at the next available space,
*   of if full, copies array to a larger one
*   and then tries again.
*
*   The array grows by a factor of the current size of 
*   so that the average time is O(1)
*/
void insertLast(VeryBasicSequence * vbs, int e){
    if(vbs->lowest_unused < vbs->size){
        vbs->array[vbs->lowest_unused] = e;
        vbs->lowest_unused += 1;
    }else{
        int new_size = vbs->size * GROWTH_FACTOR;
        int *new_array = malloc(sizeof(int) * new_size);
        memcpy(new_array, vbs->array, sizeof(int) * vbs->size);
        vbs->size = new_size;
        free(vbs->array);
        vbs->array = new_array;
        insertLast(vbs, e);
    }
}

void main(){
    VeryBasicSequence * v = create();

    int i;
    for (i =0; i<10000; i++){
        insertLast(v, i);
    }
    for(i = 8000; i<10000; i= i+2){
        replaceAt(v, i, 0) ;
    }

    for(i = 9900; i<10000; i++){
        printf("%d\n",elemAtRank(v,i));
    }


}