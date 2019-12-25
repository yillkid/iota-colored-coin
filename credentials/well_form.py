import json

def generate_token_credcredential(id_issuer, id_holder, cipher_seed, new_addr_issuer):
    content = ""
    with open("credentials/token.json", "r") as out_file:
        content = out_file.read()
        content = content.replace("ISSUERID", id_issuer)
        content = content.replace("RECEIVERID", id_holder)
        content = content.replace("SEED", cipher_seed)
        content = content.replace("ADDRESS", new_addr_issuer)

    return json.loads(content)
