from Crypto import Random
from Crypto.Cipher import AES
import os
from tkinter import Tk, Label, Button, Entry, filedialog
import time
import tkinter as tk
  
class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py' and fname != 'data.txt.enc'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)

class EncryptorGUI:
    def __init__(self, master, enc_instance):
        self.master = master
        self.enc = enc_instance
        master.title("File Encryptor GUI")
        
        self.heading_label = Label(master, text="AES Encryptor-Decryptor",font=("Helvetica", 30, "bold"), fg="blue")
        self.heading_label.pack(pady=10)

        self.password_label = Label(master, text="Enter password:" ,font=("Helvetica", 20, "bold"), fg="Black" )
        self.password_label.pack()

        self.password_entry = Entry(master, show="*")
        self.password_entry.pack(pady=10)

        self.confirm_button = Button(master, text="Confirm", command=self.confirm_password)
        self.confirm_button.pack()

        self.status_label = Label(master, text="")
        self.status_label.pack(pady=10)

        self.encrypt_button = Button(master, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = Button(master, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)

        self.encrypt_all_button = Button(master, text="Encrypt All Files", command=self.encrypt_all_files)
        self.encrypt_all_button.pack(pady=10)

        self.decrypt_all_button = Button(master, text="Decrypt All Files", command=self.decrypt_all_files)
        self.decrypt_all_button.pack(pady=10)

    def confirm_password(self):
        password = self.password_entry.get()
        if password:
            # Call your decryption function here to check if the password is correct
            # Update the status_label accordingly
            self.status_label["text"] = "Password confirmed."
        else:
            self.status_label["text"] = "Please enter a password."

    def encrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to encrypt")
        if file_path:
            # Call your encrypt_file function with the selected file_path
            self.enc.encrypt_file(file_path)
            self.status_label["text"] = f"{file_path} encrypted successfully."

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to decrypt")
        if file_path:
            # Call your decrypt_file function with the selected file_path
            self.enc.decrypt_file(file_path)
            self.status_label["text"] = f"{file_path} decrypted successfully."

    def encrypt_all_files(self):
        # Call your encrypt_all_files function
        self.enc.encrypt_all_files()
        self.status_label["text"] = "All files encrypted successfully."

    def decrypt_all_files(self):
        # Call your decrypt_all_files function
        self.enc.decrypt_all_files()
        self.status_label["text"] = "All files decrypted successfully."




def main():
        key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
        enc = Encryptor(key)

        root = Tk()
        gui = EncryptorGUI(root, enc)
        
        root.configure(bg="silver")
        root.geometry("500x400")
        root.mainloop()
        root.configure(fg="silver")



    

if __name__ == "__main__":
    main()
