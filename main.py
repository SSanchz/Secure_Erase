import os
import math
import string
import tkinter

import unicodedata
from tkinter import filedialog as fd
from multiprocessing import Process
from tkinter import *
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import random
from tkinter import ttk

root = Tk()
root.geometry("360x150")
root.title("Data Manager")
root.config(background="white")


file = StringVar() #Input file


def generate_key():
    return Fernet.generate_key() # Generates encryption key (Might be useless)


def encrypt_file(file_path, key): #Encrypts File using Fernet Library
    with open(file_path, 'rb') as f:
        data = f.read()

    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)

    with open(file_path, 'wb') as f:
        f.write(encrypted_data)




def deleteb():
    input_file = file.get()
    key = generate_key()

    if not input_file:
        messagebox.showerror("Error", "No file selected!")
        return

    output_directory = os.path.dirname(os.path.realpath(input_file))

    encrypt_file(input_file, key)  # Encrypts File Before rewrite

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(input_file, 'rb+') as file_obj:
        file_size = os.path.getsize(input_file)
        
        # Generate random data by choosing characters from all Unicode symbols
        unii = [chr(i) for i in range(0x110) if unicodedata.category(chr(i)) != 'Cn']
        char_set = string.ascii_letters + string.digits
        K_size = int(math.floor(file_size / 2))

        random_data = ''.join(random.choices(char_set, k=K_size))
        # Injects random data into file
        file_obj.write(random_data.encode('utf-16', errors='surrogatepass'))

        random_data = ''.join(random.choices(unii, k=K_size))
        # Injects random data into file
        file_obj.write(random_data.encode('utf-16', errors='surrogatepass')) #Encrypts Twice, once using ascii, then unichr
        
        # Flush and sync the changes to disk
        file_obj.flush()
        os.fsync(file_obj.fileno())

        encrypt_file(input_file, key) #Encrypts File After rewrite

        file_size = os.path.getsize(input_file)
        chunk_size = int(file_size / 10)  # Size of memory in bytes

        #Splits file into chunks
        index = 0
        while True:
            chunk = file_obj.read(chunk_size)
            if not chunk:
                break
            output_file = os.path.join(output_directory, f'chunk_{index}.bin')

            with open(output_file, 'wb') as out:
                out.write(chunk)

            os.remove(os.path.join(output_directory, f'chunk_{index}.bin'))
            index += 1

    os.remove(input_file)
    messagebox.showinfo('Warning', "Purge Completed")

#Open file Button "Browse"
def openfiles():
    global file
    file_path = fd.askopenfilename()
    if file_path:
        file.set(file_path)
    else:
        messagebox.showerror("Error", "No file selected!")

#Browse Button
select_btn = Button(root, text="Browse", command=openfiles, width=5, height=1, font=('normal', 10), background="lavender")
select_btn.grid(row=1, column=0, sticky='W')
select_btn.pack()

#Delete Button
delete_btn = Button(root, text="Purge", command=deleteb, width=5, height=1, font=('normal', 10), background="red")
#delete_btn.grid(row=0, column=0, sticky='W')
delete_btn.pack()

#Path background frame
f1 = Frame(root, width=100, height=50, background="lavender")
#f1.grid(row=1, column=1, columnspan=1)
f1.pack()

#Path "Label" on frame
Path_Label = Label(f1, text="Path:", font=("regular", 10), bg='lavender')
#Path_Label.grid(row=0, column=0, pady=5, padx=1)
Path_Label.pack()

#Path Address display (Bold, 10pts)
Path_Link = Label(f1, width=30, textvariable=file, font=('bold', 10))
#Path_Link.grid(row=0, column=1, pady=5, padx=5)
Path_Link.pack()

root.mainloop() #GUI Loop
#