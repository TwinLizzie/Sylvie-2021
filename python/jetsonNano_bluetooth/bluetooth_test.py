
import bluetooth

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
client_socket,address = server_socket.accept()
print("Accepted connection from ",address)

while True:
    res = self.client_socket.recv(1024)
    client_socket.send(res)
    if res == 'q':
        print ("Quit")
        break
    else:
        print("Received:",res)

client_socket.close()
server_socket.close()
