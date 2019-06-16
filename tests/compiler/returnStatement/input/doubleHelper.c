
#include <stdio.h>

double foo(void);

int main(void)
{
    double d = foo();
    printf("done %f\n", d);
}