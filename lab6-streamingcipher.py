import os
import sys

def rc4_init(key_bytes):
    key_len = len(key_bytes)
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key_bytes[i % key_len]) % 256
        s[i], s[j] = s[j], s[i]
    return s

def rc4_crypt(data_bytes, key_str):
    key_bytes = key_str.encode('utf-8')
    if not key_bytes:
        key_bytes = b'default_key'
        
    s = rc4_init(key_bytes)
    res = bytearray()
    i = 0
    j = 0
    
    for byte in data_bytes:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        t = (s[i] + s[j]) % 256
        k = s[t]
        res.append(byte ^ k)
        
    return bytes(res)

def main():
    print("--- STREAMING ENCRYPTION UTILITY (RC4) ---")
    print("1. Encrypt file")
    print("2. Decrypt file")
    print("3. Exit")
    
    choice = input("Select action: ").strip()
    
    if choice == "1":
        src = input("Enter source file path (e.g. lab5_encryption.py): ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        key = input("Enter encryption key: ").strip()
        dst = src + ".stream"
        
        with open(src, 'rb') as f:
            data = f.read()
            
        encrypted_data = rc4_crypt(data, key)
        
        with open(dst, 'wb') as f:
            f.write(encrypted_data)
            
        print(f"File encrypted successfully: {dst}")
        
    elif choice == "2":
        src = input("Enter encrypted file path (.stream): ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        key = input("Enter decryption key: ").strip()
        dst = src.replace(".stream", "_restored.py")
        
        with open(src, 'rb') as f:
            data = f.read()
            
        decrypted_data = rc4_crypt(data, key)
        
        with open(dst, 'wb') as f:
            f.write(decrypted_data)
            
        print(f"File decrypted successfully: {dst}")
        
    elif choice == "3":
        sys.exit()

if __name__ == "__main__":
    main()
