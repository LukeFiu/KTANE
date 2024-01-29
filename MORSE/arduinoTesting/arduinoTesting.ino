// Demo the quad alphanumeric display LED backpack kit
// scrolls through every character, then scrolls Serial
// input onto the display

#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

//For letters
char* letters[] = {
".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", // A-I
".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", // J-R 
"...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.." // S-Z
};

//For Numbers
char* numbers[] = {
  "-----", ".----", "..---", "...--", "....-", ".....",
"-....", "--...", "---..", "----."
};

char * words[] = {"shell", "halls", "slick", "trick", "boxes", "leaks", "strobe", "bistro", "flick", "bombs", "break", "brick", "steak", "sting", "vector", "beats"};

#define potPinB 28
#define potPinA 27
#define buttonPin 0
#define ledPin 15
#define winLed 17
#define loseLed 16
int indexTime = 0;
int reqDel = 0;
int dotDelay = 200;
int finalSeq[] = {};
int *sequence[] = {};
char challenge[6];
int challengeNum;
bool win = false;
bool doCheckWin = false;
char morseLetter;
char ch;
bool morseCharSpace = false;

static const PROGMEM uint8_t alphafonttable[] = {
    0b01001111, // 0
    0b00000110, // 1
    0b01011011, // 2
    0b01001111, // 3
    0b01100110, // 4
    0b01101111, // 5
    0b01111101, // 6
    0b00000111, // 7
    0b01111111, // 8
    0b01101111 // 9
};



Adafruit_AlphaNum4 alpha4 = Adafruit_AlphaNum4();


int map(int x, float in_min, float in_max, float out_min, float out_max){
  return int((x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min);
}

void checkWin(){
  int measureOne = analogRead(potPinA);
  int measureTwo = analogRead(potPinB);

  int answer = map((measureOne + measureTwo)/2, 0, 1023, 0, 16);
  if (answer == challengeNum){
    win = true;
    Serial.println("Win");
  } else {
    win = false; 
    Serial.println("lose, Try again");
  }

  digitalWrite(winLed, win);
  digitalWrite(loseLed, !win);
  doCheckWin = false;
}

void callbackButton(){
  doCheckWin = true;  
}

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(winLed, OUTPUT);
  pinMode(loseLed, OUTPUT);
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  
  alpha4.begin(0x70);  // pass in the address
  Serial.println("Start typing to display!");

  randomSeed(analogRead(26));
  challengeNum = random(0, 15);
  memcpy(challenge, words[challengeNum], 6);

  attachInterrupt(digitalPinToInterrupt(buttonPin), callbackButton, RISING);
}


char displaybuffer[4] = {'3', ' ', ' ', ' '};


int i = 0;
int j = 0;
void loop() {
  if(millis() - indexTime >= reqDel){
    digitalWrite(ledPin, LOW);
    if (morseCharSpace){
      reqDel = dotDelay * 3;
      indexTime = millis();
      morseCharSpace = false;
    } else {
      ch = challenge[i]; // read a single letter if (ch >= 'a' && ch <= 'z')
      if (ch != NULL){
        //Serial.print(ch);
        if (ch >= 'a' && ch <= 'z') {
          morseLetter = letters[ch - 'a'][j];
        }
        else if (ch >= 'A' && ch <= 'Z') {
          morseLetter = letters[ch - 'A'][j]; }
        else if (ch >= '0' && ch <= '9') {
          morseLetter = numbers[ch - '0'][j]; }
        else if (ch == ' ') {
          morseLetter = ' ';
        }
        Serial.print(morseLetter);
        if (morseLetter != NULL){
          if (morseLetter == '.'){
            reqDel = dotDelay;
            indexTime = millis();
            digitalWrite(ledPin, HIGH);
            morseCharSpace = true;
            j++;
          }
          else if (morseLetter == '-'){
            reqDel = dotDelay * 3;
            indexTime = millis();
            digitalWrite(ledPin, HIGH);
            morseCharSpace = true;
            j++; 
          } 
        } else {
          j = 0;
          i++;
          reqDel = dotDelay * 4;
          indexTime = millis();
        }
      } else {
        i = 0;
        j = 0;
        reqDel = dotDelay * 7;
        indexTime = millis();
      }
    }
  }
  
  // Serial.println(analogRead(potPinA));
  // Serial.println(analogRead(potPinB));
  // Serial.println();
  int measureOne = analogRead(potPinA);
  int measureTwo = analogRead(potPinB);

  int num = map((measureOne + measureTwo)/2, 0, 1023, 0, 16);

  switch (num) {
    case 0:
      displaybuffer[1] = '5';
      displaybuffer[2] = '0';
      displaybuffer[3] = '5';
      break;
    case 1:
      displaybuffer[1] = '5';
      displaybuffer[2] = '1';
      displaybuffer[3] = '5';
      break;
    case 2:
      displaybuffer[1] = '5';
      displaybuffer[2] = '2';
      displaybuffer[3] = '2';
      break;
    case 3:
      displaybuffer[1] = '5';
      displaybuffer[2] = '3';
      displaybuffer[3] = '2';
      break;
    case 4:
      displaybuffer[1] = '5';
      displaybuffer[2] = '3';
      displaybuffer[3] = '5';
      break;
    case 5:
      displaybuffer[1] = '5';
      displaybuffer[2] = '4';
      displaybuffer[3] = '2';
      break;
    case 6:
      displaybuffer[1] = '5';
      displaybuffer[2] = '4';
      displaybuffer[3] = '5';
      break;
    case 7:
      displaybuffer[1] = '5';
      displaybuffer[2] = '5';
      displaybuffer[3] = '2';
      break;
    case 8:
      displaybuffer[1] = '5';
      displaybuffer[2] = '5';
      displaybuffer[3] = '5';
      break;
    case 9:
      displaybuffer[1] = '5';
      displaybuffer[2] = '6';
      displaybuffer[3] = '5';
      break;
    case 10:
      displaybuffer[1] = '5';
      displaybuffer[2] = '7';
      displaybuffer[3] = '2';
      break;
    case 11:
      displaybuffer[1] = '5';
      displaybuffer[2] = '7';
      displaybuffer[3] = '5';
      break;
    case 12:
      displaybuffer[1] = '5';
      displaybuffer[2] = '8';
      displaybuffer[3] = '2';
      break;
    case 13:
      displaybuffer[1] = '5';
      displaybuffer[2] = '9';
      displaybuffer[3] = '2';
      break;
    case 14:
      displaybuffer[1] = '5';
      displaybuffer[2] = '9';
      displaybuffer[3] = '5';
      break;
    case 15:
      displaybuffer[1] = '6';
      displaybuffer[2] = '0';
      displaybuffer[3] = '0';
      break;
  }

  // while (! Serial.available()) return;

  // char c = Serial.read();
  // if (! isprint(c)) return; // only printable!
  
  // // scroll down display
  // displaybuffer[0] = displaybuffer[1];
  // displaybuffer[1] = displaybuffer[2];
  // displaybuffer[2] = displaybuffer[3];
  // displaybuffer[3] = c;

  // set every digit to the buffer
  alpha4.writeDigitRaw(0,0b0100000010001111);
  //alpha4.writeDigitAscii(0, displaybuffer[0]);
  alpha4.writeDigitAscii(1, displaybuffer[1]);
  alpha4.writeDigitAscii(2, displaybuffer[2]);
  alpha4.writeDigitAscii(3, displaybuffer[3]);

  // write it out!
  alpha4.writeDisplay();
  delay(200);
  if (doCheckWin){
    checkWin();
  }
}