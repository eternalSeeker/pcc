
extern int external_integer;

int foo(void);

int foo(void)
{
    external_integer = 10;
    return 1;
}