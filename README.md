# Bolidozor Flasher

This project is a simple visual indicator shaped like the Bolidozor network logo. The blinker activates whenever a bolide is detected by one of the stations within the Bolidozor network.

## Overview

The blinker provides a real-time visual cue for bolide detections, lighting up in sync with the network's events. It is designed for demonstrations and interactive exhibitions.

## How It Works

The blinker utilizes the **rtbolidozor** service, which distributes bolide detections in real-time over the internet. Stations across the Bolidozor network detect bolides and send a message when a bolide event is recorded. This message is transmitted to the blinker, which visualizes the event by lighting up.

There may be slight delays in data delivery. Experimentally, the typical delay has been observed to be around 0.5 seconds.
