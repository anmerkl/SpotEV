#define trigPin 12
#define echoPin 11

#define trigPin2 10
#define echoPin2 9

void setup()
{
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
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
  String s = distace + " cm";
  Serial.println(s);
  
}

void loop()
{
  poll(trigPin, echoPin);
  delay(20);

  poll(trigPin2, echoPin2);
  delay(300);
}

