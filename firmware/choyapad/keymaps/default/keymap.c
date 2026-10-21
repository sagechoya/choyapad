// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later
#include QMK_KEYBOARD_H
#include <string.h>


enum layers {
      CHOYA,
      // Add new layers here, e.g.:
      CHONTINUED,
      NUM_LAYERS
  };

static const char * const layer_names[] = {
      [CHOYA] = "CHOYA",
      [CHONTINUED] = "CHONTINUED",
  };

// Short display names for the 9 keys (rows 1-3) on each layer
static const char * const key_names[2][9] = {
    [CHOYA] = {"GW2", "SNIFF", "aaa", "NAT", "JAB", "aa", "TEQ", "LLA", "CHAK"},
    [CHONTINUED] = {"OCTO", "OOZE", "SEER", "DEPTHS", "BEAR", "BEAM", "WIZ", "DS", "KKAR"},
};

// Write str left-aligned, padded with spaces to `width` chars
static void oled_write_padded(const char *str, uint8_t width) {
    uint8_t len = (uint8_t)strlen(str);
    oled_write(str, false);
    for (uint8_t i = len; i < width; i++) {
        oled_write_char(' ', false);
    }
}

   // ── OLED ──────────────────────────────────────────────────────────────────────
void keyboard_post_init_user(void) {
    oled_on();
}

bool oled_task_user(void) {
      oled_on();
      uint8_t layer = get_highest_layer(layer_state);

      // Line 1: layer name
      oled_write_P(PSTR("Lyr:"), false);
      if (layer < NUM_LAYERS && layer_names[layer]) {
          oled_write_ln(layer_names[layer], false);
      } else {
          oled_write_ln(get_u8_str(layer, ' '), false);
      }

      // Lines 2-4: 3x3 key name grid (7 chars per column = 21 chars/line on 128px)
      for (uint8_t i = 0; i < 9; i++) {
          const char *kname = (layer < NUM_LAYERS) ? key_names[layer][i] : "?";
          oled_write_padded(kname, 7);
      }

      return false;
  }

enum custom_keycodes {
      LAYER_CYCLE = SAFE_RANGE,
      OPEN_GW2,
      LLA,
      CHAK,
      OCTO,
      OOZE,
      SEER,
      MOTH,
      SNIFF,
      aaa,
      SP,
      KC,
      EW,
      DE,
    DEPTHS,
    BEARVERGENCE,
    BEAMVERGENCE,
    CHOVERGENCE,
    CHOYASTORM,
    CHOYAKKAR,
    TEQUATL,
    NATTER,
    JABBERS,
    AA
  };


 bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (keycode == AA && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("aaaaaaaaaaa"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == JABBERS && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("*jabbers*"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == NATTER && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("*natters*"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == TEQUATL && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("/say [&BNABAAA=]"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == CHOYAKKAR && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("/say [&BDkMAAA=]"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == CHOYASTORM && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("/say [&BAkMAAA=]"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == CHOVERGENCE && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("/say [&BB8OAAA=]"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == BEAMVERGENCE && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("/say [&BDYQAAA=]"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == BEARVERGENCE && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("/say [&BK4OAAA=]"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
    if (keycode == DEPTHS && record->event.pressed) {
        tap_code(KC_ENTER); wait_ms(100);
        send_string_with_delay_P(PSTR("/say [&BDYQAAA=]"), 5);
        wait_ms(50); tap_code(KC_ENTER);
        return false;
    }
      if (record->event.pressed) {
          switch (keycode) {
              case LAYER_CYCLE:
                  layer_move((get_highest_layer(layer_state) + 1) % NUM_LAYERS);
                  return false;
              case OPEN_GW2:
                  SEND_STRING(SS_LGUI("r") SS_DELAY(500) "C:\\path\\to\\launch_games.bat"
  SS_TAP(X_ENTER));
                  return false;
              case LLA:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BEwCAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case CHAK:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BPUHAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case OCTO:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BAYIAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case OOZE:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BPgLAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case SEER:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BPwPAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case MOTH:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BJ4PAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case SNIFF:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BqLWAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case aaa:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case SP:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BGUNAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false; 
              case KC:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BBkNAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;       
              case EW:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BMwMAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;
              case DE:
                  tap_code(KC_ENTER); wait_ms(100);
                  send_string_with_delay_P(PSTR("/say [&BKIMAAA=]"), 5);
                  wait_ms(50); tap_code(KC_ENTER);
                  return false;      
          }
      }
      return true;
  }

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_ortho_3x4(
        LAYER_CYCLE, OPEN_GW2, SNIFF, aaa, NATTER, JABBERS, AA, TEQUATL, LLA, CHAK
    ),
    [1] = LAYOUT_ortho_3x4(
        LAYER_CYCLE, OCTO, OOZE, SEER, DEPTHS, BEARVERGENCE, BEAMVERGENCE, CHOVERGENCE, CHOYASTORM, CHOYAKKAR
    )
};
