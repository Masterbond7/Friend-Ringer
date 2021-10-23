// Include EEPROM header to allow access to the EEPROM's data
#include <EEPROM.h>

// Variable to store a number from the EEPROM
int old_value;

void setup() {
    Serial.begin(9600); // Start serial
    
    EEPROM.begin(1);    // Initialize the EEPROM for 1 byte of storage
    old_value = EEPROM.read(0); // Read the value into old_value
    EEPROM.write(0, old_value+1); // Increment the stored value by one

    // Write new data to the EEPROM and end connection
    EEPROM.commit();
    EEPROM.end();
}

void loop() {
    Serial.println(old_value); // Continuously display the old value over serial
}
