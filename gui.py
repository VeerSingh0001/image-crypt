import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
import os
import threading
from main import (
    encrypt_img,
    decrypt_img,
    encrypt_multiple_files,
    decrypt_multiple_files,
)


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
        


        self.encrypt_button = ttk.Button(self, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = ttk.Button(self, text="Decrypt", command=self.decrypt)
        self.decrypt_button.pack(pady=10)

    def encrypt(self):
        # [ACTION] Set mode to "encrypt" and initiate image selection.
        self.type = "encrypt"
        self.multiple_files()

    def decrypt(self):
        # [ACTION] Set mode to "decrypt" and initiate image selection.
        self.type = "decrypt"
        self.multiple_files()

    def get_image_selection(self):
        # [PROMPT] Update UI to ask how many images for the current method.
        self.label2.config(
            text=f"How many images do you want to {self.type.capitalize()}?"
        )
        self.label2.pack(expand=False, fill=tk.X, pady=10)
        self.encrypt_button.config(text="Single", command=self.single_file)
        self.encrypt_button.pack(pady=10)
        self.decrypt_button.config(text="Multiple", command=self.multiple_files)
        self.decrypt_button.pack(pady=10)

    def single_file(self):
        # [UI] Prepare interface for single file selection and passphrase entry.
        self.encrypt_button.destroy()
        self.decrypt_button.destroy()
        self.label2.config(
            text=f"Select a single image file to {self.type.capitalize()}:"
        )
        self.label2.pack(expand=False, fill=tk.X, pady=10)

        self.passphrase_label = ttk.Label(
            self, text="Enter Passphrase:", anchor="center", font=("Helvetica", 10)
        )
        self.passphrase_label.pack(expand=False, fill=tk.X, pady=5)

        self.passphrase_entry = ttk.Entry(
            self, show="*"
        ) 
        self.passphrase_entry.pack(expand=False, fill=tk.X, pady=5)
        self.passphrase_entry.focus()  

        self.get_file = ttk.Button(self, text="Select File", command=self.select_file)
        self.get_file.pack(pady=10)

    def multiple_files(self):
        # [UI] Prepare interface for multiple files selection and passphrase entry.
        self.encrypt_button.destroy()
        self.decrypt_button.destroy()
        self.label2.config(
            text=f"Select image file/files to {self.type.capitalize()}:"
        )
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

    def select_file(self):
        # [FILE] Open file dialog and process single file based on mode.
        phrase = self.get_passphrase()
        if not phrase:
            tk.messagebox.showerror("Error", "Please enter a passphrase.")
            return

        if self.type == "encrypt":
            file_path = tk.filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
            )

            if file_path:
                self.image_path = file_path
                self.encrypt_img(self.image_path, self.get_passphrase())

            else:
                tk.messagebox.showerror("Error", "No file selected.")

        elif self.type == "decrypt":
            file_path = tk.filedialog.askopenfilename(
                filetypes=[("Encrypted files", "*.des")]
            )
            if file_path:
                self.image_path = file_path
                self.decrypt_img(self.image_path, self.get_passphrase())
            else:
                tk.messagebox.showerror("Error", "No file selected.")

    def select_folder(self):
        # [FILE] Open file dialog to select multiple files and process them based on mode.
        phrase = self.get_passphrase()
        if not phrase:
            tk.messagebox.showerror("Error", "Please enter a passphrase.")
            return

        file_paths = tk.filedialog.askopenfilenames(
            title=f"Select Files to {self.type.capitalize()}",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff;*.webp;*.svg;*.ico;*.raw;*.jfif;*.heif;*.psd;*.xcf;*.icns;*.dds;*.exr") if self.type == "encrypt" else ("Encrypted files", "*.des")]
        )
        image_files = len(file_paths)
        if image_files:
            self.show_progress(f"Processing selected files, please wait...")

            def process():
                if self.type == "encrypt":
                    enc = encrypt_multiple_files(file_paths, self.get_passphrase())
                    self.hide_progress()
                    if enc:
                        tk.messagebox.showinfo("Success", f"Files encrypted successfully")
                        self.home_screen()
                    else:
                        tk.messagebox.showerror("Error", "Encryption failed. Please try again.")

                elif self.type == "decrypt":
                    dec = decrypt_multiple_files(file_paths, self.get_passphrase())
                    self.hide_progress()
                    if dec:
                        tk.messagebox.showinfo("Success", f"Files decrypted successfully")
                        self.home_screen()
                    else:
                        tk.messagebox.showerror("Error", "Decryption failed. Please try again.")

            threading.Thread(target=process).start()
        else:
            tk.messagebox.showerror("Error", "No files selected.")

    def show_progress(self, current, total):
        # [UI] Display progress by showing the current file being processed out of the total.
        progress_message = f"Processing file {current} of {total}..."
        self.progress_label = ttk.Label(self, text=progress_message, anchor="center", font=("Helvetica", 10))
        self.progress_label.pack(expand=False, fill=tk.X, pady=5)
        self.update_idletasks()

    def hide_progress(self):
        # [UI] Remove the progress message from the UI.
        if hasattr(self, 'progress_label'):
            self.progress_label.destroy()

    def encrypt_img(
        self,
        img_path,
        passphrase,
    ):
        # [PROCESS] Encrypt the image file and update the UI on success/failure.
        self.show_progress("Encrypting file, please wait...")

        def process():
            enc = encrypt_img(img_path, passphrase)
            self.hide_progress()

            if enc == 0:
                return

            if enc:
                tk.messagebox.showinfo("Success", f"File encrypted successfully")

                self.home_screen()

            else:
                tk.messagebox.showerror("Error", "Encryption failed. Please try again.")

        threading.Thread(target=process).start()

    def decrypt_img(
        self,
        img_path,
        passphrase,
    ):
        # [PROCESS] Decrypt the encrypted file and update the UI on success/failure.
        self.show_progress("Decrypting file, please wait...")

        def process():
            dec = decrypt_img(img_path, passphrase)
            self.hide_progress()

            if dec:
                tk.messagebox.showinfo("Success", f"File decrypted successfully")

                self.home_screen()
            elif dec == 0:
                tk.messagebox.showerror(f"Error", "Incorrect Passphrase for {img_path}")
            else:
                tk.messagebox.showerror("Error", "Decryption failed. Please try again.")

        threading.Thread(target=process).start()

    def home_screen(self):
        # [RESET] Restore the initial home screen UI.
        self.label2.config(text="Choose an option:")
        self.label2.pack(expand=False, fill=tk.X, pady=10)
        self.encrypt_button = ttk.Button(self, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = ttk.Button(self, text="Decrypt", command=self.decrypt)
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
