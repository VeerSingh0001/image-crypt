import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
import os
from main import (
    encrypt_img,
    decrypt_img,
    encrypt_multiple_files,
    decrypt_multiple_files,
)


class MainGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="20")
        self.pack(fill=tk.BOTH, expand=True)

        self.type = ""
        self.image = ""
        self.image_path = ""
        self.encrypted_image_path = ""
        self.passphrase = ""
        # Create a centered label
        self.label = ttk.Label(
            self, text="Image Cryptography", anchor="center", font=("Helvetica", 18)
        )
        self.label.pack(expand=False, fill=tk.X, pady=20)

        self.label2 = ttk.Label(
            self, text="Choose an option:", anchor="center", font=("Helvetica", 12)
        )
        self.label2.pack(expand=False, fill=tk.X, pady=10)
        # More widgets (buttons, entries, etc) can be added below
        # For example, an encrypt button:

        # Add the encrypt and decrypt buttons after the entry
        self.encrypt_button = ttk.Button(self, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = ttk.Button(self, text="Decrypt", command=self.decrypt)
        self.decrypt_button.pack(pady=10)

    def encrypt(self):
        # Call your encryption logic here
        self.type = "encrypt"
        type = self.get_image_selection()

    def decrypt(self):
        # Call your decryption logic here
        self.type = "decrypt"
        type = self.get_image_selection()

    def get_image_selection(self):
        self.label2.config(
            text=f"How many images do you want to {self.type.capitalize()}?"
        )
        self.label2.pack(expand=False, fill=tk.X, pady=10)
        self.encrypt_button.config(text="Single", command=self.single_file)
        self.encrypt_button.pack(pady=10)
        self.decrypt_button.config(text="Multiple", command=self.multiple_files)
        self.decrypt_button.pack(pady=10)

    def single_file(self):
        self.encrypt_button.destroy()
        self.decrypt_button.destroy()
        self.label2.config(
            text=f"Select a single image file to {self.type.capitalize()}:"
        )
        self.label2.pack(expand=False, fill=tk.X, pady=10)

        # Add passphrase entry
        self.passphrase_label = ttk.Label(
            self, text="Enter Passphrase:", anchor="center", font=("Helvetica", 10)
        )
        self.passphrase_label.pack(expand=False, fill=tk.X, pady=5)

        self.passphrase_entry = ttk.Entry(
            self, show="*"
        )  # show="*" makes it display asterisks for security
        self.passphrase_entry.pack(expand=False, fill=tk.X, pady=5)
        self.passphrase_entry.focus()  # Set focus to the passphrase entry field

        self.get_file = ttk.Button(self, text="Select File", command=self.select_file)
        self.get_file.pack(pady=10)

    def multiple_files(self):
        self.encrypt_button.destroy()
        self.decrypt_button.destroy()
        self.label2.config(
            text=f"Select multiple image files to {self.type.capitalize()}:"
        )
        self.label2.pack(expand=False, fill=tk.X, pady=10)

        # Add passphrase entry
        self.passphrase_label = ttk.Label(
            self, text="Enter Passphrase:", anchor="center", font=("Helvetica", 10)
        )
        self.passphrase_label.pack(expand=False, fill=tk.X, pady=5)

        self.passphrase_entry = ttk.Entry(self, show="*")
        self.passphrase_entry.pack(expand=False, fill=tk.X, pady=5)
        self.passphrase_entry.focus()

        self.get_folder = ttk.Button(
            self, text="Select Folder", command=self.select_folder
        )
        self.get_folder.pack(pady=10)

    def get_passphrase(self):
        return self.passphrase_entry.get()

    def select_file(self):
        # Open a file dialog to select an image file
        phrase = self.get_passphrase()
        if not phrase:
            tk.messagebox.showerror("Error", "Please enter a passphrase.")
            return

        # Encrypt or decrypt the selected file based on the types
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

        phrase = self.get_passphrase()
        if not phrase:
            tk.messagebox.showerror("Error", "Please enter a passphrase.")
            return

        files_folder = tk.filedialog.askdirectory(title=f"Select Folder to {self.type.capitalize()} Files")
        image_files = []
        if files_folder:
            # Get all valid image files based on the operation type.
            if self.type == "encrypt":
                for file in os.listdir(files_folder):
                    if file.lower().endswith((".jpg", ".jpeg", ".png")):
                        image_files.append(os.path.join(files_folder, file))
                enc = encrypt_multiple_files(image_files, self.get_passphrase())
                if enc:
                    tk.messagebox.showinfo("Success", f"Files encrypted successfully")
                    self.home_screen()
                else:   
                    tk.messagebox.showerror("Error", "Encryption failed. Please try again.")

            elif self.type == "decrypt":
                for file in os.listdir(files_folder):
                    if file.lower().endswith(".des"):
                        image_files.append(os.path.join(files_folder, file))
                dec = decrypt_multiple_files(image_files, self.get_passphrase())
                if dec:
                    tk.messagebox.showinfo("Success", f"Files decrypted successfully") 
                    self.home_screen()
                else:
                    tk.messagebox.showerror("Error", "Decryption failed. Please try again.")
                
        else:
            tk.messagebox.showerror("Error", "No folder selected.")

    def encrypt_img(
        self,
        img_path,
        passphrase,
    ):
        # Encryption logic here
        print(f"Encrypting {img_path} with passphrase: {passphrase}")
        # Add your encryption code here
        enc = encrypt_img(img_path, passphrase)  # Call the function from main.py

        if end == 0:
            return

        if enc:
            tk.messagebox.showinfo("Success", f"File encrypted successfully")

            self.home_screen()

        else:
            tk.messagebox.showerror("Error", "Encryption failed. Please try again.")

    def decrypt_img(
        self,
        img_path,
        passphrase,
    ):
        # Decryption logic here
        print(f"Decrypting {img_path} with passphrase: {passphrase}")
        # Add your decryption code here
        dec = decrypt_img(img_path, passphrase)  # Call the function from main.py

        if dec:
            tk.messagebox.showinfo("Success", f"File decrypted successfully")

            self.home_screen()
        elif dec == 0:
            tk.messagebox.showerror(f"Error", "Incorrect Passphrase for {img_path}")
        else:
            tk.messagebox.showerror("Error", "Decryption failed. Please try again.")

    def home_screen(self):
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
