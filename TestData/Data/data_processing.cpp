#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <set>
#include <algorithm>
#include <vector>
#define MaxA 400
#define MaxB 200
#define MaxC 1200
#define I 1
#define J 3
#define K 1
using namespace std;
//////////////////////////////////////////
class UidToSimilarityCouple
{
    public:
        string uid;
        int similarity;
        char userType;//B or C
        UidToSimilarityCouple(string iniUid, int iniSimilarity, char utype):
            uid(iniUid), similarity(iniSimilarity), userType(utype){}
        bool operator < (const UidToSimilarityCouple &couple)const
        {
            return similarity<couple.similarity;
        }
};

//////////////////////////////////////////
string x[1][6];
string A[MaxA][6];
string B[MaxB][6];
string C[MaxC][6];
int numA;
int numB;
int numC;
int W;
int mypow[20]={1,2,4,8,16,32,64,128,256,512,1024};
vector<UidToSimilarityCouple> allSimilarity;

//////////////////////////////////////////
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

//////////////////////////////////////////
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

//////////////////////////////////////////
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

//////////////////////////////////////////
float cal_tag_value(string a, string b)
{
    set<string> atags;
    set<string> btags;
    set<string> abtags;
    splitSet(a,' ',atags);
    splitSet(b,' ',btags);
    set_intersection(atags.begin(),atags.end(),btags.begin(),btags.end(),inserter(abtags,abtags.begin()));
    int anum=atags.size()-1;
    int bnum=btags.size()-1;
    int abnum=abtags.size()-1;
    //cout<<anum<<endl;
    //cout<<bnum<<endl;
    //cout<<cnum<<endl;
    //
    if(anum+bnum-abnum==0)
    {
        return 0;
        cout<<"Shit!!!"<<endl;
        cout<<anum<<' '<<bnum<<' '<<abnum<<endl;
        cout<<a<<endl;
    }
    return 1.0*abnum/(anum+bnum-abnum);
}

//////////////////////////////////////////
float cal_W()
{
    float sum=0;
    if(x[0][5]=="")
        cout<<x[0][0]<<endl;
    for(int i=0; i<numA; i++)
    {
        sum+=cal_tag_value(x[0][5], A[i][5]);
    }
    return sum/numA;
}

//////////////////////////////////////////
int cal_similarity(string a[], string b[])
{
    int ans=0;
    for(int i=1;i<I+1;i++)
    {
        if(a[i]==b[i])
            ans+=mypow[i];
    }
    for(int i=I+1;i<I+J+1;i++)
    {
        if(i==I+J)
        {
            ans+=mypow[i];
        }
        if(a[i]!=b[i])
            break;
    }
    for(int i=I+J+1;i<I+J+K+1;i++)
    {
        float w=cal_tag_value(a[i],b[i]);
        if(w>=W)
            ans+=mypow[i];
    }
    return ans;
}

//////////////////////////////////////////
void cal_all_similarity()
{
    for(int i=0;i<numB;i++)
    {
        int similarity=cal_similarity(x[0],B[i]);
        UidToSimilarityCouple couple(B[i][0], similarity, 'B');
        allSimilarity.push_back(couple);
    }
    for(int i=0;i<numC;i++)
    {
        int similarity=cal_similarity(x[0],C[i]);
        UidToSimilarityCouple couple(C[i][0], similarity, 'C');
        allSimilarity.push_back(couple);
    }
    sort(allSimilarity.begin(), allSimilarity.end());
    int allsize=allSimilarity.size();
    int ansOfB=0;
    int ansOfC=0;
    for(int i=allSimilarity.size()-1;i>allsize-10;i--)
    {
        if(allSimilarity[i].userType=='B')
            ansOfB++;
        if(allSimilarity[i].userType=='C')
            ansOfC++;
    }
    cout<<1.0*ansOfB/(ansOfB+ansOfC)<<endl;
}

//////////////////////////////////////////
int main(int argc, char** argv)
{
    getDataFromFile(argv[1], x);
    numA=getDataFromFile(argv[2], A);
    numB=getDataFromFile(argv[3], B);
    numC=getDataFromFile(argv[4], C);
    float W=cal_W();
    cal_all_similarity();
    ofstream fout;
    fout.open("accuracy.txt",ios::app);
    fout.close();
    return 0;
}
