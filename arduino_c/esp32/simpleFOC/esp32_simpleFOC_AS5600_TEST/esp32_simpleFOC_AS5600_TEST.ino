#include <SimpleFOC.h>

// MagneticSensorI2C(uint8_t _chip_address, float _cpr, uint8_t _angle_register_msb)
//  chip_address         - I2C chip address
//  bit_resolution       - resolution of the sensor
//  angle_register_msb   - angle read register msb
//  bits_used_msb        - number of used bits in msb register
MagneticSensorI2C as5600 = MagneticSensorI2C(0x36, 12, 0x0E, 4);
// or quick config
//MagneticSensorI2C as5600 = MagneticSensorI2C(AS5600_I2C);

void setup() {
  // monitoring port
  Serial.begin(115200);

  // init magnetic sensor hardware
  as5600.init();

  Serial.println("AS5600 ready");
  _delay(1000);
}

void loop() {
  // display the angle and the angular velocity to the terminal
  Serial.print(as5600.getAngle());
  Serial.print("\t");
  Serial.println(as5600.getVelocity());
}
