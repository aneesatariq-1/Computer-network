# ============================================================
# SECURE CHAT APPLICATION (2 USERS) – FULL GUI VERSION
# Information Security Mini Project
# Features:
# ✔ Server & Client BOTH have GUI
# ✔ Automatic key exchange (NO manual copy-paste)
# ✔ Encrypted messages (Fernet)
# ✔ Very easy to run & explain
# ============================================================

# ======================= SERVER (GUI) =======================
# Save as: server_gui.py

import socket
import threading
import tkinter as tk
from cryptography.fernet import Fernet

HOST = '127.0.0.1'
PORT = 9999

key = Fernet.generate_key()
fernet = Fernet(key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

conn = None

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Secure Chat Server")
root.geometry("400x500")

chat = tk.Text(root, state='disabled')
chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

msg_entry = tk.Entry(root)
msg_entry.pack(fill=tk.X, padx=10, pady=5)


def log(msg):
    chat.config(state='normal')
    chat.insert(tk.END, msg + "\n")
    chat.config(state='disabled')
    chat.see(tk.END)


def accept_client():
    global conn
    log("🟢 Waiting for client...")
    conn, addr = server.accept()
    log(f"✅ Connected: {addr}")

    # Send encryption key automatically
    conn.send(key)
    log("🔑 Encryption key sent securely")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = fernet.decrypt(data).decode()
        log("Client: " + msg)


def send_msg():
    if conn:
        msg = msg_entry.get()
        encrypted = fernet.encrypt(msg.encode())
        conn.send(encrypted)
        log("You: " + msg)
        msg_entry.delete(0, tk.END)


threading.Thread(target=accept_client, daemon=True).start()

send_btn = tk.Button(root, text="Send", command=send_msg)
send_btn.pack(pady=5)

root.mainloop()


# ======================= CLIENT (GUI) =======================
# Save as: client_gui.py

import socket
import threading
import tkinter as tk
from cryptography.fernet import Fernet

HOST = '127.0.0.1'
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive key automatically
key = client.recv(1024)
fernet = Fernet(key)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Secure Chat Client")
root.geometry("400x500")

chat = tk.Text(root, state='disabled')
chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

msg_entry = tk.Entry(root)
msg_entry.pack(fill=tk.X, padx=10, pady=5)


def log(msg):
    chat.config(state='normal')
    chat.insert(tk.END, msg + "\n")
    chat.config(state='disabled')
    chat.see(tk.END)


def receive_msg():
    while True:
        data = client.recv(1024)
        if not data:
            break
        msg = fernet.decrypt(data).decode()
        log("Server: " + msg)


def send_msg():
    msg = msg_entry.get()
    encrypted = fernet.encrypt(msg.encode())
    client.send(encrypted)
    log("You: " + msg)
    msg_entry.delete(0, tk.END)


threading.Thread(target=receive_msg, daemon=True).start()

send_btn = tk.Button(root, text="Send", command=send_msg)
send_btn.pack(pady=5)

root.mainloop()
