#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main (int argc, string argv[])
{
    //declaring variables
    int i = 0;
    string word;
    
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    int key = atoi(argv[1]);
    if (key <= 0)
    {
        printf("Error\n");
        return 1;
    }

    word = get_string ("Plaintext: ");
        
    while (word[i] != '\0')
    {
        
        if (word[i] >= 65 && word[i] <= 122)
        {
            //letra minuscula
            if (word[i] + key > 122)
            {
                word[i] = (word[i] + key) - 26;
            }
            //letra maicuscula 
            else if (word[i] + key > 91 && (word[i] > 64 && word[i] < 91))
            {
                word[i] = (word[i] + key) - 26;
            }
            else
            {
                word[i] = word[i] + key;
            }
            i++;
        }
    }

    printf("ciphertext: %s\n", word);
    
    return 0;
}