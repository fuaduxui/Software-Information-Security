import os
import sys

def crypt_block(block, key):
    res = bytearray()
    for i in range(len(block)):
        res.append(block[i] ^ key[i % len(key)])
    return bytes(res)

def process_file(src_path, dst_path, key_str):
    key = key_str.encode('utf-8')
    if not key:
        key = b'default'
        
    with open(src_path, 'rb') as f:
        data = f.read()
        
    res = bytearray()
    block_size = 8
    
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        res.extend(crypt_block(block, key))
        
    with open(dst_path, 'wb') as f:
        f.write(res)

def main():
    print("--- BLOCK ENCRYPTION UTILITY (DES/XOR) ---")
    print("1. Encrypt file")
    print("2. Decrypt file")
    print("3. Exit")
    
    choice = input("Select action: ").strip()
    
    if choice == "1":
        src = input("Enter source file path (e.g. lab4_data_compression.py): ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        key = input("Enter encryption key: ").strip()
        dst = src + ".enc"
        
        process_file(src, dst, key)
        print(f"File encrypted successfully: {dst}")
        
    elif choice == "2":
        src = input("Enter encrypted file path (.enc): ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        key = input("Enter decryption key: ").strip()
        dst = src.replace(".enc", "_decrypted.py")
        
        process_file(src, dst, key)
        print(f"File decrypted successfully: {dst}")
        
    elif choice == "3":
        sys.exit()

if __name__ == "__main__":
    main()
