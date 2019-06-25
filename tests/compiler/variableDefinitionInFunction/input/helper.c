
#include <stdio.h>

void foo(void);

int main(void)
{
    char c = 6;
    foo();
    char d = 7;
    printf("done %d, %d\n", c, d);
}