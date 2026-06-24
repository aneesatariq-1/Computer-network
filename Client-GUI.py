import socket
import threading
import tkinter as tk
from cryptography.fernet import Fernet

HOST = '127.0.0.1'
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive key
key = client.recv(1024)
fernet = Fernet(key)

# ================= GUI =================
root = tk.Tk()
root.title("Secure Chat - Client")
root.geometry("500x600")

tk.Label(root, text="🔐 Encrypted Data").pack()
encrypted_box = tk.Text(root, height=8, state='disabled', bg="#f0f0f0")
encrypted_box.pack(fill=tk.X, padx=10)

tk.Label(root, text="💬 Decrypted Chat").pack()
chat_box = tk.Text(root, height=12, state='disabled')
chat_box.pack(fill=tk.BOTH, expand=True, padx=10)

msg_entry = tk.Entry(root)
msg_entry.pack(fill=tk.X, padx=10, pady=5)

# ---------- helper logs ----------
def log_chat(msg):
    chat_box.config(state='normal')
    chat_box.insert(tk.END, msg + "\n")
    chat_box.config(state='disabled')
    chat_box.see(tk.END)

def log_encrypted(msg):
    encrypted_box.config(state='normal')
    encrypted_box.insert(tk.END, msg + "\n")
    encrypted_box.config(state='disabled')
    encrypted_box.see(tk.END)

# ---------- networking ----------
def receive_msg():
    while True:
        data = client.recv(1024)
        if not data:
            break

        # Show encrypted
        log_encrypted(str(data))

        # Decrypt
        msg = fernet.decrypt(data).decode()
        log_chat("Server: " + msg)

def send_msg():
    msg = msg_entry.get()

    encrypted = fernet.encrypt(msg.encode())

    # Show encrypted
    log_encrypted(str(encrypted))

    client.send(encrypted)
    log_chat("You: " + msg)
    msg_entry.delete(0, tk.END)

threading.Thread(target=receive_msg, daemon=True).start()

tk.Button(root, text="Send", command=send_msg).pack(pady=5)

root.mainloop()
