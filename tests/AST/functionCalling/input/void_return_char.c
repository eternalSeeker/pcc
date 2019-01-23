
char test(void);

void test2(void);

char test(void)
{
    char foo = 21;
    return foo;
}

void test2(void)
{
    test();
}
