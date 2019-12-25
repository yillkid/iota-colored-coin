import json
from iota import Iota, Transaction, TryteString
from wallet.config import NODE

def get_txn_info(hash_boundle):
    api = Iota(NODE)
    dict_txn = api.find_transactions(bundles = [hash_boundle])

    list_txn = api.get_trytes(dict_txn["hashes"])
    trytes_txn = str(list_txn['trytes'][0])
    txn = Transaction.from_tryte_string(trytes_txn)
    message = TryteString(txn.signature_message_fragment).decode()

    return json.loads(message)
