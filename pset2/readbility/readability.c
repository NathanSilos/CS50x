#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

//start coding
int main(void)
{
    //declaring strings
    string text;
    int letters = 0, word = 1, sentence = 0, i = 0;

    //Get text
    text = get_string("Text: ");


    //counting letters, word and setences
    while (text[i] != '\0')
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentence++;
        }
        if (text[i] <= 122 && text[i] >= 65)
        {
            letters++;
        }
        if (text[i] == ' ')
        {
            word++;
        }

        i++;

    }

    //calculating the values
    float L = (float)letters / word * 100;
    float S = (float)sentence / word * 100;
    
    //Calculating grade
    int grade = round(0.0588 * L - 0.296 * S - 15.8);

    //Showing grade
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade <= 16)
    {
        printf("Grade %i\n", grade);
    }
    else
    {
        printf("Grade 16+\n");
    }

}