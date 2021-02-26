from socket import *
import socket as sk
import threading

class client_handler :
    def __init__(self, clientSock, addr):	
        self.sock = clientSock
        self.addr = addr

        self.client_msg = ""
        self.server_msg = ""

        self.reicver = threading.Thread(target=self.recv_msg, args=())
        self.reicver.start()
        self.sender = threading.Thread(target=self.send_msg, args=())
        self.sender.start()

    def recv_msg(self):
        while True :
            self.client_msg = self.sock.recv(1024)
            if self.client_msg != "":
                self.client_msg = self.client_msg.decode('utf-8')

    def send_msg(self):
        while True :
            if self.server_msg != "" :
                self.sock.send(self.server_msg.encode('utf-8'))
                self.server_msg = ""

    def get_client_msg(self):
        if self.client_msg != "":
            ret_msg = self.client_msg
            self.client_msg = ""
            return ret_msg
        else :
            return ""

    def set_server_msg(self, msg):
        self.server_msg = msg
    # end of function
# end of class

class socket_server:
    # 클래스 생성자, 사용할 변수들을 적어주세요
    def __init__(self):
        self.server_ip = "192.168.1.159"
        self.server_port = 7001
        self.readyServer = False
        self.serverSock = None
        self.ch = None

        self.server_init()
        self.waiting_start()

    def server_init(self):  # 서버를 열어주는 스레드
        print("initiating server...")
        self.serverSock = socket(AF_INET, SOCK_STREAM)  # IPV4 형식의 IP 형식이며, SOCK_STREAM 형식을 채택
        self.serverSock.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self.serverSock.bind((self.server_ip, self.server_port))  # 서버 소켓으로 사용할 IP와 포트 번호를 지정합니다.
        self.serverSock.listen(5)  # 최대 다섯 개의 클라이언트가 접속할 수 있습니다.
        self.readyServer = True
        print("done : init server")

    def waiting_start(self):
        th = threading.Thread(target=self.client_wait, args=())
        th.start()

    def client_wait(self):
        print("waiting client...")

        while True:
            if self.readyServer :
                connectionSock, addr = self.serverSock.accept()
                self.ch = client_handler(connectionSock, addr)
                print("accepted")

        # end of while
    # end of function
# end of class



if __name__ == "__main__":
    ss = socket_server()



