#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // Ensure user ran program with two words at prompt
    if (argc != 2)
    {
        return 1;
    }
    
    // Open file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        return 1;
    }
    
    // read 3 bytes from file
    unsigned char bytes[512];
    FILE *img = NULL;
    
    // brennoli é o cara
    char name[8];
    bool check = false;
    
    int countImage = 0;
    while (fread(bytes, 512, 1, file) == 1)
    {
        // Check if bytes are 0xff 0xd8 0xff(JPEG)
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            // check if the image was found already 
            if (check == true)
            {
                fclose(img);
            }
            // elaborate the image
            else
            {
                check = true;
            }
            
            // elabora the image part2
            sprintf(name, "%03i.jpg", countImage);
            img = fopen(name, "w");
            countImage++;
        }
        if (check == true)
        {
            fwrite(bytes, 512, 1, img);
        }
    }
    
    // close everything
    fclose(img);
    fclose(file);
    
    // finished cacete
    return 0;
}
