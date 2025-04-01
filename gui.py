import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
import os
from main import (encrypt_multiple_files, decrypt_multiple_files)


class MainGUI(ttk.Frame):
    def __init__(self, parent):
        # [INIT] Initialize GUI frame, configure layout and variables.
        super().__init__(parent, padding="20")
        self.pack(fill=tk.BOTH, expand=True)

        self.type = ""
        self.image = ""
        self.image_path = ""
        self.encrypted_image_path = ""
        self.passphrase = ""

        self.label = ttk.Label(
            self, text="Image Cryptography", anchor="center", font=("Helvetica", 18)
        )
        self.label.pack(expand=False, fill=tk.X, pady=20)

        self.label2 = ttk.Label(
            self, text="Choose an option:", anchor="center", font=("Helvetica", 12)
        )
        self.label2.pack(expand=False, fill=tk.X, pady=10)

        self.encrypt_button = ttk.Button(
            self, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = ttk.Button(
            self, text="Decrypt", command=self.decrypt)
        self.decrypt_button.pack(pady=10)

    def encrypt(self):
        # [ACTION] Set mode to "encrypt" and initiate image selection.
        self.type = "encrypt"
        self.multiple_files()

    def decrypt(self):
        # [ACTION] Set mode to "decrypt" and initiate image selection.
        self.type = "decrypt"
        self.multiple_files()

    def multiple_files(self):
        # [UI] Prepare interface for multiple files selection and passphrase entry.
        self.encrypt_button.destroy()
        self.decrypt_button.destroy()
        self.label2.config(
            text=f"Select image file(s) to {self.type.capitalize()}:")
        self.label2.pack(expand=False, fill=tk.X, pady=10)

        self.passphrase_label = ttk.Label(
            self, text="Enter Passphrase:", anchor="center", font=("Helvetica", 10)
        )
        self.passphrase_label.pack(expand=False, fill=tk.X, pady=5)

        self.passphrase_entry = ttk.Entry(self, show="*")
        self.passphrase_entry.pack(expand=False, fill=tk.X, pady=5)
        self.passphrase_entry.focus()

        self.get_folder = ttk.Button(
            self, text="Select file(s)", command=self.select_folder
        )
        self.get_folder.pack(pady=10)

    def get_passphrase(self):
        # [UTIL] Retrieve the passphrase from the entry widget.
        return self.passphrase_entry.get()

    def select_folder(self):
        # [FILE] Open file dialog to select multiple files and process them based on mode.
        phrase = self.get_passphrase()
        if not phrase:
            tk.messagebox.showerror("Error", "Please enter a passphrase.")
            return

        file_paths = tk.filedialog.askopenfilenames(
            title=f"Select Files to {self.type.capitalize()}",
            filetypes=[
                (
                    (
                        "Image files",
                        "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff;*.webp;*.svg;*.ico;*.raw;*.jfif;*.heif;*.psd;*.xcf;*.icns;*.dds;*.exr",
                    )
                    if self.type == "encrypt"
                    else ("Encrypted files", "*.des")
                )
            ],
        )
        image_files = len(file_paths)
        if image_files:
            self.show_progress(
                f"{self.type.capitalize()}ing selected files, please wait..."
            )

            if self.type == "encrypt":
                enc = encrypt_multiple_files(file_paths, self.get_passphrase())
                self.hide_progress()
                if enc:
                    tk.messagebox.showinfo(
                        "Success", f"Files encrypted successfully")
                    self.home_screen()
                else:
                    tk.messagebox.showerror(
                        "Error", "Encryption failed. Please try again."
                    )

            elif self.type == "decrypt":
                dec = decrypt_multiple_files(file_paths, self.get_passphrase())
                self.hide_progress()
                if dec:
                    tk.messagebox.showinfo(
                        "Success", f"Files decrypted successfully")
                    self.home_screen()
                elif dec == 0:
                    tk.messagebox.showerror(
                        "Error", "Incorrect Passphrase for one or more files."
                    )
                else:
                    tk.messagebox.showerror(
                        "Error", "Decryption failed. Please try again."
                    )
        else:
            tk.messagebox.showerror("Error", "No files selected.")

    def show_progress(self, message):
        # [UI] Display a progress message to the user.
        self.progress_label = ttk.Label(
            self, text=message, anchor="center", font=("Helvetica", 10)
        )
        self.progress_label.pack(expand=False, fill=tk.X, pady=5)
        self.update_idletasks()

    def hide_progress(self):
        # [UI] Remove the progress message from the UI.
        if hasattr(self, "progress_label"):
            self.progress_label.destroy()

    def home_screen(self):
        # [RESET] Restore the initial home screen UI.
        self.label2.config(text="Choose an option:")
        self.label2.pack(expand=False, fill=tk.X, pady=10)
        self.encrypt_button = ttk.Button(
            self, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = ttk.Button(
            self, text="Decrypt", command=self.decrypt)
        self.decrypt_button.pack(pady=10)
        self.passphrase_label.destroy()
        self.passphrase_entry.destroy()
        if hasattr(self, "get_file"):
            self.get_file.destroy()
        if hasattr(self, "get_folder"):
            self.get_folder.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Cryptography")
    root.geometry("400x300")
    MainGUI(root)
    root.mainloop()
