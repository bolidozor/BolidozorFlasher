# This file is executed on every boot (including wake-boot from deepsleep)
import webrepl
import network
import client
import neopixel
import networks
import machine
import time

from machine import Pin
led = Pin(25, Pin.OUT)
led.toggle()
pix = neopixel.NeoPixel(machine.Pin(0, machine.Pin.OUT), 64)

pix[0] = (255, 0, 0, 128)
pix[1] = (0, 255, 0, 128)
pix[2] = (0, 0, 255, 128)

pix.write()

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

print(networks.networks)

while not sta_if.isconnected():

    for i in range(64):
        pix[i] = (0, 10, 0)
    pix.write()
    
    nts = sta_if.scan()
    print(nts)
    for net in nts:
        print("Selected", net)
        if net[0] in networks.networks:
            #led.toggle()
            print("Pripojuji se k", net[0])
            sta_if.connect(net[0], networks.networks[net[0]])
            time.sleep(2)
            #led.toggle()
            #break

    if sta_if.isconnected():
        for i in range(64):
            pix[i] = (0, 0, 0)
        pix.write()
        try:
            print("Spoustim skript...")
            #import client
            client.rtbolidozor(pix, 0, netm = sta_if)
            print("Skrpit skoncil...")
        except Exception as e:
            print(e)
            print("Chyba pri spousteni skriptu")
