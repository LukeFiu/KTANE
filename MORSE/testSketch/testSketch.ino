#define winLed 17
#define loseLed 16
#define BUTTON_PIN 0
#define potPinB 28
#define potPinA 27

bool win = false;
int challengeNum = 5;
bool doCheckWin = false;


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

void setup() {
  pinMode(winLed, OUTPUT);
  pinMode(loseLed, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);

  Serial.begin(9600);

  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), callbackButton, RISING);
}

void loop() {
  if (doCheckWin){
    checkWin();
  }
}

void callbackButton(){
  checkWin();  
}