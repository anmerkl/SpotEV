#include <Pixy.h>
#include <PixyI2C.h>
#include <PixySPI_SS.h>
#include <PixyUART.h>
#include <TPixy.h>

#define trigPin 12
#define echoPin 11

#define trigPin2 10
#define echoPin2 9

const int NUM_SAMPLES = 200;
const float SUCCESS_PERCENT = 0.60;
int countOne = 0;
int countTwo = 0;

void setup()
{
    Serial.begin(9600);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(trigPin2, OUTPUT);
    pinMode(echoPin2, INPUT);
}

int poll(int tP, int eP)
{
    int trigP = tP;
    int echoP = eP;

    long duration, distance;
    digitalWrite(trigP, LOW);
    delayMicroseconds(2);
    digitalWrite(trigP, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigP, LOW);
    duration = pulseIn(echoP, HIGH);
    delayMicroseconds(10);
    distance = (duration / 2) / 29.1;
    Serial.print(distance);
    Serial.print(" cm \t\t");

    if (distance < 250)
    { // check this 300 number for the max distance required to register a car
        return 1;
    }
    else
    {
        return 0;
    }
}

void loop()
{
    for (int i = 0; i < NUM_SAMPLES; i++)
    {
        int n = poll(trigPin, echoPin);
        leftSensor[i] =
            delay(20);
    }

    poll(trigPin2, echoPin2);
    Serial.println("");
    delay(300);
}
