#pragma once

#define OLED_TIMEOUT 0

// 3x3_+1_OLED_2026.9.26c PCB: OLED J1 SDA -> GP12, SCL -> GP13 (RP2040 I2C0)
#define I2C_DRIVER I2CD0
#define I2C1_SDA_PIN GP12
#define I2C1_SCL_PIN GP13

// No reset switch on the PCB: double-tap the module's RST to enter the UF2 bootloader
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_TIMEOUT 500U
