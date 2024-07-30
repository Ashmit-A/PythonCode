import os
import json
from cryptography.fernet import Fernet

def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

def save_passwords(passwords):
    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

def load_passwords():
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            return json.load(file)
    return {}

def add_password(website, password, key):
    passwords = load_passwords()
    passwords[website] = encrypt_password(password, key)
    save_passwords(passwords)

def get_password(website, key):
    passwords = load_passwords()
    if website in passwords:
        return decrypt_password(passwords[website], key)
    return None

def delete_password(website):
    passwords = load_passwords()
    if website in passwords:
        del passwords[website]
        save_passwords(passwords)

def main():
    generate_key()
    key = load_key()

    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Delete Password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            website = input("Enter the website: ")
            password = input("Enter the password: ")
            add_password(website, password, key)
            print("Password added successfully!")
        elif choice == "2":
            website = input("Enter the website: ")
            password = get_password(website, key)
            if password:
                print(f"Password for {website}: {password}")
            else:
                print("Password not found!")
        elif choice == "3":
            website = input("Enter the website: ")
            delete_password(website)
            print("Password deleted successfully!")
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
