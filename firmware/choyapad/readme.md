# choyapad

3x3 + 1 macropad with 128x32 SSD1306 OLED, for the `3x3_+1_OLED_2026.9.26c` PCB (RP2040 Pro Micro).

* Matrix (COL2ROW): cols GP2, GP4, GP3; rows GP5, GP6, GP7, GP8
* OLED (I2C0): SDA GP12, SCL GP13

    qmk compile -kb choyapad -km default

## Bootloader

* Hold BOOT on the RP2040 module while plugging in, or
* Double-tap the module's RST, or
* Hold the top key (matrix 0,0) while plugging in (bootmagic)
