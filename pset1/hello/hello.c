#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Get name
    string name = get_string("What's your name?\n");
    printf("Hello, %lu\n", strlen(name));
    return 0;
}



