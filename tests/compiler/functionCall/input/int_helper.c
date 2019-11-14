
#include <stdio.h>

int external_integer;
int foo(void);

int main(void)
{
    external_integer = 1;
    int res = foo();
    printf("i == %d\nres == %d", external_integer, res);
    return 0;
}