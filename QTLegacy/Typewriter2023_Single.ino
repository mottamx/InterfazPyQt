/*Typewriter ver. Single char
The document parsing is entirely on the PC software
This version only receives the exact bit combination to print a char
Place it on both encoders and then enable them
*/
int timekeystroke=250; //Time for key to be pressed, in ms
//Pins decoder 1
const int S0_1 = 2; 
const int S1_1 = 3;
const int S2_1 = 4; 
const int EN_1 = 5; 
//Pins decoder 2
const int S0_2 =  9; 
const int S1_2 = 10;
const int S2_2 = 11; 
const int EN_2 = 12; 

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  //Decoder 1
  pinMode(S0_1, OUTPUT);
  pinMode(S1_1, OUTPUT);
  pinMode(S2_1, OUTPUT);
  pinMode(EN_1, OUTPUT);
  //Decoder 2
  pinMode(S0_2, OUTPUT);
  pinMode(S1_2, OUTPUT);
  pinMode(S2_2, OUTPUT);
  pinMode(EN_2, OUTPUT);  
  //Serial.println("Ready");
  digitalWrite(EN_1, HIGH); //High disables exits
  digitalWrite(EN_2, HIGH);
}

void loop() {
  //Waits for string of bits
  while(Serial.available()){
    received= Serial.readString();
    //Serial.println(received);
    //Decoder 1
    digitalWrite(S0_1, received[0]);
    digitalWrite(S1_1, received[1]);
    digitalWrite(S2_1, received[2]);
    //Decoder 2
    digitalWrite(S0_2, received[3]);
    digitalWrite(S1_2, received[4]);
    digitalWrite(S2_2, received[5]);
    //Now enable decoders to get connection
    digitalWrite(EN_1, LOW);
    digitalWrite(EN_2, LOW);
    delay(timekeystroke);
    digitalWrite(EN_1, HIGH); //High disables exits
    digitalWrite(EN_2, HIGH);
  }
}

//Carlos Motta
//https://github.com/mottamx/
