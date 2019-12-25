from iota import Iota
from wallet.config import NODE

def generate_new_address(seed):
    api = Iota(NODE, seed)
    return api.get_new_addresses(count = None, index = None)

def get_new_address(issuer):
    pass

def check_valid(address):
    pass
