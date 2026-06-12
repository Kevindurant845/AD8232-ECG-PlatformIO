#include <Arduino.h>

#define AD8232_PIN 35
#define SAMPLING_FREQUENCY 360
#define SAMPLE_DURATION 30

#define LO_PLUS 32
#define LO_MINUS 33

const int total_samples = SAMPLING_FREQUENCY * SAMPLE_DURATION;

void sendJSON();

unsigned long last_sample_time = 0;
unsigned long sample_interval = 1000000 / SAMPLING_FREQUENCY;

int ecg_data[total_samples];

int sample_index = 0;
bool done_sampling = false;

void setup()
{
  Serial.begin(115200);
  delay(1000);

  pinMode(LO_PLUS, INPUT);
  pinMode(LO_MINUS, INPUT);

  Serial.println("Starting ECG capture...");
}

void loop()
{
  if (done_sampling) return;

  if (digitalRead(LO_PLUS) == 1 || digitalRead(LO_MINUS) == 1)
  {
    Serial.println("Leads disconnected!");
  }
  else
  {
    unsigned long current_time = micros();

    if (current_time - last_sample_time >= sample_interval)
    {
      ecg_data[sample_index] = analogRead(AD8232_PIN);

      sample_index++;
      last_sample_time = current_time;

      if (sample_index >= total_samples)
      {
        done_sampling = true;
        sendJSON();
      }
    }
  }
}

void sendJSON()
{
  Serial.print("{\"ecg\":[");

  for (int i = 0; i < total_samples; i++)
  {
    Serial.print(ecg_data[i]);

    if (i < total_samples - 1)
      Serial.print(",");
  }

  Serial.println("]}");
  Serial.println("Done!");
}