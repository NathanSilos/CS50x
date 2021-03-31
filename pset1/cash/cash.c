#include <cs50.h>
#include <stdio.h>


int main(void)
{
    //Declaring variables
    int coins = 0, change_round;
    double change;
    //Taking change to calculate
    do 
    {   
        //Take the imput
        change = get_double("Change owed:");
    }
    while (change <= 0);

    //dollars to cents
    change_round = round(change * 100);
    
    //starting the loop
    do
    {
        //double change_round = round(change);
        if (change_round >= 25)
        {
            //calcutating value
            for (double i = 25; change_round >= 25; i = 25)
            {
                coins = coins + 1;
                change_round = change_round - 25;
            }
        }
        
        else if (change_round >= 10)
        {
            for (double i = 10; change_round >= 10; i = 10)
            {
                coins = coins + 1;
                change_round = change_round - 10;
            }
        }
        else if (change_round >= 5)
        {
            for (double i = 5; change_round >= 5; i = 5)
            {
                coins = coins + 1;
                change_round = change_round - 5;
            }
        }
        else if (change_round >= 1)
        {
            for (double i = 1; change_round >= 1; i = 1)
            {
                coins = coins + 1;
                change_round = change_round - 1;
            }
        }
    }
    while (change_round != 0);
    
    printf("Coins to change is: %i", coins);


}