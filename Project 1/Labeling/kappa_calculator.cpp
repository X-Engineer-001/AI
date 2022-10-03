#include<iostream>
#include<cmath>
using namespace std;
float a1,a2,b1,b2,c1,c2,d1,d2;
int main(){
    while(cin>>a1){
        cin>>b1>>c1>>d1>>a2>>b2>>c2>>d2;
        float po=(a1+a2+d1+d2)/100,pe=((a1+a2+b1+b2)/100)*((a1+a2+c1+c2)/100)+((c1+c2+d1+d2)/100)*((b1+b2+d1+d2)/100),k=(po-pe)/(1-pe);
        cout<<"("<<a1<<"+"<<a2<<"+"<<d1<<"+"<<d2<<")/100="<<po<<endl;
        cout<<"(("<<a1<<"+"<<a2<<"+"<<b1<<"+"<<b2<<")/100)(("<<a1<<"+"<<a2<<"+"<<c1<<"+"<<c2<<")/100)+(("<<c1<<"+"<<c2<<"+"<<d1<<"+"<<d2<<")/100)(("<<b1<<"+"<<b2<<"+"<<d1<<"+"<<d2<<")/100)="<<pe<<endl;
        cout<<"("<<po<<"-"<<pe<<")/(1-"<<pe<<")="<<round(k*10000)/10000<<endl;
    }
}
