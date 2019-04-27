
#include <stdio.h>

extern float f;

int main(void)
{
    f = 42.0;
    printf("f == %f\n", f);
}