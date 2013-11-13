#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <set>
#include <algorithm>
#define MaxA 400
#define MaxB 200
#define MaxC 1200

using namespace std;

string x[1][6];
string A[MaxA][6];
string B[MaxB][6];
string C[MaxC][6];
int numA;
int numB;
int numC;
int W;
int mypow[20]={1,2,4,8,16,32,64,128,256,512,1024};

int splitString(string S, char ch, string splits[])
{
    int i=0;
    int pos;
    while((pos=S.find(ch))<S.length())
    {
        splits[i]=S.substr(0,pos);
        S=S.substr(pos+1);
        i++;
    }
    splits[i]=S;
    i++;
    return i;
}
void splitSet(string S, char ch, set<string> &tagset)
{
    int pos;
    while((pos=S.find(ch))<S.length())
    {
        tagset.insert(S.substr(0,pos));
        S=S.substr(pos+1);
    }
    tagset.insert(S);
}
int getDataFromFile(char fileName[], string store[][6])
{
    ifstream fin;
    fin.open(fileName);
    string l;
    string temp[10];
    int i=0;
    while(getline(fin,l))
    {
        splitString(l,'\t',temp);
        store[i][0]=temp[0];//uid
        store[i][1]=temp[3];//gender
        store[i][2]=temp[4];//province
        store[i][3]=temp[5];//city
        store[i][4]=temp[6];//location
        store[i][5]=temp[7];//tags
        i++;
    }
    return i;
}
float cal_tag_value(string a, string b)
{
    set<string> atags;
    set<string> btags;
    set<string> ctags;
    splitSet(a,' ',atags);
    splitSet(b,' ',btags);
    set_intersection(atags.begin(),atags.end(),btags.begin(),btags.end(),inserter(ctags,ctags.begin()));
    int anum=atags.size()-1;
    int bnum=btags.size()-1;
    int cnum=ctags.size()-1;
    cout<<anum<<endl;
    cout<<bnum<<endl;
    cout<<cnum<<endl;
    return 1.0*cnum/(anum+bnum-cnum);
}
float cal_W()
{
    float sum=0;
    for(int i=0; i<numA; i++)
    {
        sum+=cal_tag_value(x[0][5], A[i][5]);
    }
    return sum/numA;
}
int main(int argc, char** argv)
{
    getDataFromFile(argv[1], x);
    numA=getDataFromFile(argv[2], A);
    numB=getDataFromFile(argv[3], B);
    numC=getDataFromFile(argv[4], C);
    float W=cal_W();
    ofstream fout;
    fout.open("W.txt",ios::app);
    fout<<W<<endl;
    return 0;
}
