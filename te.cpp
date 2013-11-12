#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <fstream>

#define MAX 100
#define smax 20
using namespace std;

int main(int argc, char **argv)
{
	int a1=0;
	int a2=0;
	int a3=0;
	int Sum[400];
	int Num[400];
	int n=0;

    string iPath="Sum.txt";
	ifstream r;
	r.open("Sum.txt");
	while(a1!=3)
		r >> a1 >> a2 >> a3;

	while(a1==3)
	{
		Num[n]=a2;
		Sum[n]=a3;
		n++;
		r >> a1 >> a2 >> a3;
	}

	r.close();

	ofstream w;
    string oPath="Result.txt";
	w.open("Result.txt");
	for(int i=0;i<n;i++)
		w << Num[i] << ":" << Sum[i] << endl;
	w.close();

	return 0;
}
