
#include <stdio.h>

int external_integer;

int main(void)
{
    external_integer = 1;
    printf("i == %d\n", external_integer);
}