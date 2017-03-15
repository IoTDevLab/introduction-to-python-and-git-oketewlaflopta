#PS/ITC/14/0058
# PRINCE DARKWAH
import sys
from socket import *
import select 

class server():
    def __init__(self, Host, SOCKET_LIST, RECV_BUFFER, PORT):
        self.HOST = Host 
        self.SOCKET_LIST = SOCKET_LIST
        self.RECV_BUFFER = RECV_BUFFER
        self.PORT = PORT

    def Server(self):

        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((self.HOST, self.PORT))
        server_socket.listen(10)
        #print(server_socket)
        # add server socket object to the list of readable connections
        self.SOCKET_LIST.append(server_socket)
     
        print ("Chat server started on port " + str(self.PORT))
     
        while True:

            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read,ready_to_write,in_error = select.select(self.SOCKET_LIST,[],[],0)
          
            for sock in ready_to_read:
                # a new connection request recieved
                
                
                if sock == server_socket: 
                    sockfd, addr = server_socket.accept()
                    self.SOCKET_LIST.append(sockfd)
                    #print(sockfd)
                    print ("Client (%s, %s) connected" % addr)
                     
                    self.run(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
                 
                # a message from a client, not a new connection
                else:
                    #print(sock.getpeername())
                    # process data recieved from client, 
                    try:
                        # receiving data from the socket.
                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            # there is something in the socket
                            self.run(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                        else:
                            # remove the socket that's broken    
                            if sock in self.SOCKET_LIST:
                                self.SOCKET_LIST.remove(sock)

                            # at this stage, no data means probably the connection has been broken
                            self.run(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                    # exception 
                    except:
                        self.run(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                        continue

        server_socket.close()
        

    # broadcast chat messages to all connected clients
    def run (self, server_socket, sock, message):
        for socket in self.SOCKET_LIST:
            # send the message only to peer
            if socket != server_socket and socket != sock :
                try :
                    socket.send(message)
                except :
                    # broken socket connection
                    socket.close()
                    # broken socket, remove it
                    if socket in self.SOCKET_LIST:
                        self.SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":
    s = server("192.168.109.1 ", [], 4096, 9009)
    sys.exit(s.Server())
    #sys.exit()

