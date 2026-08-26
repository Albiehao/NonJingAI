# Codex Quota Display - ESP8266

ESP8266 + SSD1306 128x64 OLED client for displaying Codex quota status from a trusted local gateway.

## Hardware

- ESP8266 / NodeMCU
- SSD1306 128x64 I2C OLED (0x3C)

Default NodeMCU wiring:

| OLED | ESP8266 |
|---|---|
| VCC | 3.3V |
| GND | GND |
| SDA | D2 / GPIO4 |
| SCL | D1 / GPIO5 |

## Arduino libraries

Install:

- Adafruit GFX Library
- Adafruit SSD1306
- ArduinoJson 7.x

ESP8266WiFi and ESP8266HTTPClient are provided by the ESP8266 Arduino core.

## Gateway contract

The ESP8266 intentionally does **not** store any ChatGPT/OpenAI credential. It polls your own trusted HTTP gateway:

`GET /codex/status`

Optional request header:

`X-Device-Token: CHANGE_ME`

Expected JSON:

```json
{
  "codex_available": true,
  "five_hour_remaining": 75,
  "weekly_remaining": 82,
  "five_hour_reset_seconds": 3214
}
```

Fields:

- `codex_available`: whether the gateway considers Codex ready for use.
- `five_hour_remaining`: remaining percentage in the primary 5-hour window, 0-100.
- `weekly_remaining`: remaining percentage in the secondary weekly window, 0-100.
- `five_hour_reset_seconds`: seconds until the primary window resets.

## Configuration

Edit these values at the top of `codex_quota_display.ino`:

```cpp
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* STATUS_URL = "http://192.168.1.100:8080/codex/status";
const char* DEVICE_TOKEN = "CHANGE_ME";
```

The device refreshes from the gateway once per minute and maintains the reset countdown locally once per second.

## Display

The OLED shows:

- 5-hour remaining percentage and progress bar
- weekly remaining percentage and progress bar
- READY / LIMITED state
- countdown to the 5-hour reset

## Security

Do not put ChatGPT session credentials, Codex credentials, or OpenAI tokens directly on the ESP8266. Keep those credentials on the machine running Codex/app-server and expose only the minimal quota JSON to the device.
