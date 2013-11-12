#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main()
{
    char a[20]="1234";
    char b[20]="Shasha";
    sprintf(a,"Hello %s!\n",b);
    printf("%s",a);
}
