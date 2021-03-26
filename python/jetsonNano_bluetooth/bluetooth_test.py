
import bluetooth

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
client_socket,address = server_socket.accept()
print("Accepted connection from ",address)

while True:
    res = client_socket.recv(1024)
    client_socket.send(res)
    if res == 'q':
        print ("Quit")
        break
    else:
        print("Received:",res)

client_socket.close()
server_socket.close()

# Commands used:
# 1. sudo sdptool add SP
# 2. rfcomm watch hci0
# 3. minicom -b 9600 -o -D /dev/rfcomm0
# 4. sudo nano /etc/systemd/system/dbus-org.bluez.service
#	Then add lines:
#	ExecStart=/usr/lib/bluetooth/bluetoothd -C
#	ExecStartPost=/usr/bin/sdptool add SP
# 5. sudo systemctl daemon-reload	
# 6. sudo systemctl restart bluetooth.service
# https://scribles.net/setting-up-bluetooth-serial-port-profile-on-raspberry-pi/

