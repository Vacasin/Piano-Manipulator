#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
using namespace std;
struct lHand
{
    vector<float> time;
    vector<string> cmd;
};
struct rHand
{
    vector<float> time;
    vector<string> cmd;
};
static int side=0;
static float gapTime=0.0;
int main()
{
    ifstream file("input.txt"); // ���ı��ļ�
    if (!file.is_open())
    {
        cerr << "�޷����ļ�" << endl;
        return 1;
    }

    vector<string> s;
    string line;

    while (getline(file, line))
    {
        s.push_back(line);
    }

    file.close(); // �ر��ļ�
//    for(auto it=s.begin();it!=s.end();it++)
//    {
//        cout<<(*it)<<endl;
//    }

    lHand lhand;
    rHand rhand;

    for(auto it=s.begin(); it!=s.end(); it++)
    {
        //cout<<"*it[0]="<<(*it)[0]<<" "<<"*it[1]="<<(*it)[1]<<endl;
        string cmd1;
        string cmd2;
        string cmd3;
        string cmd4;
        string cmd5;//The command is like I001-500-1-1-2000,which consisted of 5 parts.
        string cmd6;
        string tCmd;//Total cmd;
        string bCmd;//Back cmd;


        cmd1="I001";
        cmd2="100";
        cmd3="1";
        cmd5="900";
        cmd6="1500";//back command
        if((*it)[0]=='S'&&(*it)[1]=='i')
        {
            int len=(*it).size();
            //cout<<len<<endl;
            char ch=(*it)[len-2];
            if(ch=='-')
            {
                side=-1;
            }
            else
            {
                side=1;
            }
        }

            if((*it)[0]=='M'&&(*it)[1]=='o')
            {
                // �ҵ����һ���ո��λ��
                size_t lastSpacePos = (*it).rfind(' ');

                if (lastSpacePos != string::npos && lastSpacePos + 1 < (*it).length())
                {
                    // ��ȡ�������ֲ���
                    string numberStr = (*it).substr(lastSpacePos + 1);

                    // ���ַ���ת��Ϊfloat
                    istringstream iss(numberStr);
                    float duration;
                    if (iss >> duration)
                    {
                        // ��ӡ���
                        //cout << "��ȡ������Ϊ: " << duration << endl;
                        gapTime=duration;
                        //cout<<gapTime<<endl;
                    }
                    else
                    {
                        cerr << "�޷�ת��Ϊ����" << endl;
                    }
                }
                else
                {
                    cerr << "δ�ҵ�����" << endl;
                }
                if(side==1)
            {
                rhand.time.push_back(gapTime);
            }
            else if(side==-1)
            {
                lhand.time.push_back(gapTime);
            }
            }
                        if((*it)[0]=='P'&&(*it)[1]=='r')
            {
                // �ҵ����һ���ո��λ��
                size_t lastSpacePos = (*it).rfind(' ');

                if (lastSpacePos != string::npos && lastSpacePos + 1 < (*it).length())
                {
                    // ��ȡ�������ֲ���
                    string numberStr = (*it).substr(lastSpacePos + 1);

                    // ���ַ���ת��Ϊfloat
                    istringstream iss(numberStr);
                    float duration;
                    if (iss >> duration)
                    {
                        // ��ӡ���
                        //cout << "��ȡ������Ϊ: " << duration << endl;
                        gapTime=duration;
                        //cout<<gapTime<<endl;
                    }
                    else
                    {
                        cerr << "�޷�ת��Ϊ����" << endl;
                    }
                }
                else
                {
                    cerr << "δ�ҵ�����" << endl;
                }
                        if(side==1)
            {
                rhand.time.push_back(gapTime);
            }
            else if(side==-1)
            {
                lhand.time.push_back(gapTime);
            }
            }
        if((*it)[0]=='C'&&(*it)[1]=='u')
        {
            int len=(*it).size();
            int num1=(*it)[len-1];
            switch(num1)
            {
            case '1':
                cmd4="2";
                break;
            case '2':
                cmd4="3";
                break;
            case '3':
                cmd4="4";
                break;
            case '4':
                cmd4="5";
                break;
            }

            tCmd=cmd1+"-"+cmd2+"-"+cmd3+"-"+cmd4+"-"+cmd5;
            bCmd=cmd1+"-"+cmd2+"-"+cmd3+"-"+cmd4+"-"+cmd6;
            //cout<<tCmd<<endl;
            //cout<<gapTime<<endl;

            //cout<<side<<endl;
            if(side==1)
            {
                rhand.cmd.push_back(tCmd);
                rhand.cmd.push_back(bCmd);
            }
            else if(side==-1)
            {
                lhand.cmd.push_back(tCmd);
                lhand.cmd.push_back(bCmd);
            }
        }
    }
//    cout<<"right hand:"<<endl;
//    for(auto it=rhand.cmd.begin(); it!=rhand.cmd.end(); it++)
//    {
//        cout<<(*it)<<endl;
//    }
//    cout<<"left hand:"<<endl;
//    for(auto it=lhand.cmd.begin(); it!=lhand.cmd.end(); it++)
//    {
//        cout<<(*it)<<endl;
//    }
//      for(auto it=lhand.time.begin();it!=lhand.time.end();it++)
//      {
//          cout<<(*it)<<endl;
//      }



    ofstream ofs;
    ofs.open("rightCmd.txt", ios::out);
    if (ofs.is_open())
    {
        for(auto it=rhand.cmd.begin(); it!=rhand.cmd.end(); it++)
        {
            //cout<<(*it)<<endl;
            ofs<<(*it)<<endl;
        }
    }
    ofs.close(); // �ر��ļ�

    ofs.open("leftCmd.txt", ios::out);
    if (ofs.is_open())
    {
        for(auto it=lhand.cmd.begin(); it!=lhand.cmd.end(); it++)
        {
            //cout<<(*it)<<endl;
            ofs<<(*it)<<endl;
        }
    }
    ofs.close(); // �ر��ļ�
      ofs.open("rightTime.txt", ios::out);
    if (ofs.is_open())
    {
        for(auto it=rhand.time.begin(); it!=rhand.time.end(); it++)
        {
            //cout<<(*it)<<endl;
            ofs<<(*it)<<endl;
        }
    }
    ofs.close(); // �ر��ļ�
      ofs.open("leftTime.txt", ios::out);
    if (ofs.is_open())
    {
        for(auto it=lhand.time.begin(); it!=lhand.time.end(); it++)
        {
            //cout<<(*it)<<endl;
            ofs<<(*it)<<endl;
        }
    }
    ofs.close(); // �ر��ļ�
    return 0;
}
