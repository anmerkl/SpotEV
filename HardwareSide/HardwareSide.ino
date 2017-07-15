const int pir_1 = 7;
const int pir_2 = 8;

int state = LOW;
int val = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(pir_1, INPUT);
  pinMode(13, OUTPUT);
  pinMode(pir_2, INPUT);
    
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  val = digitalRead(pir_1);
  if (val == HIGH){
    Serial.println("on");
    digitalWrite(13, HIGH);
    if (state == LOW){
      Serial.println("Detected motion");
      state = HIGH;
    }
  }
  else{
    Serial.println("off");
    digitalWrite(13, LOW);
    if (state == HIGH){
      Serial.println("Motion ended");
      state = LOW;
    }
  }
}
