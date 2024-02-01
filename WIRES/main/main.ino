#include <Array.h>

#define winLed 9
#define loseLed 8

#define sensorPin0 A0
#define sensorPin1 A1
#define sensorPin2 A2
#define sensorPin3 A3
#define sensorPin4 A4
#define sensorPin5 A5

const int wires[6] = {sensorPin0,sensorPin1,sensorPin2,sensorPin3,sensorPin4,sensorPin5};
Array<int,6> availableWires;

char serialNo[] = "AL50F2";

int sensorValue = 0;       // sensorPin default value
float Vin = 4.8;             // Input voltage
float Vout = 0;            // Vout default value
float Rref = 330;          // Reference resistor's value in ohms (you can give this value in kiloohms or megaohms - the resistance of the tested resistor will be given in the same units)
float R = 0;  

//colour defenitions
int black[] = {10, 100};
int red[] = {300, 400};
int blue[] = {500, 700};
int yellow[] = {800, 2000};
int white[] = {2500, 5000};

int wireCount;
int wireToCut;
bool win = false;



bool isLastDigitOdd(){
  char last = (serialNo[sizeof(serialNo)/sizeof(serialNo[0])-2]);
  return last%2;
}

float measureWire(int pin){
  sensorValue = analogRead(pin);
  Vout = (Vin * sensorValue) / 1023;    
  R = Rref * (1 / ((Vin / Vout) - 1));  
  Serial.print("R: ");                  
  Serial.println(R);    
  return R;                
}

bool checkForWire(int pin){
  R = measureWire(pin);
  if (R > 5000){
    return false;
  } else {
    return true;
  }
}

int getLastWireOfColour(int colour[]){
  int wireIndex;
  for (int i=0; i < 6; i++){
    if (checkWireForColour(wires[i],colour)){
      wireIndex = i;
    }
  }
  return wireIndex;
}

bool checkWireForColour(int pin, int colour[]){
  R = measureWire(pin);
  if (R > colour[0] && R <= colour[1]){
    return true;
  }
  return false;
}

int getColourCount(int colour[]){
  int wiresOfColour = 0;
  for (int i=0; i < 6; i++){
    if (checkWireForColour(wires[i], colour)){
      wiresOfColour++;
    }
  }
  return wiresOfColour;
}

void initWires(){
  availableWires.clear();
  int numWires = 6;
  for (int i= 0; i < 6; i++){
    R = measureWire(wires[i]); 
    if (R > 5000){
      numWires--;
    } else {
      availableWires.push_back(i);
    }
  } 
  wireCount = numWires; 
}

int checkWireCount(){
  int numWires = 6;
  for (int i= 0; i < 6; i++){
    R = measureWire(wires[i]); 
    if (R > 5000){
      numWires--;
    } 
  } 
  return numWires;                            
}

void getWireToCut(int numWires){
  switch (numWires) {
    case 3:
      Serial.println("case 3");
      Serial.println();
      if (getColourCount(red) == 0){
        wireToCut = availableWires[1];
      } else if (checkWireForColour(white, availableWires.back()) == true){
        wireToCut = availableWires.back();
      } else if (getColourCount(blue) > 1){
        wireToCut = getLastWireOfColour(blue);
      }else{
        wireToCut = availableWires.back();
      }
      break;

    case 4:
      Serial.println("case 4");
      Serial.println();
      if (isLastDigitOdd() && getColourCount(red) > 1){
        wireToCut = getLastWireOfColour(red);
      } else if (checkWireForColour(yellow, availableWires.back()) && getColourCount(red) == 0){
        wireToCut = availableWires[0];
      } else if (getColourCount(blue) == 1){
        wireToCut = availableWires[0];
      } else if (getColourCount(yellow) > 1){
        wireToCut = availableWires.back();
      } else {
        wireToCut = availableWires[1];
      }
      break;

    case 5:
      Serial.println("case 5");
      Serial.println();
      if (checkWireForColour(black, availableWires.back()) && isLastDigitOdd()){
        wireToCut = availableWires[3];
      } else if (getColourCount(red) == 1 && getColourCount(yellow) > 1){
        wireToCut = availableWires[0];
      } else if (getColourCount(black) == 0){
        wireToCut = availableWires[1];
      } else {
        wireToCut = availableWires[0];
      }
      break;

    case 6:
      Serial.println("case 6");
      Serial.println();
      if ((getColourCount(yellow) == 0) && (isLastDigitOdd())){
        wireToCut = availableWires[2];
      } else if (getColourCount(yellow) == 1 && getColourCount(white) > 1){
        wireToCut = availableWires[3];
      } else if (getColourCount(red) == 0){
        wireToCut = availableWires.back();
      } else {
        wireToCut = availableWires[3];
      }
      break;
  }
}

void setup ()
{
  pinMode(winLed, OUTPUT);
  pinMode(loseLed, OUTPUT);
  Serial.begin(9600);      // Initialize serial communications at 9600 bps
  initWires();
  getWireToCut(wireCount);
}

void loop ()
{
  if(!win){
    int currentWireCount = checkWireCount();
    Serial.println(currentWireCount);

    if (currentWireCount != wireCount){
      if (!checkForWire(wireToCut)){
        Serial.println("WIN");
        win = true;
        digitalWrite(winLed, HIGH);
      } else {
        Serial.println("WRONG");
        wireCount--;
        digitalWrite(loseLed, HIGH);
        delay(300);
        digitalWrite(loseLed, LOW);
      }
    }
  }
  delay(1000);
}
