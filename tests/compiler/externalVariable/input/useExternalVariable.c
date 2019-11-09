
extern int external_integer;

void foo(void);

void foo(void)
{
    external_integer = 10;
    return;
}