#include <AltSoftSerial.h>

#define RE 6
#define DE 7
AltSoftSerial mod;

const byte nitro[] = {0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xe4, 0x0c};
const byte phos[] = {0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc};
const byte pota[] = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0};

byte values[11];
byte val1, val2, val3;

void setup() {
  Serial.begin(4800);
  mod.begin(4800);
  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);
  delay(1000);
}

void loop() {
  readNPK(); // Read NPK sensors
  
  // Send values to Raspberry Pi

  delay(10000);
}

void readNPK() {
  val1 = readSensor(nitro);
  val2 = readSensor(phos);
  val3 = readSensor(pota);

  Serial.print(val1);
  Serial.print(", "); // Add comma and space after val1
  Serial.print(val2);
  Serial.print(", "); // Add comma and space after val2
  Serial.print(val3);
  Serial.println(" ");
}
byte readSensor(const byte* sensor) {
  mod.flushInput();
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(1);
  for (uint8_t i = 0; i < sizeof(sensor); i++ ) mod.write(sensor[i]);
  mod.flush();
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);
  delay(100);
  for (byte i = 0; i < 7; i++) {
    values[i] = mod.read();
  }
  return values[4];
}

