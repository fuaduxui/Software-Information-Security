import os
import json
from hashlib import sha256

DB_FILE = "users_db.json"

def hash_password(password):
    if not password:
        return ""
    return sha256(password.encode()).hexdigest()

def check_complexity(password):
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_letter and has_digit

def load_db():
    if not os.path.exists(DB_FILE):
        db = {
            "ADMIN": {
                "password": hash_password(""),
                "blocked": False,
                "restricted": False
            }
        }
        save_db(db)
        return db
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def login():
    db = load_db()
    for _ in range(3):
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if username not in db:
            print("Access denied. User not found.")
            continue
            
        user_data = db[username]
        
        if user_data["blocked"]:
            print("Account is blocked by administrator.")
            return None, None
            
        if user_data["password"] == hash_password(password):
            print(f"Login successful. Welcome, {username}!")
            return username, user_data
        else:
            print("Incorrect password.")
            
    print("Three incorrect attempts. Program terminated.")
    exit()

def admin_menu(username):
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Change admin password")
        print("2. View registered users")
        print("3. Add new user")
        print("4. Block/Unblock user")
        print("5. Toggle password restrictions")
        print("6. About program")
        print("7. Exit")
        
        choice = input("Select action: ").strip()
        db = load_db()
        
        if choice == "1":
            old_pass = input("Enter old password: ").strip()
            if db[username]["password"] == hash_password(old_pass):
                new_pass = input("Enter new password: ").strip()
                confirm_pass = input("Confirm new password: ").strip()
                if new_pass != confirm_pass:
                    print("Passwords do not match.")
                    continue
                if db[username]["restricted"] and not check_complexity(new_pass):
                    print("Password must contain both letters and digits.")
                    continue
                db[username]["password"] = hash_password(new_pass)
                save_db(db)
                print("Password changed successfully.")
            else:
                print("Wrong old password.")
                
        elif choice == "2":
            print("\nUser list:")
            for u, data in db.items():
                print(f"User: {u} | Blocked: {data['blocked']} | Restrictions: {data['restricted']}")
                
        elif choice == "3":
            new_user = input("Enter unique username to add: ").strip()
            if not new_user:
                print("Username cannot be empty.")
                continue
            if new_user in db:
                print("User already exists.")
                continue
            db[new_user] = {
                "password": hash_password(""),
                "blocked": False,
                "restricted": False
            }
            save_db(db)
            print(f"User {new_user} added with empty password.")
            
        elif choice == "4":
            target_user = input("Enter username to change block state: ").strip()
            if target_user == "ADMIN":
                print("Cannot block administrator account.")
                continue
            if target_user not in db:
                print("User not found.")
                continue
            db[target_user]["blocked"] = not db[target_user]["blocked"]
            save_db(db)
            print(f"User {target_user} blocked status now: {db[target_user]['blocked']}")
            
        elif choice == "5":
            target_user = input("Enter username to change restrictions: ").strip()
            if target_user not in db:
                print("User not found.")
                continue
            db[target_user]["restricted"] = not db[target_user]["restricted"]
            save_db(db)
            print(f"Restrictions for {target_user} set to: {db[target_user]['restricted']}")
            
        elif choice == "6":
            print("\nAbout Program:")
            print("Author: Fuad Mammadov")
            print("Task: Password authentication and encryption system. Variant 3.")
            
        elif choice == "7":
            print("Closing application.")
            break

def user_menu(username):
    while True:
        print(f"\n--- USER MENU ({username}) ---")
        print("1. Change password")
        print("2. About program")
        print("3. Exit")
        
        choice = input("Select action: ").strip()
        db = load_db()
        
        if choice == "1":
            old_pass = input("Enter old password: ").strip()
            if db[username]["password"] == hash_password(old_pass):
                new_pass = input("Enter new password: ").strip()
                confirm_pass = input("Confirm new password: ").strip()
                if new_pass != confirm_pass:
                    print("Passwords do not match.")
                    continue
                if db[username]["restricted"] and not check_complexity(new_pass):
                    print("Password must contain both letters and digits.")
                    continue
                db[username]["password"] = hash_password(new_pass)
                save_db(db)
                print("Password changed successfully.")
            else:
                print("Wrong old password.")
        elif choice == "2":
            print("\nAbout Program:")
            print("Author: Fuad Mammadov")
            print("Task: Password authentication and encryption system. Variant 3.")
        elif choice == "3":
            print("Closing application.")
            break

def main():
    print("Security System Authorization")
    username, user_data = login()
    if not username:
        return
        
    if username == "ADMIN":
        admin_menu(username)
    else:
        user_menu(username)

if __name__ == "__main__":
    main()
