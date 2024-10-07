ampy -p /dev/ttyACM0 put client.py client.py
ampy -p /dev/ttyACM0 put networks.py networks.py
ampy -p /dev/ttyACM0 mkdir uwebsockets || true
ampy -p /dev/ttyACM0 put uwebsockets/protocol.py uwebsockets/protocol.py
ampy -p /dev/ttyACM0 put uwebsockets/client.py uwebsockets/client.py
ampy -p /dev/ttyACM0 put boot.py boot.py
