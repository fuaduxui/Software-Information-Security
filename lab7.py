import os
import sys

def md2_hash(data_bytes):
    s = list(range(256))
    pi = [
        41, 46, 67, 201, 162, 216, 124, 1, 61, 54, 84, 161, 236, 240, 6, 19,
        98, 167, 5, 243, 192, 199, 115, 140, 152, 147, 43, 217, 188, 76, 130, 202,
        30, 155, 87, 60, 253, 212, 224, 22, 103, 66, 111, 24, 138, 23, 229, 18,
        147, 78, 112, 95, 12, 141, 50, 53, 0, 91, 47, 185, 143, 104, 238, 31,
        242, 154, 45, 131, 105, 137, 239, 122, 9, 129, 101, 48, 121, 56, 145, 118,
        251, 223, 85, 233, 254, 86, 184, 150, 139, 189, 11, 106, 13, 213, 116, 51,
        175, 241, 52, 114, 142, 218, 90, 144, 10, 193, 33, 44, 249, 14, 237, 119,
        77, 151, 42, 146, 94, 96, 255, 219, 16, 198, 32, 244, 214, 38, 40, 228,
        197, 4, 180, 57, 153, 93, 65, 49, 174, 210, 62, 74, 92, 207, 206, 102,
        225, 204, 252, 73, 187, 107, 100, 156, 113, 179, 181, 117, 173, 248, 247, 246,
        164, 149, 211, 172, 123, 165, 209, 186, 83, 158, 203, 69, 64, 178, 8, 171,
        250, 215, 68, 163, 72, 177, 63, 109, 88, 59, 55, 34, 166, 20, 230, 231,
        196, 235, 15, 21, 170, 7, 160, 169, 195, 226, 135, 216, 134, 133, 132, 127,
        26, 27, 28, 29, 35, 36, 37, 39, 42, 44, 46, 48, 50, 52, 54, 56,
        146, 125, 232, 120, 211, 110, 97, 208, 82, 126, 89, 81, 80, 79, 75, 71
    ]
    
    pad_len = 16 - (len(data_bytes) % 16)
    padded = bytearray(data_bytes) + bytearray([pad_len] * pad_len)
    
    checksum = bytearray(16)
    l = 0
    for i in range(len(padded) // 16):
        for j in range(16):
            c = padded[i * 16 + j]
            checksum[j] ^= pi[c ^ l]
            l = checksum[j]
            
    padded += checksum
    x = bytearray(48)
    
    for i in range(len(padded) // 16):
        for j in range(16):
            x[16 + j] = padded[i * 16 + j]
            x[32 + j] = x[16 + j] ^ x[j]
        t = 0
        for j in range(18):
            for k in range(48):
                t = x[k] ^= pi[t]
            t = (t + j) % 256
            
    return bytes(x[:16])

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = ext_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def generate_keys():
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    while gcd(e, phi) != 1:
        e += 2
    _, x, _ = ext_gcd(e, phi)
    d = (x % phi + phi) % phi
    return (e, n), (d, n)

def main():
    print("--- DIGITAL SIGNATURE UTILITY (RSA + MD2) ---")
    print("1. Generate new keys")
    print("2. Sign file")
    print("3. Verify signature")
    print("4. Exit")
    
    choice = input("Select action: ").strip()
    
    if choice == "1":
        pub, priv = generate_keys()
        with open("public.key", "w") as f:
            f.write(f"{pub[0]},{pub[1]}")
        with open("private.key", "w") as f:
            f.write(f"{priv[0]},{priv[1]}")
        print("Keys generated and saved to 'public.key' and 'private.key'.")
        
    elif choice == "2":
        src = input("Enter source file path to sign (e.g. lab6_streaming_cipher.py): ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        if not os.path.exists("private.key"):
            print("Private key file missing. Generate keys first.")
            return
            
        with open("private.key", "r") as f:
            d, n = map(int, f.read().split(","))
            
        with open(src, "rb") as f:
            data = f.read()
            
        file_hash = md2_hash(data)
        signature = [pow(b, d, n) for b in file_hash]
        
        sig_path = src + ".sig"
        with open(sig_path, "w") as f:
            f.write(",".join(map(str, signature)))
        print(f"Digital signature created successfully: {sig_path}")
        
    elif choice == "3":
        src = input("Enter original file path: ").strip()
        sig_path = input("Enter signature file path (.sig): ").strip()
        
        if not os.path.exists(src) or not os.path.exists(sig_path):
            print("Files missing.")
            return
            
        if not os.path.exists("public.key"):
            print("Public key file missing.")
            return
            
        with open("public.key", "r") as f:
            e, n = map(int, f.read().split(","))
            
        with open(sig_path, "r") as f:
            signature = list(map(int, f.read().split(",")))
            
        with open(src, "rb") as f:
            data = f.read()
            
        current_hash = md2_hash(data)
        decrypted_hash = bytes([pow(sig_block, e, n) for sig_block in signature])
        
        print(f"Current document hash: {current_hash.hex()}")
        print(f"Decrypted signature hash: {decrypted_hash.hex()}")
        
        if current_hash == decrypted_hash:
            print("VERIFICATION RESULT: SUCCESS (Signature is genuine, file intact)")
        else:
            print("VERIFICATION RESULT: FAILED (Signature mismatch or file modified)")
            
    elif choice == "4":
        sys.exit()

if __name__ == "__main__":
    main()
