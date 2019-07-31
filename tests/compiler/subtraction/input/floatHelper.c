
#include <stdio.h>

float foo(void);

int main(void)
{
    float f = foo();
    printf("done %f\n", f);
}