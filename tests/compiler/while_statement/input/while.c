
int foo(void);

int foo(void)
{
    int retVal = 10;
    int i = 10;
    while(i)
    {
        i = i - 1;
        retVal = retVal + i;
    }
    return retVal;

}