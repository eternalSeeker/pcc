
extern int external_integer;

int foo(void);

int foo(void)
{
    int i = 5;
    i = i + external_integer;
    return i;
}