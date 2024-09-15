# This file is executed on every boot (including wake-boot from deepsleep)
import webrepl
import network
import client
import neopixel
import networks
import machine
import time

pix = neopixel.NeoPixel(machine.Pin(32, machine.Pin.OUT), 20)

pix[0] = (255, 0, 0, 128)
pix[1] = (0, 255, 0, 128)
pix[2] = (0, 0, 255, 128)

pix.write()

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

print(networks.networks)

while not sta_if.isconnected():

    for i in range(20):
        pix[i] = (0, 10, 0)
    pix.write()

    nts = sta_if.scan()
    for net in nts:
        if net[0] in networks.networks:
            print("Pripojuji se k", net[0])
            sta_if.connect(net[0], networks.networks[net[0]])
            time.sleep(2)
            break

    
    if sta_if.isconnected():
        for i in range(20):
            pix[i] = (0, 0, 0)
        pix.write()
        try:
            print("Spoustim skript...")
            client.rtbolidozor(pix, 0, netm = sta_if)
            print("Skrpit skoncil...")
        except Exception as e:
            print(e)
            print("Chyba pri spousteni skriptu")