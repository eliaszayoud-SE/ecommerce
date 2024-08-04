import os
from cryptography.fernet import Fernet

key = os.environ.get("FERNET_KEY")

fernet = Fernet(key)

def decrypt():
    with open('ecommerce-service.json', 'rb') as enc_file:
        encrypted = enc_file.read()
 
    # decrypting the file
    decrypted = fernet.decrypt(encrypted)
    
    # opening the file in write mode and
    # writing the decrypted data
    with open('ecommerce-service.json', 'wb') as dec_file:
        dec_file.write(decrypted)

decrypt()