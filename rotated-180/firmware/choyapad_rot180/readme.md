# choyapad_rot180

Same `3x3_+1_OLED_2026.9.26c` PCB as `choyapad`, but for using the macropad **turned 180°** on the desk
(OLED at the front/bottom so the keycaps don't hide it; tray in `../../case/`).

* Key map remapped in `keyboard.json` (`LAYOUT_rot180`): the 3x3 grid keeps its functions in the same places as you
  look at it (what was bottom-right is now top-left in the matrix, and so on); the lone key — now bottom-right,
  beside the OLED — is still LAYER_CYCLE.
* OLED turned 180° in software (`oled_init_user` -> `OLED_ROTATION_180`).
* Matrix (COL2ROW): cols GP2, GP4, GP3; rows GP5, GP6, GP7, GP8 — unchanged.
* OLED (I2C0): SDA GP12, SCL GP13 — unchanged.

    qmk compile -kb choyapad_rot180 -km default

(needs this folder copied or symlinked into `qmk_firmware/keyboards/`).

## Bootloader

* Hold BOOT on the RP2040 module while plugging in, or
* Double-tap the module's RST, or
* Hold the lone key (matrix 0,0 — now bottom-right, next to the OLED) while plugging in (bootmagic)
