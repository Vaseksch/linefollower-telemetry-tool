BAUD_RATE = 115200

ESP_KNOWN_VIDS_PIDS = {
    (0x10C4, 0xEA60),  # Silicon Labs CP2102 / CP2104 (very common on ESP boards)
    (0x1A86, 0x7523),  # CH340 / CH341 (common on NodeMCU, Wemos D1)
    (0x0403, 0x6001),  # FTDI FT232R
    (0x0403, 0x6010),  # FTDI FT2232
    (0x0403, 0x6011),  # FTDI FT4232
    (0x0403, 0x6014),  # FTDI FT232H
    (0x2341, 0x0043),  # Arduino Uno (sometimes used with ESP)
    (0x239A, None),    # Adafruit (ESP Feather boards)
    (0x303A, 0x1001),  # Espressif USB JTAG/serial (ESP32-S3, ESP32-C3 native USB)
    (0x303A, 0x0002),  # Espressif native USB
}

FEATURES = [
    "time",
    "error",
    "correction",
    "derivative",
    "mot_a_speed",
    "mot_b_speed",
    "flag"
]