import os
import sys

def compress_rle(data_str):
    if not data_str:
        return ""
    res = []
    count = 1
    char = data_str[0]
    for i in range(1, len(data_str)):
        if data_str[i] == char:
            count += 1
        else:
            res.append(f"{char}{count}")
            char = data_str[i]
            count = 1
    res.append(f"{char}{count}")
    return "|".join(res)

def decompress_rle(compressed_str):
    if not compressed_str:
        return ""
    res = []
    parts = compressed_str.split("|")
    for part in parts:
        if not part:
            continue
        char = part[0]
        count = int(part[1:])
        res.append(char * count)
    return "".join(res)

def main():
    print("--- DATA COMPRESSION UTILITY (RLE) ---")
    print("1. Compress file")
    print("2. Decompress file")
    print("3. Exit")
    
    choice = input("Select action: ").strip()
    
    if choice == "1":
        src = input("Enter source file path (e.g. lab1_2_security.py): ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
            
        compressed = compress_rle(content)
        dst = src + ".rle"
        
        with open(dst, "w", encoding="utf-8") as f:
            f.write(compressed)
            
        orig_size = os.path.getsize(src)
        comp_size = os.path.getsize(dst)
        
        ratio = (1 - (comp_size / orig_size)) * 100 if orig_size > 0 else 0
        
        print(f"File compressed successfully: {dst}")
        print(f"Original size: {orig_size} bytes")
        print(f"Compressed size: {comp_size} bytes")
        print(f"Compression ratio: {ratio:.2f}%")
        
    elif choice == "2":
        src = input("Enter compressed file path (.rle): ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()
            
        decompressed = decompress_rle(content)
        dst = src.replace(".rle", "_restored.py")
        
        with open(dst, "w", encoding="utf-8") as f:
            f.write(decompressed)
            
        print(f"File decompressed successfully: {dst}")
        
    elif choice == "3":
        sys.exit()

if __name__ == "__main__":
    main()
