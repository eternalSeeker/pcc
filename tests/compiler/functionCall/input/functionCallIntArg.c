
extern int external_integer;

void bar(int i);

void bar(int i)
{
    external_integer = i;
    return;
}

int foo(void);

int foo(void)
{
    int j = 21;
    bar(j);
    return 0;
}