from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode

def check_credential_valid(holder_private_key, encry_seed):
    # Decrypt seed
    priv_key_obj = RSA.importKey(holder_private_key)
    cipher = Cipher_PKCS1_v1_5.new(priv_key_obj)
    decrypt_text = cipher.decrypt(b64decode(encry_seed), None)
    seed = ""
    try:
        seed = str(decrypt_text, encoding = "utf-8")
    except:
        seed = decrypt_text

    return True
