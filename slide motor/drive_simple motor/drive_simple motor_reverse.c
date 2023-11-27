#include<stdio.h>
#include<wiringPi.h>
const int makerobo_motorPin[]={1, 4, 5, 6};
int positon[]={1,2,3,4,5,6,7,8,9,10};
int makerobo_rolePerMinute = 30;
int makerobo_stepsPerRevolution = 1024;
int makerobo_stepSpeed = 0;
int flag=0;

void makerobo_rotary(char direction){
        
if(direction == 'c'){
for(int j=0;j<4;j++){
for(int i=0;i<4;i++){
digitalWrite(makerobo_motorPin[i],0x99>>j &(0x08>>i));}
delayMicroseconds(makerobo_stepSpeed);
}
}
else if(direction == 'a'){
for(int j=0;j<4;j++){
for(int i=0;i<4;i++){
digitalWrite(makerobo_motorPin[i],0x99<<j &(0x80>>i));}
delayMicroseconds(makerobo_stepSpeed);
}
}

}

void makerobo_loop(){
char makerobo_direction ='O';
int c[10000];c[1]=5;
int k=2;
while (1){
flag=0;  makerobo_stepSpeed=(40000000/makerobo_rolePerMinute)/makerobo_stepsPerRevolution; 
printf("scanf 1,2,3,.....:");
scanf("%d",&c[k]);

if (c[k]-c[k-1]>=0){
makerobo_direction='c';
makerobo_stepSpeed/=£¨1+c[k]-c[k-1]£©;
}
else {
makerobo_direction='a';
makerobo_stepSpeed/=£¨1+c[k-1]-c[k]£©;
}
while(1){
        
        makerobo_rotary (makerobo_direction);
        flag++;
        if(flag>=500)break;
        }
delayMicroseconds(10000);
k++;
}
}

int main(void){
if (wiringPiSetup()==-1){
printf("setup wiringPi failed !");
return 0;
}
for (int i = 0; i< 4; i++)
{
pinMode(makerobo_motorPin[i], OUTPUT);
}
makerobo_loop();
return 0;
}
