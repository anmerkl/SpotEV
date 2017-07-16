const int pir_1 = 7;
const int pir_2 = 8;

int state = LOW;
int state2 = LOW;
int val = 0;
int val2 = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(pir_1, INPUT);
  pinMode(13, OUTPUT);
  pinMode(pir_2, INPUT);
    
  Serial.begin(115200);
  Serial.println("hihihi");
}

void loop() {
  // put your main code here, to run repeatedly:
  val = digitalRead(pir_1);
  val2 = digitalRead(pir_2);
  if (val == HIGH){
    Serial.print("One is on \t");
    digitalWrite(13, HIGH);
    if (state == LOW){
      Serial.print("One Detected motion \t");
      state = HIGH;
    }
  }
  else if (val == LOW){
    Serial.print("One is off \t");
    digitalWrite(13, LOW);
    if (state == HIGH){
      Serial.print("One Motion ended \t");
      state = LOW;
    }
  }

  if (val2 == HIGH){
    Serial.print("two is on \t");
    if (state2 == LOW){
      Serial.print("two Detected motion \t");
      state2 = HIGH;
    }
  }
  else if (val2 == LOW){
    Serial.print("two is off \t");
    if (state2 == HIGH){
      Serial.print("two Motion ended \t");
      state2 = LOW;
    }
  }

  Serial.println("");
}
