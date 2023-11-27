#include<stdio.h>
#include<wiringPi.h>

const int makerobo_motorPin[]={1, 4, 5, 6};
const int makerobo_motorPins[]={7, 0, 2, 3};
int makerobo_rolePerMinute = 15;
int makerobo_stepsPerRevolution = 2048;
int makerobo_stepSpeed = 0;
int makerobo_stepSpeeds = 0;

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

void makerobo_rotarys(char direction){
if(direction == 'c'){
for(int j=0;j<4;j++){
for(int i=0;i<4;i++){
digitalWrite(makerobo_motorPins[i],0x99>>j &(0x08>>i));}
delayMicroseconds(makerobo_stepSpeeds);
}
}
else if(direction == 'a'){
for(int j=0;j<4;j++){
for(int i=0;i<4;i++){
digitalWrite(makerobo_motorPins[i],0x99<<j &(0x80>>i));}
delayMicroseconds(makerobo_stepSpeeds);
}
}
}


void makerobo_loop(){
char makerobo_direction ='a';char makerobo_directions ='a';
while(1){
makerobo_rotary (makerobo_direction);
makerobo_rotarys (makerobo_directions);
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
pinMode(makerobo_motorPins[i], OUTPUT);
}
makerobo_stepSpeed=(50000000/makerobo_rolePerMinute)/makerobo_stepsPerRevolution;
makerobo_stepSpeeds=(60000000/makerobo_rolePerMinute)/makerobo_stepsPerRevolution;
makerobo_loop();
return 0;

}
