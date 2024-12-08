
# General File Deletion (HDDs)
This version is designed for traditional hard drives (HDDs) and employs a combination of encryption, overwriting, chunking, and file deletion to make files unrecoverable.

## Features
Encryption:

Files are encrypted using the cryptography.fernet library before and after overwriting.
This ensures that any residual data remains inaccessible.
Overwriting:

Files are overwritten multiple times with random ASCII and Unicode characters.
This process scrambles the original data at the physical storage level.
Chunking and Deletion:

Files are split into chunks, and each chunk is rewritten and then deleted.
GUI for Ease of Use:

Browse and select files.
Initiate the deletion process with a button click.
How It Works
Select the file using the "Browse" button.
Click "Purge" to securely delete the file.
The file will be encrypted, overwritten, split into chunks, and finally deleted.

## Requirements
Python 3.x

## Dependencies:
  cryptography
  tkinter
  unicodedata
  random

## Execution:

```bash
python data_manager.py
