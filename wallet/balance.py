from iota import Iota
from wallet.config import NODE

def get_account_data(seed):
    api = Iota(NODE, seed)
    return api.get_account_data()
