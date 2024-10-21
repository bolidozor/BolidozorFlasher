# This file is executed on every boot (including wake-boot from deepsleep)
import webrepl
import network
# import client
import neopixel
import networks
import machine
import time
#import uasyncio as asyncio
import uwebsockets.client
import os



def all():
    pix = neopixel.NeoPixel(machine.Pin(0, machine.Pin.OUT), 64)

    pix[0] = (255, 0, 0, 128)
    pix[1] = (0, 255, 0, 128)
    pix[2] = (0, 0, 255, 128)
    pix[3] = (255, 255, 0, 128)

    pix.write()

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    print(networks.networks)

    while not sta_if.isconnected():
        #machine.idle()  

        for i in range(64):
            pix[i] = (0, 10, 0)
        pix.write()
        
        nts = sta_if.scan()
        print(nts)
        for net in nts:
            #await asyncio.sleep(0.2)
            print("Selected", net)
            if net[0] in networks.networks:
                #led.toggle()
                print("Pripojuji se k", net[0])
                sta_if.connect(net[0], networks.networks[net[0]])
                #await asyncio.sleep(2)
                time.sleep(2)

                if sta_if.isconnected():
                    break

    if sta_if.isconnected():
        for i in range(64):
            pix[i] = (0, 0, 0)
        pix.write()

        try:
            print("Spoustim skript...")
            #import client
            a = uwebsockets.client.connect('ws://rtbolidozor.astro.cz/ws/')
            a.settimeout(0.01)
            
            last = time.ticks_ms()
            last = 0
            light = 1
            delay = 1000
            while True:

                data = None
                try:
                    data =  a.recv()
                except Exception as e:
                    #await asyncio.sleep(0.1)
                    pass
                    #print('.')
                
                if data:
                    #led.toggle()
                    #print('>>', data)
                    last = time.ticks_ms()
                    light += 1
                else:
                    pass
                    #await asyncio.sleep(0.1)
                

                pix.write()
                if light > 3:
                    light = 3
                if light > 1:
                    light -= 0.04
                if light > 0:
                    light -= 0.01
                
                real_light = light
                if real_light<0: real_light=0
                if real_light>1: real_light=1
                
                fromLast = time.ticks_ms() - last
                black = int(fromLast / 250) % 64
                for i in range(64):
                    pix[i] = (
                        int(min(255, max(0, 253 * real_light + 2))),
                        int(min(255, max(0, 128 * (light - 1) / 2.0 + 1))) if light > 1 else 0,
                        int(min(255, max(0, 128 * (light - 1) / 2.0 + 1))) if light > 1 else 0
                    )
                pix[black] = (0, 0, 0)
                pix.write()

                # if last and last+delay < time.ticks_ms():
                #     last = 0
                #     #print("DOWN")
            
                if not sta_if.isconnected():
                    #print("Reconnecting...")
                    break


            print("Skrpit skoncil...")
        except Exception as e:
            print(e)
            print("Chyba pri spousteni skriptu")

all()

#asyncio.run(all())