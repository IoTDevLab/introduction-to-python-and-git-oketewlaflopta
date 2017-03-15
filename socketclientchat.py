# PS/ITC/14/0058
#  PRINCE DARKWAH
import sys
from select import *
from socket import *

class client:

    
    def __init__(self, host, port, username):
        self.username = username
        self.host = host
        self.port = port
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        #self.client_socket.settimeout(5)

        try:
            self.client_socket.connect((self.host,self.port))
            #self._prompt()
        except:
            print("unable to connect to {} on port {}".format(self.host, self.port))
            sys.exit()

        print("Connected, you can start sending")
        self.client_socket.send(self.username.encode('utf-8'))
        self._prompt()

    def run(self):
        #print(self.client_socket)
        while True:
            connectors = [sys.stdin, self.client_socket]
            ready_to_read = connectors
            #ready_to_read, ready_to_write, in_error = select(connectors , [], [])

            for sock in ready_to_read:
                if sock == self.client_socket:
                    # handle incoming message send(), recv()
                    data = sock.recv(2048)
                    if not data:
                        print("\nDisconnected from chat server")
                        sys.exit()
                    else:
                        sys.stdout.write(data.decode('utf-8'))
                        sys.stdout.flush()
                        self._prompt()
                                    
                else:
                    # send message                        
                    message = sys.stdin.readline()
                    self.client_socket.send(message.encode('utf-8'))
                    self._prompt()

                    
    def _prompt(self):
        sys.stdout.write("\r=[{}]: ".format(self.username))
        sys.stdout.flush()


if __name__=='__main__':
    
    user = input("please enter your name: ")
    c = client("192.168.109.1",9009, str(user))
    #c._prompt()
    c.run()
        
                                                                                
