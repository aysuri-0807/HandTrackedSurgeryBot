#include <Servo.h>
Servo ARM;
Servo ROTATE; 
Servo KNIFE; 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(1);

  ARM.attach(3);
  ROTATE.attach(5);
  KNIFE.attach(6);
  KNIFE.write(180);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n'); // Read until newline
    int firstComma = input.indexOf(','); //Get index of comma (where we seperate two vars)
    if (firstComma > 0) {
      int Rotation = input.substring(0, firstComma).toInt();
      String Arm = input.substring(firstComma + 1);
      ARM.write(Rotation);
      if (Arm == "UP"){
        ARM.write(100);
      }
      else if (Arm == "DOWN"){
        ARM.write(80);
        }
      else{
        ARM.write(90); 
      }
      }
    }
  }
