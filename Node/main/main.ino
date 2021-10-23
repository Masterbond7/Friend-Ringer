#include <EEPROM.h>

int old_value;

void setup() {
    Serial.begin(9600);
    EEPROM.begin(1);
    old_value = EEPROM.read(0);
    EEPROM.write(0, old_value+1);
    EEPROM.commit();
}

void loop() {
    Serial.println(old_value);
}
