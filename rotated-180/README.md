# 26c macropad turned 180° (2026-10-24)

Use the macropad turned round so the OLED is at the FRONT (nearest you, low end of the slope) instead of behind
the keycaps. Same PCB, same cover plate (`../case/3x3_+1_OLED_2026.9.26c_cover-plate_no-pin-hole.*`, just turned
round with the board) — only the tray and the firmware change.

## case/
| file | |
|---|---|
| `choyapad-rot180-tilt10_tray-choya-2color.3mf` | Bambu 2.5 project, 10° tilt, same 2 manual colour swaps as before (start CASE colour). Sliced OK with the 2.5 CLI: ~30 g, ~1 h 18 |
| `choyapad-rot180-tilt10_tray-choya.stl` | single-colour version (text cut 0.6 into the bottom) |
| `..._2color_body.stl` / `..._choya-inlay.stl` | 2-colour parts as separate STLs |
| `build_tray-rot180.py` | `python3 build_tray-rot180.py <out-prefix> [tilt]` — reuses `../../case/build_cover-plate.py` |
| `tray-rot180-heightmap.png` | top view (brighter = taller; top of image = back) |

- Same wedge as the old TILT10 tray (front 11.1 mm, back 26.5 mm), but the tray inside is spun 180°:
  the 3x3 grid end is now up the back, the OLED end + Pro Micro at the front.
- USB opening is now on the LEFT side, near the front.
- Pro Micro pocket is now front-left: 8.9 mm room under it (flat tray had 6.5).
- "choyapad" stays on the same spot on the bottom (now under the high back), same way round as on the original tray (turning it 180 read upside down).

## firmware/
`choyapad_rot180/` = QMK keyboard (copy of `choyapad` with `LAYOUT_rot180` + OLED rotated 180°).
Build: copy (or symlink) `firmware/choyapad_rot180/` into `qmk_firmware/keyboards/`, then `qmk compile -kb choyapad_rot180 -km default`.
Grid keys keep their functions where you see them; the lone key (now bottom-right beside the OLED) is still LAYER_CYCLE.
