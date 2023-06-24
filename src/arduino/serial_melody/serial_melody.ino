# define C 262
# define D 294
# define E 330
# define F 349
# define G 392
# define A 440
# define B 494
# define C2 523

const int NOTES[] = {C,D,E,F,G,A,B,C2}
const int BUZZER_PIN = 13;

void setup() {
  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) {
    char c = Serial.read();

    // 문자로 구성된 숫자를 정수형 숫자로 변형
    // ASCII 코드를 참조하면 답이 있음
    int index = (c - '0') - 1;

    if (index >= 0 && index < 8) {
      int note = NOTES[index];
      tone(BUZZER_PIN, note, 300);
      delay(300);
    }else{
      delay(10);
    }
  }else{
    delay(10);
  }

}
