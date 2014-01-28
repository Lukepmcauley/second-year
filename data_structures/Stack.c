/*
* Implementing a stack in C
* Luke McAuley
* 24/1/14
*/

#include <stdlib.h>
#include <stdio.h>

struct Node{
	struct Node * next;
	int value;
};

struct Stack{
	struct Node * head;
} Stack;


int Pop(struct Stack * stack){
	struct Node * popped = stack->head;
	stack->head = popped->next;
    int value = popped->value;
    free(popped);
    return value;
}

void Push(struct Stack *stack, int x){
    struct Node * new_node = malloc(sizeof(struct Node));
    new_node->value = x;
    new_node->next = stack->head;
    stack->head = new_node;
}

int isEmpty(struct Stack *stack){
    return stack->head == NULL;
}


int main(){
    struct Stack stack = {0};
    int i; 
    for(i = 0; i<100; i++){
        Push(&stack, i);
    }
    while(!isEmpty(&stack)){
        printf("%d\n",Pop(&stack));
    }
}