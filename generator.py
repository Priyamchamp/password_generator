import argparse
import os
import random
import re
import requests
import string
import pyperclip

COMMON_PASSWORDS = [
    "password", "123456", "123456789", "12345678", "12345", "1234567",
    "1234567", "1234567", "1234567", "1234567", "1234567", "1234567",
    "qwerty", "abc123", "monkey", "1234567890", "123123", "password1",
    "qwerty123", "admin", "welcome", "login", "passw0rd", "1234"
]

def download_dictionary_file():
    if os.path.exists("password_generator/dictionary.txt"):
        print("Dictionary file already exists.")
        return True

    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open("password_generator/dictionary.txt", "wb") as file:
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
        print("Please select at least one type of characters (numbers, letters, or special characters).")
        return None

    if not os.path.exists("password_generator/generated.txt"):
        with open("password_generator/generated.txt", "w"): pass

    password = ''.join(random.choice(characters) for _ in range(length))
    with open("password_generator/generated.txt", "w") as file:
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
    with open("password_generator/dictionary.txt", "r") as file:
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

def generate_and_check_password(length, use_numbers, use_letters, use_special_chars):
    password = generate_password(length, use_numbers, use_letters, use_special_chars)
    if password:
        password_strength = check_password_strength(password)
        print(f"Generated Password: {password}\nPassword Strength: {password_strength}")

def copy_password():
    with open("password_generator/generated.txt", "r") as file:
        password = file.read()
    pyperclip.copy(password)

def main():
    parser = argparse.ArgumentParser(description="Generate and check password strength.")
    parser.add_argument("--length", type=int, default=12, help="Length of the password (default: 12)")
    parser.add_argument("--numbers", action="store_true", help="Include numbers in the password")
    parser.add_argument("--letters", action="store_true", help="Include letters in the password")
    parser.add_argument("--special-chars", action="store_true", help="Include special characters in the password")
    parser.add_argument("--copy", action="store_true", help="Copy the generated password to the clipboard")
    args = parser.parse_args()

    if not (args.numbers or args.letters or args.special_chars):
        parser.error("Please select at least one type of characters (numbers, letters, or special characters).")

    if download_dictionary_file():
        print("Dictionary file downloaded successfully.")

    password = generate_password(args.length, args.numbers, args.letters, args.special_chars)
    if password:
        password_strength = check_password_strength(password)
        print(f"Generated Password: {password}\nPassword Strength: {password_strength}")
        if args.copy:
            copy_password()

if __name__ == "__main__":
    main()
