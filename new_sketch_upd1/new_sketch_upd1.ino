// ─── Pin assignments ─────────────────────────────────────────────────────
const uint8_t DATA_PIN  = 8;
const uint8_t CLOCK_PIN = 12;
const uint8_t LATCH_PIN = 11;

// ─── Segment patterns for digits 0–9 (gfedcba) ──────────────────────────
const uint8_t digitToSegment[10] = {
  0b00111111,  // 0
  0b00000110,  // 1
  0b01011011,  // 2
  0b01001111,  // 3
  0b01100110,  // 4
  0b01101101,  // 5
  0b01111101,  // 6
  0b00000111,  // 7
  0b01111111,  // 8
  0b01101111   // 9
};

// ─── Global Variables ────────────────────────────────────────────────────
uint8_t segments[4] = {0, 0, 0, 0};  // Current segment patterns
int hour = 0, minute = 0;
bool timeSet = false;

unsigned long lastUpdateMillis = 0;  // For tracking passing minutes

// ─── Helper: send 4 bytes (MSB-first) to 74HC595 chain ──────────────────
void shiftOut4(const uint8_t bytesOut[4])
{
  digitalWrite(LATCH_PIN, LOW);
  for (uint8_t i = 0; i < 4; ++i) {
    shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, bytesOut[i]);
  }
  digitalWrite(LATCH_PIN, HIGH);
}

// ─── Helper: update segments[] from current hour and minute ─────────────
void updateSegmentsFromTime()
{
  int h1 = hour / 10;
  int h2 = hour % 10;
  int m1 = minute / 10;
  int m2 = minute % 10;

  segments[0] = digitToSegment[h1];
  segments[1] = digitToSegment[h2];
  segments[2] = digitToSegment[m1];
  segments[3] = digitToSegment[m2];
}

// ─── Setup ──────────────────────────────────────────────────────────────
void setup()
{
  pinMode(DATA_PIN,  OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);

  Serial.begin(9600);
  Serial.println(F("Set time in HHMM format (e.g. 0930 for 9:30):"));
}

// ─── Main loop ──────────────────────────────────────────────────────────
void loop()
{
  // ── 1. Wait for initial input ─────────────────────────────────────────
  if (!timeSet && Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.length() == 4 &&
        isDigit(line.charAt(0)) &&
        isDigit(line.charAt(1)) &&
        isDigit(line.charAt(2)) &&
        isDigit(line.charAt(3))) {
      
      int h = (line.charAt(0) - '0') * 10 + (line.charAt(1) - '0');
      int m = (line.charAt(2) - '0') * 10 + (line.charAt(3) - '0');

      if (h >= 0 && h <= 23 && m >= 0 && m <= 59) {
        hour = h;
        minute = m;
        updateSegmentsFromTime();
        shiftOut4(segments);
        lastUpdateMillis = millis();
        timeSet = true;
        Serial.println(F("Clock started."));
      } else {
        Serial.println(F("Invalid time. Enter HHMM (0000–2359):"));
      }
    } else {
      Serial.println(F("Invalid input. Enter 4 digits in HHMM format."));
    }
  }

  // ── 2. Update display every ~1 second (optional fade) ─────────────────
  if (timeSet) {
    shiftOut4(segments);
    delay(50); // Smooth refresh

    // ── 3. Update time every minute ─────────────────────────────────────
    if (millis() - lastUpdateMillis >= 60000UL) {
      lastUpdateMillis += 60000UL;
      minute++;
      if (minute >= 60) {
        minute = 0;
        hour++;
        if (hour >= 24) {
          hour = 0;
        }
      }
      updateSegmentsFromTime();
    }
  }
}
