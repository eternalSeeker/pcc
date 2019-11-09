
#include <stdio.h>

extern double d;

int main(void)
{
    d = 42.0;
    printf("d == %f\n", d);
    return 0;
}