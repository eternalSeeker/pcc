
int foo(void);

int foo2(void);

int foo2(void)
{
    return 1;
}

int foo(void)
{
    int i = 0;
    if(foo2())
    {
        i = 5;
    }
    return i;
}