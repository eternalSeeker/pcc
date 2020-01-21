
#include <stdio.h>

int foo(int i);

int main(void)
{
    int i = 4;
    int res = foo(i);
    printf("done %d\n", res);
    return 0;
}