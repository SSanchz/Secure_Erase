import os
import sys
import platform
import ctypes
import subprocess
from tkinter import Tk, StringVar, filedialog, messagebox, Frame, Button, OptionMenu, Label, HORIZONTAL, TOP
from tkinter import ttk
from cryptography.fernet import Fernet
import math
import string
import unicodedata
import shutil
import random

root = Tk()
root.geometry("560x130")
root.title("Data Manager")
root.config(background="white")

file = StringVar()  # Input file
method = StringVar(value="HDD")  # Method selection with default value "HDD"
status = StringVar()  # Status message

# Auto-elevation on Windows
def is_admin():
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    return os.geteuid() == 0  # For Linux/MacOS

def elevate():
    if platform.system() == "Windows":
        params = " ".join(f'"{arg}"' for arg in sys.argv)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()
    elif platform.system() == "Linux":
        try:
            subprocess.run(["sudo", sys.executable] + sys.argv)
        except FileNotFoundError:
            print("Error: 'sudo' is required for elevation.")
        sys.exit()

# Ensure the script is running with the required privileges
if not is_admin():
    elevate()

def secure_delete_ssd_Linux(file_path):
    try:
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found!")
            return

        messagebox.showinfo("Info", "Attempting SSD-specific secure deletion (TRIM or discard).")

        if is_linux():
            partition = os.path.realpath(file_path)
            blkdiscard_path = shutil.which("blkdiscard")
            
            if blkdiscard_path:
                subprocess.run(["sudo", blkdiscard_path, file_path], check=True)
                messagebox.showinfo("Info", f"TRIM issued for {file_path}")
            else:
                messagebox.showwarning("Warning", "blkdiscard is not available. Please install it for secure SSD deletion.")
        else:
            messagebox.showwarning("Warning", "SSD-specific secure deletion is not supported on this OS.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error during SSD secure deletion: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")

def secure_delete_ssd_windows(file_path):
    try:
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found!")
            return
        
        trim_check_cmd = ["fsutil", "behavior", "query", "DisableDeleteNotify"]
        trim_output = subprocess.run(trim_check_cmd, capture_output=True, text=True)
        
        if "0" in trim_output.stdout:
            messagebox.showinfo("Info", "TRIM is enabled. Proceeding with SSD optimization.")
        else:
            messagebox.showwarning("Warning", "TRIM is not enabled. Ensure TRIM is supported and enabled on your system.")

        optimize_cmd = [
            "powershell",
            "-Command",
            "Optimize-Volume",
            "-DriveLetter", file_path[0],
            "-ReTrim", "-Verbose"
        ]
        result = subprocess.run(optimize_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, optimize_cmd, output=result.stdout, stderr=result.stderr)
        
        messagebox.showinfo("Info", f"TRIM operation initiated for drive {file_path[0]}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error during SSD secure deletion: {e.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")

def generate_key():
    return Fernet.generate_key()

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()

    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)

    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

def delete_HDD():
    input_file = file.get()
    key = generate_key()

    if not input_file:
        messagebox.showerror("Error", "No file selected!")
        return

    output_directory = os.path.dirname(os.path.realpath(input_file))

    status.set("Encrypting file...")
    encrypt_file(input_file, key)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(input_file, 'rb+') as file_obj:
        file_size = os.path.getsize(input_file)
        
        unii = [chr(i) for i in range(0x110) if unicodedata.category(chr(i)) != 'Cn']
        char_set = string.ascii_letters + string.digits
        K_size = int(math.floor(file_size / 2))

        random_data = ''.join(random.choices(char_set, k=K_size))
        file_obj.write(random_data.encode('utf-16', errors='surrogatepass'))

        random_data = ''.join(random.choices(unii, k=K_size))
        file_obj.write(random_data.encode('utf-16', errors='surrogatepass'))
        
        file_obj.flush()
        os.fsync(file_obj.fileno())

        status.set("Encrypting file again...")
        encrypt_file(input_file, key)

        file_size = os.path.getsize(input_file)
        chunk_size = int(file_size / 10)

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

            # Update progress bar and status
            progress['value'] = (index * chunk_size / file_size) * 100
            status.set(f"Processing chunk {index}...")
            root.update_idletasks()

    if method.get() == "HDD":
        os.remove(input_file)
    elif method.get() == "SSDWin":
        secure_delete_ssd_windows(input_file)
    elif method.get() == "SSDLinux":
        secure_delete_ssd_Linux(input_file)
    
    messagebox.showinfo('Warning', "Purge Completed")
    progress['value'] = 0  # Reset progress bar
    status.set("Purge Completed")

def openfiles():
    global file
    file_path = filedialog.askopenfilename()
    if file_path:
        file.set(file_path)
    else:
        messagebox.showerror("Error", "No file selected!")

# Create a frame to hold the buttons and dropdown
button_frame = Frame(root, background="white")
button_frame.pack(side=TOP, anchor='n')

select_btn = Button(button_frame, text="Browse", command=openfiles, width=5, height=1, font=('normal', 10), background="lavender")
select_btn.grid(row=0, column=0, padx=5, pady=5)

method_menu = OptionMenu(button_frame, method, "HDD", "SSDWin", "SSDLinux")
method_menu.grid(row=0, column=1, padx=5, pady=5)

delete_btn = Button(button_frame, text="Purge", command=delete_HDD, width=5, height=1, font=('normal', 10), background="red")
delete_btn.grid(row=0, column=2, padx=5, pady=5)

Path_Label = Label(button_frame, text="Path:", font=("regular", 10), bg='lavender')
Path_Label.grid(row=0, column=3, padx=5, pady=5)

Path_Link = Label(button_frame, width=30, textvariable=file, font=('bold', 10), bg='lavender')
Path_Link.grid(row=1, column=3, padx=5, pady=5)

# Create a progress bar
progress = ttk.Progressbar(root, orient=HORIZONTAL, length=530, mode='determinate')
progress.pack(side=TOP, pady=10)

# Create a status label
status_label = Label(root, textvariable=status, font=("regular", 10), bg='white')
status_label.pack(side=TOP, pady=5)

root.mainloop()