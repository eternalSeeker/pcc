#include<stdio.h>

int foo(int bar)
{
    if(bar == 0)
    {
        bar = 1;
    }
    else
    {
        bar++;
    }
    return bar;
}

int main()
{
    return foo(1);
}