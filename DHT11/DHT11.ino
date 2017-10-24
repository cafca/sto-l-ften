#include <SimpleDHT.h>

int pinDHT11 = 2;
int counter = 0;
SimpleDHT11 dht11;

void setup() {
  Serial.begin(9600);
}

void loop() {
  counter += 1;
  Serial.print(counter);
  Serial.print(" >>> ");
  
  byte temperature = 0;
  byte humidity = 0;
  byte data[40] = {0};
  if (dht11.read(pinDHT11, &temperature, &humidity, data)) {
    Serial.print("FAIL");
    return;
  }

  Serial.print((int)temperature); Serial.print("C ");
  Serial.print((int)humidity); Serial.println("H");
  
  delay(1000);
}
