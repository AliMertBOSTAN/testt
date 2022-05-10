from solcx import compile_standard, install_solc
import json
from web3 import Web3, EthereumTesterProvider
import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

with open(
    "/home/proven/Desktop/Blockchain_test/web3_py_simple_storage/SimpleStorage.sol", "r"
) as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# print(compiled_sol)

with open("compiled-code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/45db24eec99348cd9d5066701155a9e7")
)
chain_id = 4
my_address = "0xe35Dd8D3fbe83F54fA3a3d0E202F5a4Ec53fc7C5"
private_key = ""
print(private_key)


SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(f"Kayıtlı veri, {simple_storage.functions.retrieve().call()}")

# kayıtlı veriyi değiştirme ve imzalama
greeting_transaction = simple_storage.functions.addPerson("selam", 0).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
