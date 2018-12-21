# This file is executed on every boot (including wake-boot from deepsleep)
import webrepl
import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
networks = {
    b'rdnet_gateway': '2627f68597',
    b'hvezdarna-svakov': 'Aezoyiosh4eh9Uit',
    b'Radiobouda': '55aa55aa55'
}
for net in sta_if.scan():
    if net[0] in networks:
	sta_if.connect(net[0], networks[net[0]])
	print("Pripojuji se k", net[0])
	break
#sta_if.connect('rdnet_gateway', '2627f68597')
#sta_if.connect('hvezdarna-svakov', 'Aezoyiosh4eh9Uit')
while not sta_if.isconnected():
    pass
webrepl.start()

print("Spoustim skript...")
import client
client.rtbolidozor(200)
