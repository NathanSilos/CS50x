#include <stdio.h>
#include <cs50.h>

int main(void)

{ 
    char a[100]; int length;
    printf("Enter a string to calculate its length\n"); gets(a);
    length = strlen(a);
    printf("Length of the string = %d\n", length);
    return 0; 
    
}