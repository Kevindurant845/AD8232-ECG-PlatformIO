#include <Arduino.h>

#define AD8232_PIN 4
#define SAMPLING_FREQUENCY 360

unsigned long last_sample_time = 0;
unsigned long sample_interval = 1000000 / SAMPLING_FREQUENCY;

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  unsigned long current_time = micros();

  if (current_time - last_sample_time >= sample_interval)
  {
    int ecg = analogRead(AD8232_PIN);
    Serial.println(ecg);
    last_sample_time = current_time;
  }
}