import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import re
import os
import requests
import pyperclip

COMMON_PASSWORDS = [
    "password", "123456", "123456789", "12345678", "12345", "1234567",
    "1234567", "1234567", "1234567", "1234567", "1234567", "1234567",
    "qwerty", "abc123", "monkey", "1234567890", "123123", "password1",
    "qwerty123", "admin", "welcome", "login", "passw0rd", "1234"
]

def download_dictionary_file():
    if os.path.exists("dictionary.txt"):
        print("Dictionary file already exists.")
        return True

    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open("dictionary.txt", "wb") as file:
            file.write(response.content)
        print("Dictionary file downloaded successfully.")
        return True
    else:
        print("Failed to download dictionary file.")
        return False

def generate_password(length, use_numbers, use_letters, use_special_chars):
    characters = ''
    if use_numbers:
        characters += string.digits
    if use_letters:
        characters += string.ascii_letters
    if use_special_chars:
        characters += string.punctuation

    if not characters:
        messagebox.showinfo("Error", "Please select at least one type of characters (numbers, letters, or special characters).")
        return None

    if not os.path.exists("generated.txt"):
        with open("generated.txt", "w"): pass

    password = ''.join(random.choice(characters) for _ in range(length))
    with open("generated.txt", "w") as file:
        file.write(password)
    return password

def check_password_strength(password):
    # Check length
    if len(password) < 8:
        return "Weak: Password length should be at least 8 characters."

    # Check for common passwords
    if password.lower() in COMMON_PASSWORDS:
        return "Weak: Commonly used password. Choose a different one."

    # Check for dictionary words
    with open("dictionary.txt", "r") as file:
        dictionary = file.read().splitlines()

    if password.lower() in dictionary:
        return "Weak: Password is a dictionary word. Choose a different one."

    # Check for uppercase, lowercase, numbers, and special characters
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)

    if not all([has_uppercase, has_lowercase, has_digit, has_special]):
        return "Weak: Password should contain uppercase, lowercase, numbers, and special characters."

    # Check for common patterns that reduce password strength
    if re.search(r"(.)\1\1", password):
        return "Weak: Password contains repeating characters."

    if re.search(r"\d{4,}", password):
        return "Weak: Password contains a sequence of digits."

    if re.search(r"[a-zA-Z]{4,}", password):
        return "Weak: Password contains a sequence of letters."

    return "Strong: Password meets all criteria for strength."

def generate_and_check_password():
    length = int(length_entry.get())
    use_numbers = numbers_var.get()
    use_letters = letters_var.get()
    use_special_chars = special_chars_var.get()

    password = generate_password(length, use_numbers, use_letters, use_special_chars)
    if password:
        password_strength = check_password_strength(password)
        password_result_label.config(text=f"Generated Password: {password}\nPassword Strength: {password_strength}")
        copy_button.config(state=tk.NORMAL)  # Enable the copy button

def copy_password():
    with open("generated.txt", "r") as file:
        password = file.read()
    pyperclip.copy(password)

# Download the dictionary file
if download_dictionary_file():
    print("Dictionary file downloaded successfully.")

# Create the main window
root = tk.Tk()
root.title("Password Generator and Strength Checker")

# Add style
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", foreground="black", background="#007bff")
style.map("TButton", background=[("active", "#0056b3")])

# Length label and entry
length_label = tk.Label(root, text="Password Length:")
length_label.pack()
length_entry = tk.Entry(root)
length_entry.pack()

# Checkboxes for character types
numbers_var = tk.BooleanVar()
numbers_checkbutton = ttk.Checkbutton(root, text="Include Numbers", variable=numbers_var)
numbers_checkbutton.pack()

letters_var = tk.BooleanVar()
letters_checkbutton = ttk.Checkbutton(root, text="Include Letters", variable=letters_var)
letters_checkbutton.pack()

special_chars_var = tk.BooleanVar()
special_chars_checkbutton = ttk.Checkbutton(root, text="Include Special Characters", variable=special_chars_var)
special_chars_checkbutton.pack()

# Button to generate and check password
generate_button = ttk.Button(root, text="Generate and Check Password", command=generate_and_check_password)
generate_button.pack()

# Button to copy password to clipboard
copy_button = ttk.Button(root, text="Copy Password", command=copy_password, state=tk.DISABLED)
copy_button.pack()

# Label to display generated password and its strength
password_result_label = tk.Label(root, text="")
password_result_label.pack()

# Start the GUI event loop
root.mainloop()
