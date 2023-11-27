#include<stdio.h>
#include<wiringPi.h>

const int makerobo_motorPin[]={1, 4, 5, 6 };
int makerobo_rolePerMinute = 30;
int makerobo_stepsPerRevolution = 1024;
int makerobo_stepSpeed = 0;

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
while (1){
printf("Makerobo select motor direction a=anticlockwise,c=clockwise:");
makerobo_direction=getchar();
if (makerobo_direction =='c'){
printf("Makerobo motor running clockwise\n");
break;
}
else if (makerobo_direction =='a'){
printf("Makerobo motor running anti-clockwise\n");
break;
}
else{
        printf("Makerobo input error, please try again!\n");
}

}
while(1){
makerobo_rotary (makerobo_direction);
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
makerobo_stepSpeed=(60000000/makerobo_rolePerMinute)/makerobo_stepsPerRevolution;
makerobo_loop();
return 0;

}
