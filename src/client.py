#from uwebsockets import client
import uwebsockets.client
import os
import time
import machine
import neopixel

def rtbolidozor(pix, delay = 200, netm = None):
    print("Zacatek...")

    delay = 1000
    #led = machine.Pin(33, machine.Pin.OUT)
    #led = machine.PWM(machine.Pin(25, machine.Pin.OUT), freq=1000)
    led = machine.Pin(25, machine.Pin.OUT)
    led.toggle()
    #led.freq(500)
    #led.duty(0)

    time.sleep(1)

    last = time.ticks_ms()


    #beep = machine.Pin(18)
    #beep_pwm = machine.PWM(beep)
    #beep_pwm.freq(500)
    #beep_pwm.duty(0)

    #delay = 5000;
    #with uwebsockets.client.connect('ws://rtbolidozor.astro.cz:80/ws') as websocket:


    #    while 1:
    #        msg = websocket.recv()
    #        print(msg)
    
    a = uwebsockets.client.connect('ws://rtbolidozor.astro.cz/ws/')
    a.settimeout(0.01)
    print(a)
    #print(a.recv())
    print("prvni prijem dat")



    last = 0
    light = 1
    while True:
        data = None
        try:
           data =  a.recv()
        except Exception as e:
            pass
            #print('.')
        
        if data:
            led.toggle()
            print('>>', data)
            last = time.ticks_ms()
            light += 1
            #led.value(1)
            #beep_pwm.duty(int((2**10)*0.5))
            #print(last)
        
        if light > 3:
            light = 3
        if light > 1:
            light -= 0.04
        if light > 0:
            light -= 0.01
        
        real_light = light
        if real_light<0: real_light=0
        if real_light>1: real_light=1
        print(real_light, light)

        #led.duty(int(1023*real_light))
        for i in range(64):
            pix[i] = (int(253*real_light)+2, int(128*light/3.0+1), int(128*light/3.0+1))
        pix.write()

        if last and last+delay < time.ticks_ms():
            last = None
            print("DOWN")
    
        if not netm.isconnected():
            print("Reconnecting...")
            break

