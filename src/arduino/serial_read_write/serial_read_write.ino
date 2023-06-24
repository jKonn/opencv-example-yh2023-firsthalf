char cmd;

void setup() {
  
  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) {
    cmd = Serial.read();
    Serial.println(cmd);
    cmd = NULL;
  }
  delay(10);
}
