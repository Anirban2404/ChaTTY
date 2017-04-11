# Tcp Chat client
import socket
import threading
import sys

SIZE = 1024


class client(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.stopIt = False

    def messagerecv(self):
        data = self.conn.recv(SIZE)
        self.conn.send('OK')
        return self.conn.recv(int(data))

    def run(self):
        while not self.stopIt:
            message = self.messagerecv()
            print 'received-> ', message


host = sys.argv[1]
port = int(sys.argv[2])
server_address = (host, port)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.connect(server_address)
send_socket.send('WILL SEND')  # telling server we will send data from here

rcv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rcv_socket.connect(server_address)
rcv_socket.send('WILL RECV')  # telling server we will recieve data from here


def messagesend(connection, message):
    if len(message) <= SIZE and len(message) > 0:
        connection.send(str(len(message)))
        if connection.recv(2) == 'OK':
            connection.send(message)
        else:
            sys.exit()
    else:
        connection.send(str(SIZE))
        if connection.recv(2) == 'OK':
            connection.send(message[:SIZE])
            messagesend(connection, message[SIZE + 1:])  # calling recursive
        else:
            sys.exit()


thread = client(rcv_socket)
thread.start()

try:
    while True:
        _mymessage = raw_input()
        messagesend(send_socket, _mymessage)
        if _mymessage == "QUIT":
            messagesend(dict['send'], 'bye!!')
            client.conn.send('QUIT')
            sys.exit()
except:
    print 'closing'
finally:
    thread.stopIt = True
    thread.conn.close()
    send_socket.close()
    rcv_socket.close()
