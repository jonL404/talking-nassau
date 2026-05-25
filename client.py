import socket
import threading

SERVER_IP = input("Server IP: ")
PORT = 5555

nickname = input("Your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("Disconnected from server.")
            client.close()
            break


def send_messages():
    while True:
        message = input()

        full_message = f"{nickname}: {message}"

        client.send(full_message.encode())


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()