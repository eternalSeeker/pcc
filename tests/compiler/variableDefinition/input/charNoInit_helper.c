
#include <stdio.h>

extern char c;

int main(void)
{
    c = 42;
    printf("c == %d\n", c);
    return 0;
}