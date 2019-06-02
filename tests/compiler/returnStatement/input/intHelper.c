
#include <stdio.h>

int foo(void);

int main(void)
{
    int i = foo();
    printf("done %d\n", i);
}