
#include <stdio.h>

char foo(void);

int main(void)
{
    char c = foo();
    printf("done %d\n", c);
    return 0;
}