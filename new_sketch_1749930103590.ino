/*
   4-digit 7-segment display driven by four cascaded 74HC595 shift registers.
   ─────────────────────────────────────────────────────────────────────────
   - Accepts a 4-digit number over the Serial monitor (e.g. 1234).
   - Translates each digit to its 7-segment pattern (common-cathode: HIGH = LED ON).
   - Shifts the four patterns out MSB-first to the shift-register chain.
   - Keeps displaying the number until new input arrives.
*/

// ─── Pin assignments (change if you wired them differently) ──────────────
const uint8_t DATA_PIN  = 8;   // DS  of first 74HC595
const uint8_t CLOCK_PIN = 12;  // SH_CP
const uint8_t LATCH_PIN = 11;  // ST_CP

// ─── Segment patterns for digits 0-9 (gfedcba) ───────────────────────────
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

// ─── Globals ─────────────────────────────────────────────────────────────
uint8_t segments[4] = {0, 0, 0, 0};   // current patterns to show
bool     newNumber  = true;           // flag: need fresh user input?

// ─── Helper: send 4 bytes (MSB-first) to 74HC595 chain ───────────────────
void shiftOut4(const uint8_t bytesOut[4])
{
  digitalWrite(LATCH_PIN, LOW);
  for (uint8_t i = 0; i < 4; ++i) {
    shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, bytesOut[i]);
  }
  digitalWrite(LATCH_PIN, HIGH);
}

// ─── Setup ───────────────────────────────────────────────────────────────
void setup()
{
  pinMode(DATA_PIN,  OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);

  Serial.begin(9600);
  Serial.println(F("Enter 4 digits (e.g. 1234) then press ⏎"));
}

// ─── Main loop ───────────────────────────────────────────────────────────
void loop()
{
  // ── 1. If we need new input, poll Serial until we get exactly 4 digits ──
  if (newNumber) {
    if (Serial.available()) {
      String line = Serial.readStringUntil('\n');
      line.trim();
      if (line.length() == 4 && line.charAt(0) >= '0' && line.charAt(0) <= '9'
                              && line.charAt(1) >= '0' && line.charAt(1) <= '9'
                              && line.charAt(2) >= '0' && line.charAt(2) <= '9'
                              && line.charAt(3) >= '0' && line.charAt(3) <= '9') {
        for (uint8_t i = 0; i < 4; ++i) {
          segments[i] = digitToSegment[line.charAt(i) - '0'];
        }
        newNumber = false;          // ready to display
        Serial.println(F("Displaying…  (enter new digits any time)"));
      } else {
        Serial.println(F("Invalid input – please type exactly 4 digits."));
      }
    }
  }

  // ── 2. Continuously refresh the display (74HC595 latches output) ───────
  if (!newNumber) {
    shiftOut4(segments);
    delay(50);                      // ~20 FPS; adjust if needed
  }

  // ── 3. Check if user typed something new while we were displaying ──────
  if (Serial.available()) {
    newNumber = true;               // next loop iteration will read it
  }
}
