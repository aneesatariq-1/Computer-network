import socket
import threading
import tkinter as tk
from cryptography.fernet import Fernet

HOST = '127.0.0.1'
PORT = 9999

# Generate key
key = Fernet.generate_key()
fernet = Fernet(key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

conn = None

# ================= GUI =================
root = tk.Tk()
root.title("Secure Chat - Server")
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
def accept_client():
    global conn
    log_chat("🟢 Waiting for client...")
    conn, addr = server.accept()
    log_chat(f"✅ Connected with {addr}")

    # Send key
    conn.send(key)
    log_chat("🔑 Encryption key sent")

    while True:
        data = conn.recv(1024)
        if not data:
            break

        # Show encrypted data
        log_encrypted(str(data))

        # Decrypt
        msg = fernet.decrypt(data).decode()
        log_chat("Client: " + msg)

def send_msg():
    if conn:
        msg = msg_entry.get()

        encrypted = fernet.encrypt(msg.encode())

        # Show encrypted form
        log_encrypted(str(encrypted))

        conn.send(encrypted)
        log_chat("You: " + msg)
        msg_entry.delete(0, tk.END)

threading.Thread(target=accept_client, daemon=True).start()

tk.Button(root, text="Send", command=send_msg).pack(pady=5)

root.mainloop()
