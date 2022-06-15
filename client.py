import socket
import threading
import re
import sys

class ChatClient:

    def __init__ (self, host="127.0.0.1", port=55555):
        self.client_name = input("Qual seu nome?\n")
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        

    def run (self):
        wrt_thread = threading.Thread(target=self.wrt_to_server)
        wrt_thread.start()

        rcv_thread = threading.Thread(target=self.rcv_from_server)
        rcv_thread.start()

    
    def wrt_to_server(self):
        while True:
            pre_msg = input("")

            user = re.search("<(\w+)>", pre_msg)
            user = "" if user is None else user.group(0)

            msg = f"{user}{self.client_name}: {pre_msg.replace(user, '')}"
            self.client.send(msg.encode("utf8"))

    def rcv_from_server(self):
        while True:
            try:
                msg = self.client.recv(1024).decode("utf8")
                if msg == "NAME":
                    self.client.send(self.client_name.encode("utf8"))
                else:
                    print(msg)
            except:
                print("Vish...")
                print("Você foi desconectado!")
                self.client.close()
                break
        
        sys.exit()


if __name__ == "__main__":
    client = ChatClient()
    client.run()
