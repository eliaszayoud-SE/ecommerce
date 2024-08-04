import os
from cryptography.fernet import Fernet

from django.conf import settings


key = os.environ.get("FERNET_KEY")

fernet = Fernet(key)

file_path = os.path.join(settings.BASE_DIR, 'ecommerce-service.json')

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