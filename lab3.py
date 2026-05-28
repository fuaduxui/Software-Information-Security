import os
import sys
import json
import getpass
import socket
from hashlib import sha256

CONFIG_FILE = "system_hardware.key"
DB_FILE = "users_db.json"

def hash_password(password):
    if password == "":
        return sha256("".encode()).hexdigest()
    return sha256(password.encode()).hexdigest()

def check_complexity(password):
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_letter and has_digit

def get_hardware_profile():
    username = getpass.getuser()
    hostname = socket.gethostname()
    win_dir = os.environ.get('windir', '/windows')
    sys_dir = os.environ.get('systemroot', '/windows/system32')
    
    profile_string = f"{username}_{hostname}_{win_dir}_{sys_dir}"
    return sha256(profile_string.encode()).hexdigest()

def run_installer():
    print("--- SOFTWARE INSTALLATION WIZARD ---")
    install_dir = input("Enter target installation path (or press Enter for current dir): ").strip()
    if not install_dir:
        install_dir = os.getcwd()
        
    print(f"Collecting hardware signatures...")
    hw_hash = get_hardware_profile()
    
    config_data = {
        "installation_path": install_dir,
        "signature": hw_hash
    }
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
        
    db = {
        "ADMIN": {
            "password": hash_password(""),
            "blocked": False,
            "restricted": False
        }
    }
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)
        
    print("Installation completed successfully. License bound to this hardware.")
    print("Please restart the application to login.")
    sys.exit()

def verify_license():
    if not os.path.exists(CONFIG_FILE):
        return False
        
    with open(CONFIG_FILE, "r") as f:
        config_data = json.load(f)
        
    current_hw_hash = get_hardware_profile()
    return current_hw_hash == config_data["signature"]

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def login():
    db = load_db()
    attempts = 0
    while attempts < 3:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if username not in db:
            print("Access denied. User not found.")
            attempts += 1
            continue
            
        user_data = db[username]
        
        if user_data["blocked"]:
            print("Account is blocked by administrator.")
            return None
            
        if user_data["password"] == hash_password(password):
            print(f"Login successful. Welcome, {username}!")
            return username
        else:
            print("Incorrect password.")
            attempts += 1
            
    print("Three incorrect attempts. Program terminated.")
    return None

def admin_menu(username):
    while True:
        print("\n--- ADMIN MENU (SECURE ACCESS) ---")
        print("1. Change admin password")
        print("2. View registered users")
        print("3. Add new user")
        print("4. Block/Unblock user")
        print("5. Toggle password restrictions")
        print("6. Show hardware binding keys")
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
            print(f"\nCurrent HW Identifier: {get_hardware_profile()}")
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    cfg = json.load(f)
                print(f"Registered HW Identifier: {cfg['signature']}")
            
        elif choice == "7":
            break

def user_menu(username):
    while True:
        print(f"\n--- USER MENU ({username}) ---")
        print("1. Change password")
        print("2. Exit")
        
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
            break

def main():
    if not os.path.exists(CONFIG_FILE):
        run_installer()
        
    print("Checking software integrity and hardware binding status...")
    if not verify_license():
        print("[CRITICAL ERROR] Hardware signature mismatch. Access denied.")
        print("This software copy is not registered on this computer system.")
        sys.exit()
        
    print("Signature verification: OK")
    print("\n--- Security System Authorization ---")
    username = login()
    if not username:
        return
        
    if username == "ADMIN":
        admin_menu(username)
    else:
        user_menu(username)

if __name__ == "__main__":
    main()
