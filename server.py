# Tcp Chat server
import socket
import threading
import sys
SIZE = 1024

host = sys.argv[1]
port = int(sys.argv[2])
server_address = (host, port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)


class server(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.stopIt = False

    def messagerecv(self):
        data = self.conn.recv(SIZE)
        self.conn.send('OK')
        message = self.conn.recv(int(data))
        return message

    def run(self):
        while not self.stopIt:
            message = self.messagerecv()
            print 'received->  ', message


def setConn(conn1, conn2):
    dict = {}
    state = conn1.recv(9)
    conn2.recv(9)
    if state == 'WILL RECV':
        dict['send'] = conn1  # server will send data to reciever
        dict['recv'] = conn2
    else:
        dict['recv'] = conn1  # server will recieve data from sender
        dict['send'] = conn2
    return dict


def messagesend(conn, message):
    if len(message) <= SIZE and len(message) > 0:
        conn.send(str(len(message)))
        if conn.recv(2) == 'OK':
            conn.send(message)
        else:
            sys.exit()
    else:
        conn.send(str(SIZE))
        if conn.recv(2) == 'OK':
            conn.send(message[:SIZE])
            messagesend(conn, message[SIZE + 1:])  # calling recursive
        else:
            sys.exit()


(c1, a1) = server_socket.accept()
(c2, a2) = server_socket.accept()
dict = setConn(c1, c2)
thread = server(dict['recv'])
thread.start()
try:
    while True:
        _mymessage = raw_input()
        messagesend(dict['send'], _mymessage)
        if _mymessage == "QUIT":
            messagesend(dict['send'], 'bye!!')
            server.conn.send('QUIT')
            sys.exit()
except:
    print 'closing'
finally:
    thread.stopIt = True
    thread.conn.close()
    server_socket.close()
