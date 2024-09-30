from cryptography.fernet import  Fernet
# writing encrytpion key
key = Fernet.generate_key()
f =Fernet(key)
def write_key_toFile():
    with open('keys/key.key', "wb") as file:
       file.write(key)
write_key_toFile()

def encrypt_file(filepath):

    with open(filepath, "rb")as original_file:
        orig =original_file.read()

    encrypted = f.encrypt(orig)

    with open("encrypted_Data/enc_text.txt", "wb")as encrpyt_file:
        encrpyt_file.write(encrypted)

encrypt_file("Original_Data/08 Aug 2024  Dom GERP Download.csv")

# decrpyt the file:
def decrpyt_file():
    with open("keys/key.key", "rb") as f:
        key =f.read()
    f =Fernet(key)

    with open("encrypted_Data/enc_text.txt", "rb")as encrpyt_file:
        encrypted=encrpyt_file.read()

    decrypted = f.decrypt(encrypted)

    with open("decrypted_data/decrypt_text.csv", "wb")as decrcrpyt_file:
        decrcrpyt_file.write(decrypted)

decrpyt_file()