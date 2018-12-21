import uwebsockets.client
import os
import time
import machine

print("")




def rtbolidozor(delay = 200):
    print("Zacatek...")
    led = machine.Pin(19, machine.Pin.OUT)
    beep = machine.Pin(18)
    beep_pwm = machine.PWM(beep)
    beep_pwm.freq(500)
    beep_pwm.duty(0)

    #delay = 5000;
    #with uwebsockets.client.connect('ws://rtbolidozor.astro.cz:80/ws') as websocket:


    #    while 1:
    #        msg = websocket.recv()
    #        print(msg)
    
    a = uwebsockets.client.connect('ws://rtbolidozor.astro.cz:80/ws')
    print(a.recv())
    print("prvni prijem dat")
    a.settimeout(0.05)


    last = 0
    while True:
        data = None
        try:
           data =  a.recv()
        except Exception as e:
            pass
            #print('.')
        
        if data:
            print('>>', data)
            #if 'SVAKOV-R12' in data:
            #print("UP")
            last = time.ticks_ms()
            led.value(1)
            beep_pwm.duty(int((2**10)*0.5))
            #print(last)
        
        else:
            pass

        #sprint(time.ticks_ms(), last+delay)
        if last and last+delay < time.ticks_ms():
            print(time.ticks_ms(), last+delay)
            led.value(0)
            beep_pwm.duty(0)
            last = None
            #print("DOWN")

