# tm1637raw — External ESPHome component (raw 7-seg control)
Use-cases: Most of tm1637 modules have only 4 digits, while TM1637 driver can handle up to 6 digits. This component give user ability to control raw segments for other purposes as indicator LEDs.

- Implements a TM1637-style 7-segment display driver as an external (local) component.
- Adds a public method you can call from lambdas: `it.raw(uint8_t segments, uint8_t pos)` which writes a raw 8-bit segment pattern to the specified digit position.
## How to install

### Local

1. In your ESPHome configuration directory (the same directory that contains your YAML files) create the folder `custom_components/` (you can use your external_components folder if you already have one).

2. Copy the folder `components/tm1637raw` of this repository into that directory so the files are directly under:

```
<your-esphome-config>/custom_components/tm1637raw/
  ├─ tm1637raw.h
  ├─ tm1637raw.cpp
  ├─ display.py
  └─ binary_sensor.py
```

ESPHome will detect and compile the C++ code and load the Python bindings when you build a firmware for a device in that config directory.

### Git / external

Use `external_components` to fetch it from this Git repository directly. See the ESPHome docs for the exact `external_components` syntax for your version of ESPHome.

```yaml
external_components:
  - source:
        type: git
        url: git://github.com/susembeded/raw-tm1637-esphome
    components: [tm1637raw]
```
## How to use (example YAML)

Example that shows the most common usage including the `it.raw()` call inside the `lambda`:

```yaml
display:
  - platform: tm1637raw
    clk_pin: GPIO5
    dio_pin: GPIO4
    num_digits: 6
    id: my_tm
    update_interval: 1s // If set to 0 the display will be updated every loop.
    lambda: |-
      // Set a single segment (example: bit 1 = segment B)
      it.raw(0b00000010, 1);

      static int grid5 = 255; // still int, but convert when sending
      if (grid5 >= 0 && grid5 <= 0xFF) {                       // range-check A..X
        it.raw(static_cast<uint8_t>(grid5), 4);
      }

      // Set the decimal point at position 0
      it.raw(0x80, 0);  // 0x80 is the DP bit

      // Mix raw writes and normal text printing
      it.print("12:34");
```
Other display options (brightness, etc) are supported as per the built-in `tm1637` component. See [TM1637 ESPHome docs](https://esphome.io/components/display/tm1637/).

Notes:
- You must not write to positions outside the configured `num_digits` otherwise the device will complain: `[E][display.tm1637raw:430]: raw(): position 4 out of bounds (length 4)`. Just set `num_digits: 6` in most cases.
- Positions are 0-indexed: position `0` is the left-most digit and `it.print()` fills from left to right.
- You can mix `it.raw(...)` calls with `it.print(...)` calls in the same `lambda`. The order of calls matters. `it.print(...)` should be called before `it.raw(...)` to prevent unexpected of LEDs being lit.

## Segments and Grids

The TM1637 driver supports up to 6 digits (grids) and each digit has 8 segments (A-G + DP). To drive LEDs or other indicators, you can use any combination of the 8 bits. You must refer to the TM1637 pinout.
<img width="390" height="365" alt="image" src="https://github.com/user-attachments/assets/a6563baf-ec3f-474f-a63e-f8a85bc4b8f4" />

If LED 1 is connected between SEG1 and GRID5, LED 2 between SEG2 and GRID5, etc, then to light up LED 1 and LED 2 you would set bits 0 and 1 of the segments byte for position 5 (GRID5): 

```cpp
it.raw(0b00000011, 4);
```
## Compatibility

- Tested with ESPHome 2025.12.6