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

float carOneTime = 0;
float carTwoTime = 0;

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
    Serial.println(" cm");

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
        countOne += n;
        delay(20);
    }
    if (NUM_SAMPLES * SUCCESS_PERCENT < countOne)
    {
        Serial.println("Object one is found!");
        carOneTime += NUM_SAMPLES * 0.02 + 0.01;
    }
    else
    {
        Serial.println("Could not find the first object ... moving on");
        carOneTime = 0;
    }

    for (int i = 0; i < NUM_SAMPLES; i++)
    {
        int n = poll(trigPin2, echoPin2);
        countTwo += n;
        delay(20);
    }
    if (NUM_SAMPLES * SUCCESS_PERCENT < countTwo)
    {
        Serial.println("Object two is found!");
        carTwoTime = NUM_SAMPLES * 0.02 + 0.01;
    }
    else
    {
        Serial.println("Could not find the second object ... moving on");
        carTwoTime = 0;
    }

    countOne = 0;
    countTwo = 0;
    delay(300);
}

// JSON Object Schema:
// { 'spot': { 'id': 1, 'location': 'building 10', 'occupied': 'true', 'prev_occupy_duration': 134 } }
