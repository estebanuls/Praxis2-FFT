void setup() {
  Serial.begin(115200);
}

void loop() {
  int p1 = analogRead(A0);
  int p2 = analogRead(A1);
  int p3 = analogRead(A2);
  int p4 = analogRead(A3);
  int p5 = analogRead(A4);
  int p6 = analogRead(A5);

  Serial.print(p1); Serial.print(",");
  Serial.print(p2); Serial.print(",");
  Serial.print(p3); Serial.print(",");
  Serial.print(p4); Serial.print(",");
  Serial.print(p5); Serial.print(",");
  Serial.println(p6);

  delay(20);
}
