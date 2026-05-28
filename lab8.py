import os
import sys

def embed_message(bmp_data, text_message):
    message_bytes = text_message.encode('utf-8') + b'\x00'
    binary_message = ""
    for byte in message_bytes:
        binary_message += f"{byte:08b}"
        
    header_size = int.from_bytes(bmp_data[10:14], byteorder='little')
    pixel_data = bytearray(bmp_data[header_size:])
    
    if len(binary_message) > len(pixel_data):
        print("Error: Message is too large for this image layer size.")
        return None
        
    for i in range(len(binary_message)):
        bit = int(binary_message[i])
        pixel_data[i] = (pixel_data[i] & 0xFE) | bit
        
    return bmp_data[:header_size] + bytes(pixel_data)

def extract_message(bmp_data):
    header_size = int.from_bytes(bmp_data[10:14], byteorder='little')
    pixel_data = bmp_data[header_size:]
    
    binary_message = ""
    for i in range(len(pixel_data)):
        binary_message += str(pixel_data[i] & 1)
        
    message_bytes = bytearray()
    for i in range(0, len(binary_message), 8):
        byte_str = binary_message[i:i+8]
        if len(byte_str) < 8:
            break
        byte_val = int(byte_str, 2)
        if byte_val == 0:
            break
        message_bytes.append(byte_val)
        
    try:
        return message_bytes.decode('utf-8')
    except:
        return "[Error] Extracted binary structure is corrupted or has no valid signature."

def create_dummy_bmp():
    pixel_data_size = 4000
    file_size = 54 + pixel_data_size
    
    header = bytearray(54)
    header[0:2] = b'BM'
    header[2:6] = file_size.to_bytes(4, byteorder='little')
    header[10:14] = (54).to_bytes(4, byteorder='little')
    header[14:18] = (40).to_bytes(4, byteorder='little')
    header[18:22] = (30).to_bytes(4, byteorder='little')
    header[22:26] = (30).to_bytes(4, byteorder='little')
    header[26:28] = (1).to_bytes(2, byteorder='little')
    header[28:30] = (24).to_bytes(2, byteorder='little')
    header[34:38] = pixel_data_size.to_bytes(4, byteorder='little')
    
    pixels = bytearray([128] * pixel_data_size)
    return bytes(header + pixels)

def main():
    print("--- STEGANOGRAPHIC DATA HIDING UTILITY (LSB) ---")
    print("1. Create placeholder carrier image (container.bmp)")
    print("2. Hide message in image")
    print("3. Extract hidden message from image")
    print("4. Exit")
    
    choice = input("Select action: ").strip()
    
    if choice == "1":
        bmp = create_dummy_bmp()
        with open("container.bmp", "wb") as f:
            f.write(bmp)
        print("Carrier bitmap file generated successfully as 'container.bmp'.")
        
    elif choice == "2":
        src = input("Enter container image path (e.g. container.bmp): ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        message = input("Enter secret message string to embed: ").strip()
        
        with open(src, "rb") as f:
            bmp_data = f.read()
            
        stego_data = embed_message(bmp_data, message)
        if stego_data:
            dst = src.replace(".bmp", "_encoded.bmp")
            with open(dst, "wb") as f:
                f.write(stego_data)
            print(f"Message hidden successfully. Saved payload container to: {dst}")
            
    elif choice == "3":
        src = input("Enter encoded container image path: ").strip()
        if not os.path.exists(src):
            print("File not found.")
            return
            
        with open(src, "rb") as f:
            bmp_data = f.read()
            
        extracted = extract_message(bmp_data)
        print(f"\nExtracted Hidden Payload:\n{extracted}")
        
    elif choice == "4":
        sys.exit()

if __name__ == "__main__":
    main()
