
int foo(int i);

int foo(int i)
{
   int j = 0;
   if(i > 1)
   {
    int c = i-1;
    j = foo(c);
    j = j * i;
    return j;
   }
   return 1;
}
