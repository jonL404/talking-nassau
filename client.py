# client.py

import socket
import threading
import customtkinter as ctk


class ChatApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Local Chat")
        self.geometry("700x500")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.client = None

        self.create_widgets()

    def create_widgets(self):

        # Top frame
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=10)

        self.ip_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text="Server IP"
        )
        self.ip_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.name_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text="Your Name"
        )
        self.name_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.connect_button = ctk.CTkButton(
            self.top_frame,
            text="Connect",
            command=self.connect_to_server
        )
        self.connect_button.pack(side="left", padx=5)

        # Chat box
        self.chat_box = ctk.CTkTextbox(self, state="disabled")
        self.chat_box.pack(expand=True, fill="both", padx=10, pady=10)

        # Bottom frame
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(fill="x", padx=10, pady=10)

        self.message_entry = ctk.CTkEntry(
            self.bottom_frame,
            placeholder_text="Type your message..."
        )
        self.message_entry.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5,
            pady=5
        )

        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(
            self.bottom_frame,
            text="Send",
            command=self.send_message
        )
        self.send_button.pack(side="left", padx=5)

    def connect_to_server(self):

        server_ip = self.ip_entry.get()
        self.nickname = self.name_entry.get()

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((server_ip, 5555))

            self.add_message("Connected to server.\n")

            receive_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )
            receive_thread.start()

        except Exception as error:
            self.add_message(f"Connection error: {error}\n")

    def receive_messages(self):

        while True:
            try:
                message = self.client.recv(1024).decode()

                if message:
                    self.add_message(message + "\n")

            except:
                self.add_message("Disconnected from server.\n")
                break

    def send_message(self, event=None):

        message = self.message_entry.get()

        if message.strip() == "":
            return

        full_message = f"{self.nickname}: {message}"

        try:
            self.client.send(full_message.encode())

            self.add_message(full_message + "\n")

            self.message_entry.delete(0, "end")

        except Exception as error:
            self.add_message(f"Send error: {error}\n")

    def add_message(self, message):

        self.chat_box.configure(state="normal")

        self.chat_box.insert("end", message)

        self.chat_box.see("end")

        self.chat_box.configure(state="disabled")


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()