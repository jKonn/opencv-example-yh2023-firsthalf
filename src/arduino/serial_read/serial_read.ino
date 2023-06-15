char cmd;
void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}
void loop() {

  digitalWrite(13, LOW);
  if (Serial.available() > 0) {
    cmd = Serial.read();

    if (cmd == 'w') {
      digitalWrite(13, HIGH);
      delay(500);
      digitalWrite(13, LOW);
      delay(500);
    }
  }
  delay(10);
}
