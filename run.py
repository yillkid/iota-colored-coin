import os
import shutil
import json
from accounts.did import DID
from accounts.seed import get_seed
from wallet.address import generate_new_address, get_new_address
from wallet.send_transfer import send

list_account = ["cb", "a", "b", "c", "d", "e", "f"]

# Create all DID accounts
print("1. Create all DID accounts:" + str(list_account))

# Clear all output files
shutil.rmtree('outputs/')
os.mkdir('outputs/')

for index in range(len(list_account)):
    obj_did = DID(list_account[index])

# CB to a, b, c
print("2. cb to a, b, c")
list_holder = ["a", "b", "c"]

seed_cb = get_seed("cb")

for obj in list_holder:
    new_addr_cb = generate_new_address(seed_cb)
    message = {"issuer":"cb","holder":obj}
    hash_bundle = send(message, new_addr_cb["addresses"][0])

    print("Bundle cb to " + obj + " = " + str(hash_bundle))

# c to d
print("3. c to d")
list_holder = ["d"]
for obj in list_holder:
    # Get new address from cb
    address = get_new_address("cb")
    # Send token
    pass

# Check valid to c and d
# c: valid
# d: invalid

# Create new branch from d
