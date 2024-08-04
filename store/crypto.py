import os
from cryptography.fernet import Fernet
from pathlib import Path



key = os.environ.get("FERNET_KEY")

fernet = Fernet(key)

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR + '/store/ecommerce-service.json'

print(file_path)

def decrypt():
    with open(file_path, 'rb') as enc_file:
        encrypted = enc_file.read()
 
    # decrypting the file
    decrypted = fernet.decrypt(encrypted)
    
    # opening the file in write mode and
    # writing the decrypted data
    with open(file_path, 'wb') as dec_file:
        dec_file.write(decrypted)

decrypt()