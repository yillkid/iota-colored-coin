from Crypto import Random
from Crypto.PublicKey import RSA

import hashlib
import json
import os
from random import SystemRandom
from wallet.send_transfer import send

PATH_ACCOUNT = "outputs/" 
alphabet = u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class DID():
    def __init__(self, username):
        self.username = username
        # Create DID dir
        if not os.path.exists(PATH_ACCOUNT + username):
            os.mkdir(PATH_ACCOUNT + username)

        # Create seed
        seed = ""
        public_pem = ""
        if not os.path.exists(PATH_ACCOUNT + username + "/" + "seed.txt"):
            generator = SystemRandom()
            seed = u''.join(generator.choice(alphabet) for _ in range(81))
            with open(PATH_ACCOUNT + username + "/" + "seed.txt", 'w') as out_file:
                out_file.write(seed)

        # Check key-pair exist
        if not os.path.exists(PATH_ACCOUNT + username + "/rsa/"):
            os.mkdir(PATH_ACCOUNT + username + "/rsa/")

            # Generate key pair
            random_generator = Random.new().read
            rsa = RSA.generate(1024, random_generator)
            private_pem = rsa.exportKey()
            with open(PATH_ACCOUNT + username + "/rsa/private.pem", "wb") as f:
                f.write(private_pem)

            public_pem = rsa.publickey().exportKey()
            with open(PATH_ACCOUNT + username + "/rsa/public.pem", "wb") as f:
                f.write(public_pem)
        
        # Create DID on Tangle
        content = ""
        boundle = ""
        with open("credentials/did.json", "r") as out_file:
            content = out_file.read()
            s = hashlib.sha256()
            s.update(seed.encode('utf-8'))
            did_id = s.hexdigest()
            content = content.replace("USERID", did_id)
            content = content.replace("PUBKEY", str(public_pem))

            boundle = send(json.loads(content))

        # Write DID URL
        with open(PATH_ACCOUNT + username + "/did.tangle", "w") as f:
                f.write(str(boundle))
