import os
import shutil
import json
from accounts.did import DID
from accounts.seed import get_seed
from wallet.address import generate_new_address, get_new_address
from wallet.send_transfer import send
from wallet.transaction import get_txn_info
from credentials.well_form import generate_token_credcredential
from credentials.validation import check_credential_valid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode

list_account = ["d"]
issuer = "c"
holder = "d"

PATH_ACCOUNT = "outputs/"

hash_issuer_did = ""
hash_holder_did = ""

# Create all DID accounts
print("1. Create all DID accounts:" + str(list_account))

for index in range(len(list_account)):
    obj_did = DID(list_account[index])

# c to d
print("2. c to d")

# Issuer ID
with open(PATH_ACCOUNT + issuer + "/did.tangle", "r") as f:
    hash_issuer_did = f.read()

# Receiver ID
with open(PATH_ACCOUNT + holder + "/did.tangle", "r") as f:
    hash_holder_did = f.read()

# Issuer and holder id
obj_issuer = get_txn_info(hash_issuer_did)
obj_holder = get_txn_info(hash_holder_did)

# Get encrypt seed
token_hash = ""
with open(PATH_ACCOUNT + issuer + "/rsa/balance.txt", "r") as f:
    token_hash = f.read()

token_info = get_txn_info(str(token_hash))


# Get private key
private_key_issuer = ""
with open(PATH_ACCOUNT + issuer + "/rsa/private.pem", "r") as f:
    private_key_issuer = f.read()

# Decrypt seed
priv_key_obj = RSA.importKey(private_key_issuer)
cipher = Cipher_PKCS1_v1_5.new(priv_key_obj)
decrypt_text = cipher.decrypt(b64decode(token_info["credentialSubject"]["seed"]), None)

seed =  str(decrypt_text, encoding = "utf-8")


# Channel address
new_addr_issuer = generate_new_address(seed)

# Send
print("3. send token")

cipher_seed = token_info["credentialSubject"]["seed"]

message = generate_token_credcredential(str(obj_issuer["credentialSubject"]["id"]), str(obj_holder["credentialSubject"]["id"]), cipher_seed, str(new_addr_issuer["addresses"][0]))
hash_bundle = send(message, new_addr_issuer["addresses"][0])
print("Bundle " + issuer + " to " + holder + " = " + str(hash_bundle))

print("===================================")

# Verify
print("4. verify on D")
credential_info = get_txn_info(str(hash_bundle))

# Get private key
private_key_holder = ""
with open(PATH_ACCOUNT + holder + "/rsa/private.pem", "r") as f:
    private_key_holder = f.read()

if check_credential_valid(private_key_holder, credential_info["credentialSubject"]["seed"]) == True:
    print("This token is valid!")
else:
    print("This token is invalid!")
