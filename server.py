import socket
import threading
import re

class ChatServer (threading.Thread):

    def __init__(self, chat_name, host="0.0.0.0", port=55555):
        print(f"Iniciando Server {chat_name}")

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

        self.chat_name = chat_name
        self.clients = []
        self.names = []
    
    def run(self):
        print(f"Chat {self.chat_name} na escuta...")

        while True:
            client, address = self.server.accept()
            print(f"Novo cliente em {str(address)}.")

            client.send("NAME".encode("utf8"))
            name = client.recv(1024).decode("utf8")
            self.names.append(name)
            self.clients.append(client)

            print(f"Cliente se chama {name}.")
            self.send_chat_to_clients(client, f"{name} entrou no chat!".encode("utf8"))
            client.send(f"Você conectou ao chat {self.chat_name}!".encode("utf8"))

            clt_thread = threading.Thread(target=self.handler, args=(client,))
            clt_thread.start()


    def handler(self, client):
        while True:
            try:
                msg = client.recv(1024)

                user = re.search("<(\w+)>", msg.decode("utf8"))
                if user is not None:
                    msg = msg.decode("utf8")
                    msg = msg.replace(user.group(0), "")
                    msg = msg.replace("  ", " ")
                    msg = msg.replace(":", "(privado):")
                    msg = msg.encode("utf8")

                    self.send_chat_to_client(msg, user.group(0))
                    continue

                self.send_chat_to_clients(client, msg)
            except Exception as e:
                print(e)
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                name = self.names[index]
                self.send_chat_to_clients(client, f"{name} saiu do chat!".encode("utf8"))
                self.names.remove(name)
                break


    def send_chat_to_client(self, msg, user):
        user = user.replace("<", "").replace(">", "")

        for i, name in enumerate(self.names):
            if name == user:
                self.clients[i].send(msg)
                break


    def send_chat_to_clients(self, clt, msg):
        for client in self.clients:
            if client != clt:
                client.send(msg)


if __name__ == "__main__":
    chat = ChatServer(input("Qual o nome do server?\n"))
    chat.run()
