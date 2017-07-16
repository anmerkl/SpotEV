#define trigPin 12
#define echoPin 11

#define trigPin2 10
#define echoPin2 9

void setup()
{
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
}

void poll(int tP, int eP)
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
  distance = (duration/2) / 29.1;
  Serial.print(distance);
  Serial.print(" cm \t\t");
}

void loop()
{
  poll(trigPin, echoPin);
  delay(20);

  poll(trigPin2, echoPin2);
  Serial.println("");
  delay(300);
}

