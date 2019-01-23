
int test(void);

void test2(void);

int test(void)
{
    int foo = 5;
    return foo;
}

void test2(void)
{
    test();
}
