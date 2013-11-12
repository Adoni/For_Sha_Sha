#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include "mysql.h"
#define MaxN 1000
#define MaxM 10
#define MaxTags 100

using namespace std;
long int N;
int M, I=3, J=3, K=2;
string data[MaxN][MaxM];
string usertags[MaxN][MaxTags];//usertags[i][j] means the tag_j of user_i
int tagLen[MaxTags];//means the number of tags of user_i.

//use splitAllTags to cut the tags in database(which is a string)to an array of tag
void splitAllTags(string usertags[][MaxTags])
{
    for(int i=0;i<N;i++)
    {
        int j=0;
        string tags=data[i][7];
        int pos;
        while((pos=tags.find("\t "))<tags.length())
        {
            usertags[i][j]=tags.substr(0,pos);
            tags=tags.substr(pos+1);
            j++;
        }
        tagLen[i]=j;
    }
}
int main(int argc, char** argv)
{
    char root[]="root";
    char passwd[]="9261adoni";
    char host[]="localhost";
    char database[]="shasha";
    unsigned int port=3306;
    MYSQL myCont;
    MYSQL_RES *result;
    MYSQL_ROW sql_row;
    MYSQL_FIELD *fd;
    int res;

    mysql_init(&myCont);
    if(!mysql_real_connect(&myCont, host, root, passwd, database, port, NULL, 0))
    {
        cout<<"Connect Failed!"<<endl;
        return 0;
    }
    mysql_query(&myCont, "SET NAMES UTF8"); //设置编码格式,否则在cmd下无法显示中文
    res=mysql_query(&myCont,"select * from users");//查询
    if(!res)
    {
        result=mysql_store_result(&myCont);//保存查询到的数据到result
        if(result)
        {
            int i,j;
            cout<<"number of result: "<<(unsigned long)mysql_num_rows(result)<<endl;
            for(i=0;fd=mysql_fetch_field(result);i++)//获取列名
            {
                cout<<fd->name<<"\t";
            }
            cout<<endl;
            M=mysql_num_fields(result);
            cout<<M<<endl;
            i=0;
            while(sql_row=mysql_fetch_row(result))//获取具体的数据
            {
                for(j=0;j<M;j++)
                {
                    data[i][j]=sql_row[j];
                }
                i++;
            }
            N=i;
        }
    }
    else
    {
        cout<<"query sql failed!"<<endl;
    }
    splitAllTags(usertags);
    int p = 0;
    long int L2;
    ofstream write;
    write.open("Sum.txt");
    long int i, j;
    long long int Sum = 0;
    for (long int b = 0; b < N; b++)
    {
        for (long int c = 0; c < N; c++)
        {
            for (int k = 1; k < I + 1; k++)//孤立信息
                if (data[b][k] == data[c][k])
                    Sum += (int) pow(2, k);
            for (int k = I + 1; k < I + J + 1; k++)//偏序信息
            {
                if (data[b][k] == data[c][k])
                    Sum += (int) pow(2, k);
                else
                    break;
            }
            double S = 0;
            for (int k = 0; k < tagLen[b]; k++)//相似信息
                for (int l = 0; l < tagLen[c]; l++)
                    if (usertags[b][k] == usertags[c][l])
                        S++;
            double V = (S / K) / K;
            if (V > 0.1)
                //cout<<"Here"<<endl;
                Sum += (int) pow(2, (I + J + 1));

            if (Sum != 0 && b != c)
                write << b << " " << c << " " << Sum << endl;
            Sum = 0;
        }
    }
    write.close();

    return 0;
}

