
#include <stdio.h>

int external_integer;
void foo(void);

int main(void)
{
    external_integer = 1;
    foo();
    printf("i == %d\n", external_integer);
    return 0;
}