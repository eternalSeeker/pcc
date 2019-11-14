
extern int external_integer;

void bar(void);

void bar(void)
{
    external_integer = 20;
    return;
}

int foo(void);

int foo(void)
{
    bar();
    return 0;
}