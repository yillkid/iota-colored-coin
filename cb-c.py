import os
import shutil
import json
from accounts.did import DID
from accounts.seed import get_seed
from wallet.address import generate_new_address, get_new_address
from wallet.send_transfer import send
from wallet.transaction import get_txn_info
from credentials.well_form import generate_token_credcredential
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode

list_account = ["cb", "c"]
issuer = "cb"
holder = "c"

PATH_ACCOUNT = "outputs/"

hash_issuer_did = ""
hash_holder_did = ""

# Create all DID accounts
print("1. Create all DID accounts:" + str(list_account))

# Clear all output files
shutil.rmtree('outputs/')
os.mkdir('outputs/')

for index in range(len(list_account)):
    obj_did = DID(list_account[index])

# CB to c
print("2. cb to c")

# Issuer seed
seed_issuer = get_seed(issuer)

# Issuer ID
with open(PATH_ACCOUNT + issuer + "/did.tangle", "r") as f:
    hash_issuer_did = f.read()

# Receiver ID
with open(PATH_ACCOUNT + holder + "/did.tangle", "r") as f:
    hash_holder_did = f.read()

# Channel address
new_addr_issuer = generate_new_address(seed_issuer)

# Issuer and holder id
obj_issuer = get_txn_info(hash_issuer_did)
obj_holder = get_txn_info(hash_holder_did)

# Holder public key

# Encrypt seed
pub_key =  RSA.importKey(str(obj_holder["credentialSubject"]["publicKeyPem"][2:len(obj_holder["credentialSubject"]["publicKeyPem"])-1]))
cipher = Cipher_PKCS1_v1_5.new(pub_key)
cipher_seed = cipher.encrypt(seed_issuer.encode())

cipher_seed = b64encode(cipher_seed)
cipher_seed = str(cipher_seed, encoding = "utf-8")

message = generate_token_credcredential(str(obj_issuer["credentialSubject"]["id"]), str(obj_holder["credentialSubject"]["id"]), cipher_seed, str(new_addr_issuer["addresses"][0]))

# Send
print("3. send token")
hash_bundle = send(message, new_addr_issuer["addresses"][0])
with open(PATH_ACCOUNT + holder + "/rsa/balance.txt", "w") as f:
    f.write(str(hash_bundle))

print("===================================")
print("Bundle " + issuer + " to " + holder + " = " + str(hash_bundle))
