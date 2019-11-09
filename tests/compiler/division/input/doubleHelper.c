
#include <stdio.h>

double foo(void);

int main(void)
{
    double d = foo();
    printf("done %4.3f\n", d);
    return 0;
}