# **Data Manager: Secure File Deletion Tool**

The **Data Manager** is a secure file deletion tool that supports both HDDs and SSDs. It provides an intuitive graphical user interface (GUI) to securely delete files by overwriting, encrypting, and managing file storage.

## **Features**

### **General File Deletion (HDDs)**
- **Encryption**: 
  - Files are encrypted using the `cryptography.fernet` library.
  - Encryption is applied both before and after the overwriting process to ensure that any residual data remains inaccessible.
- **Overwriting**:
  - Files are overwritten multiple times with random ASCII and Unicode characters.
  - This process ensures that the original data is scrambled and unrecoverable.
- **Chunking and Deletion**:
  - Files are split into chunks, rewritten, and then deleted.
  - Each chunk is securely processed to make recovery impossible.

### **SSD-Specific Deletion**
- **Windows (SSDWin)**:
  - Utilizes PowerShell's `Optimize-Volume` command to issue TRIM commands for secure file deletion on SSDs.
- **Linux (SSDLinux)**:
  - Uses the `blkdiscard` utility to securely discard file data on SSDs.
  - Requires `sudo` privileges to execute.
  
### **User-Friendly GUI**
- Intuitive interface built with **Tkinter**.
- Options to:
  - Select a file using the **Browse** button.
  - Choose between HDD, Windows SSD, and Linux SSD deletion methods via a dropdown menu.
  - Monitor progress with a **Progress Bar** and real-time **Status Messages**.

---

## **Usage**

1. **Run the Script**:
   - Open the script with Python (`python data_manager.py`).
   - If administrative privileges are required, the script will prompt for elevation.
   
2. **Choose a File**:
   - Click the **Browse** button to select the file you want to delete.
   
3. **Select Deletion Method**:
   - From the dropdown, choose the desired method:
     - `HDD`: Overwrites and securely deletes files on traditional hard drives.
     - `SSDWin`: Issues a TRIM command for SSDs on Windows.
     - `SSDLinux`: Uses the `blkdiscard` command for SSDs on Linux.

4. **Start the Process**:
   - Click the **Purge** button to initiate the secure deletion process.
   - Monitor the progress via the progress bar and status messages.

---

## **Requirements**

- **Python**: Version 3.6 or higher.
- **Operating System**:
  - Windows 10/11
  - Linux distributions supporting `blkdiscard`.
- **Privileges**:
  - Administrative privileges are required to perform SSD-specific deletions.

---

## **Dependencies**

Ensure the following Python libraries are installed:
- `cryptography`
- `tkinter`
- `unicodedata`

To install dependencies, use:

```bash
pip install -r requirements.txt


```
## Execution
  Run the script from your terminal or command prompt:

```bash
    python secure_eraser.py
  ```
If administrative privileges are required, the script will prompt you to confirm elevation.

## Additional Notes
### Windows SSD Deletion:

Ensure Optimize-Volume is available in your PowerShell environment.
Run the script as an administrator to issue TRIM commands.
Linux SSD Deletion:

Requires blkdiscard to be installed (sudo apt install util-linux on Debian/Ubuntu).
The script must be run with sudo privileges.
Data Manager is Irreversible:

Once the deletion process is initiated, the file cannot be recovered.

# Disclaimer
This script is designed for secure file deletion and should be used with caution. Ensure you have backups of important data before initiating the deletion process. The developers are not responsible for any unintended data loss.