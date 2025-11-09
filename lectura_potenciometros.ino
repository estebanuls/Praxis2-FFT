void setup() {
  Serial.begin(115200);
}

void loop() {
  int p1 = analogRead(A0);
  int p2 = analogRead(A1);
  int p3 = analogRead(A2);
  int p4 = analogRead(A3);
  Serial.print(p1); Serial.print(",");
  Serial.print(p2); Serial.print(",");
  Serial.print(p3); Serial.print(",");
  Serial.println(p4);
  delay(20);
}
