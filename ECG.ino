#include <SoftwareSerial.h>

SoftwareSerial QuartzBT(10,11); //10->RX, 11->TX
float alpha = 0.9;  // Low-pass filter constant
float filteredValue = 0.0;
int heartRate=0;          // Calculated heart rate
unsigned long previousMillis = 0; // For timing
float threshold=50;

void setup() {
// initialize the serial communication:
Serial.begin(9600);
pinMode(12, INPUT); // Setup for leads off detection LO +//orange//10
pinMode(13, INPUT); // Setup for leads off detection LO -//yellow//11
QuartzBT.begin(9600);  //Default Baud for comm, it may be different for your Module.
Serial.println("The bluetooth gates are open.\n Connect to HC-05 from any other bluetooth device with 1234 as pairing key!.");
 
}
 
void loop() {
 
if((digitalRead(12) == 1)||(digitalRead(13) == 1)){
Serial.println('!');
QuartzBT.print('!');
}
else{
// send the value of analog input 0:
int sensorValue=analogRead(A0);
float fs=millis();
float dt=1/fs;
float tao=7/(44*threshold);
alpha = dt/(tao+dt);
filteredValue = alpha * filteredValue + (1 - alpha) * sensorValue;  // Low-pass filter

Serial.println(filteredValue);

if (filteredValue > threshold) {
    heartRate = map(filteredValue, threshold, 1023, 60, 200);
    Serial.print("Heart Rate: ");
    Serial.println(heartRate);
}

String v=String(filteredValue,5);
String r=String(heartRate);
String output="{\"Value\":"+v+",\"Rate\":"+r+"}";
QuartzBT.println(output);

}
//Wait for a bit to keep serial data from saturating
delay(140);

}
