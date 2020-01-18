
int putchar(int c);

void main(void);

int fac(int i);

int fac(int i)
{
    int j;
    if(i > 1)
    {
    int c = i-1;
   j = fac(c);
   j = j * i;
   return j;
    }
    return 1;
}

void main(void)
{
    int c;
    int i;
    c = 4;
    i = fac(c);
    c = i - 24;
    if(c)
    {
    c = 'N';
    putchar(c);
    }


    c = 'H';
    putchar(c);
    c = 'e';
    putchar(c);
    c = 'l';
    putchar(c);
    c = 'l';
    putchar(c);
    c = 'o';
    putchar(c);
    c = 32;
    putchar(c);
    c = 'W';
    putchar(c);
    c = 'o';
    putchar(c);
    c = 'r';
    putchar(c);
    c = 'l';
    putchar(c);
    c = 'd';
    putchar(c);
    c = '\n';
    putchar(c);
    return;
}