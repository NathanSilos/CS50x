// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdbool.h>
#include <ctype.h>

#include "dictionary.h"



// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1830;

// Total number of words
unsigned int nWords = 0;
// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int index = hash(word);
    
    // declaring the cursor
    node *cursor = table[index];
    
    // starting the loop to look at a word in hash table
    while (cursor != NULL)
    {
        // dont find de word
        if (strcasecmp(cursor->word, word))
        {
            cursor = cursor->next;
        }
        // word found
        else
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int size = strlen(word);
    unsigned int index = 0;
    
    for (int i = 0; i < size; i++)
    {
        if ((word[i] >= 65 && word[i] <= 90) || (word[i] >= 97 && word[i] <= 122) || word[i] == 39)
        {
            index += tolower(word[i]);
        }
    }
    return (index % N);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Empty file.");
        return false;
    }

    // Read strings from Dictionary
    char wordFile[LENGTH + 1];
    while (fscanf(dict, "%s", wordFile) != EOF)
    {
        // Create a New Node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, wordFile);
        n->next = NULL;d

        // Hash Word
        int index = hash(wordFile);
        if (table[index] == NULL)
        {
            // Insert Node into Hash Table
            table[index] = n;
        }
        else
        {
            // Already exist a value in some location
            n->next = table[index];
            table[index] = n;
        }
        //counting how many words
        nWords++;
    }

    //close File
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // return the number of words in dictionary
    return nWords;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *comander = table[i];
        node *cursor = comander;
        node *tmp = cursor;
        
        while(tmp != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    
    return true;
}
