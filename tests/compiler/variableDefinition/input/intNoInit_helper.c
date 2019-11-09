
#include <stdio.h>

extern int i;

int main(void)
{
    i = 42;
    printf("i == %d\n", i);
    return 0;
}