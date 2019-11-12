#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

int dataReady = 0;

void setup(void) 
{
  attachInterrupt(0, triggerData, HIGH);
  
  Serial.begin(9600);
  
  if(!mag.begin())
  {
    /* There was a problem detecting the HMC5883 ... check your connections */
    Serial.println("Ooops, no HMC5883 detected ... Check your wiring!");
    while(1);
  }
}

void triggerData(){
  dataReady = 1;
}

void loop(void)
{
 
   if(dataReady == 1){
    sensors_event_t event;
    mag.getEvent(&event);
    
    /* Donées en micro-tesla */
    Serial.print(event.magnetic.x);Serial.print("\t");
    Serial.print(event.magnetic.y);Serial.print("\t");
    Serial.print(event.magnetic.z);Serial.print("\n");
   }
  
}
