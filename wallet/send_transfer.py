import json
from iota import Iota, ProposedTransaction, Address, TryteString, Tag, Transaction, ProposedBundle, Hash
from iota.trits import trits_from_int
from wallet.config import SEED, DEPTH, MIN_WEIGHT_MAGNITUDE, NODE

txn_tag = "TXNTAGS"
value = 0
default_receiver_addr = "THE9IOTA9MIXER9999999999999999999999999999999999999999999999999999999999999999999"

def send(message, receiver_addr = default_receiver_addr):
    # Iota instance
    api = Iota(NODE, SEED)

    # Txn description
    txn = ProposedTransaction(
        address = Address(receiver_addr),
        message = TryteString.from_string(json.dumps(message)),
        tag = Tag(txn_tag),
        value = value,
        )

    # Send transaction
    prepared_transferes = []
    bundle = ""
    prepared_transferes.append(txn)
    try:
        bundle = api.send_transfer(
            depth = DEPTH,
            transfers = prepared_transferes,
            min_weight_magnitude = MIN_WEIGHT_MAGNITUDE
        )
    except Exception as e:
        print(e)

    return bundle['bundle'].hash
