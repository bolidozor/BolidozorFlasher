# Bolidozor Flasher

This project is a simple visual indicator shaped like the Bolidozor network logo. The blinker activates whenever a bolide is detected by one of the stations within the Bolidozor network.

![obrazek](https://github.com/user-attachments/assets/56ce7f6a-ac22-4e70-a62d-664da8a0c2ee)

---

## Overview

The blinker provides a real-time visual cue for bolide detections, lighting up in sync with the network's events. It is designed for demonstrations and interactive exhibitions.

## How It Works

The blinker utilizes the **rtbolidozor** service, which distributes bolide detections in real-time over the internet. Stations across the Bolidozor network detect bolides and send a message when a bolide event is recorded. This message is transmitted to the blinker, which visualizes the event by lighting up.

There may be slight delays in data delivery. Experimentally, the typical delay has been observed to be around 0.5 seconds.

---

## Configuration

The device supports up to 10 Wi-Fi networks, which can be configured over a serial connection. Configuration is saved persistently.

### 📡 Connecting to Wi-Fi

1. Connect the device to your computer via USB.
2. Open a serial terminal
3. Type the following command to enter configuration mode:
   ```
   conf
   ```
4. Set the SSID, password, and enable the network (replace with your own values):
   ```
   W0S=YourSSID
   W0P=YourPassword
   W0E=1
   ```
5. Save the configuration:
   ```
   save
   ```
6. View current settings (optional):
   ```
   show
   ```
7. Exit configuration mode:
   ```
   exit
   ```

> You can configure multiple networks (W0–W9). The device will attempt to connect to any enabled network.

---

## Serial Commands

| Command              | Description                                      |
|----------------------|--------------------------------------------------|
| `conf`               | Enter configuration menu                         |
| `met`                | Simulate a meteor event (manually flash)         |
| `W<X>S=SSID`         | Set SSID for network `X` (0–9)                   |
| `W<X>P=PASSWORD`     | Set password for network `X`                     |
| `W<X>E=0/1`          | Enable (`1`) or disable (`0`) network `X`        |
| `save`               | Save configuration to internal storage           |
| `show`               | Print currently configured networks              |
| `reboot`             | Reboot the device (currently disabled)           |
| `exit`               | Exit configuration mode                          |
| `help`               | Display help inside configuration mode           |

---

## Data Source

WebSocket connection is made to:

```
ws://rtbolidozor.astro.cz/ws/
```

Each message received indicates a detected bolide and triggers a visual response.
