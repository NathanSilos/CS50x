#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Declaring variables
    int height = 0;
    char space = ' ', hash = '#';
    
    while (height <= 0 || height >= 9)
    {
        //Take the height
        height = get_int("Height: ");
    }
    //Conditional to the height number


    //Loop that makes the pyramid
    
    for (int n = 1; n <= height; n++)
    {
        for (int i = 1; i <= height - n ; i++)
        {
            printf("%c", space);
        }
    
        for (int j = 1; j <= n; j++)
        {
            printf("%c", hash);
        }
        printf("\n");
    }
}