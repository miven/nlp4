'''
https://www.jianshu.com/p/5e2d3878abb4


区块链单机版本:





调用:



curl "http://localhost:5000/txion"  -d"{\"from\": \"akjflw\", \"to\":\"fjlakdj\", \"amount\": 3}" -H "Content-Type: application/json"


'''

import hashlib as hasher


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) +
                   str(self.timestamp) +
                   str(self.data) +
                   str(self.previous_hash)).encode("utf-8"))
        return sha.hexdigest() # 先uupdate 再digets

import datetime as date

def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), "Genesis Block", "0")


def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = "Hey! I'm block " + str(this_index)
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, this_hash)







# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
# previous_block = blockchain[0]
#
# # How many blocks should we add to the chain
# # after the genesis block
# num_of_blocks_to_add = 20
#
# # Add blocks to the chain
# for i in range(0, num_of_blocks_to_add):
#   block_to_add = next_block(previous_block)
#   blockchain.append(block_to_add)
#   previous_block = block_to_add
#   # Tell everyone about it!
#   print( "Block #{} has been added to the blockchain!".format(block_to_add.index))
#   print ("Hash: {}\n".format(block_to_add.hash) )



import flask

from flask import Flask#导入flask模块用于创建http服务
from flask import request
import json#导入json模块用于表示交易结构
import requests#导入request模块用于响应http请求
import hashlib as hasher#导入hashlib模块用于进行哈希运算
import datetime as date#导入datetime模块用于读取时间
node = Flask(__name__)#启动一个http服务实例



node = Flask(__name__)

# Store the transactions that
# this node has in a list
this_nodes_transactions = []

@node.route('/txion', methods=['POST'])
def transaction():
  if request.method == 'POST':
    # On each new POST request,
    # we extract the transaction data
    new_txion = request.get_json()
    # Then we add the transaction to our list
    this_nodes_transactions.append(new_txion)
    # Because the transaction was successfully
    # submitted, we log it to our console
    print( "New transaction")
    print ("FROM: {}".format(new_txion['from']))
    print ("TO: {}".format(new_txion['to']))
    print( "AMOUNT: {}\n".format(new_txion['amount']))
    # Then we let the client know it worked out
    return "Transaction submission successful\n"














miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

def proof_of_work(last_proof):
  # Create a variable that we will use to find
  # our next proof of work
  incrementor = last_proof + 1
  # Keep incrementing the incrementor until
  # it's equal to a number divisible by 9
  # and the proof of work of the previous
  # block in the chain
  while not (incrementor % 9 == 0 and incrementor % last_proof == 0):# 每一次挖矿计算量至少翻一倍.
    incrementor += 1
  # Once that number is found,
  # we can return it as a proof
  # of our work
  return incrementor



#创建一个区块
@node.route('/mine', methods = ['GET'])
def mine():
  # Get the last proof of work
  last_block = blockchain[len(blockchain) - 1]
  last_proof = last_block.data['proof-of-work']

  proof = proof_of_work(last_proof)

  this_nodes_transactions.append(
    { "from": "network", "to": miner_address, "amount": 1 }
  )

  new_block_data = {
    "proof-of-work": proof,
    "transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = this_timestamp = date.datetime.now()
  last_block_hash = last_block.hash
  # Empty transaction list
  this_nodes_transactions[:] = []
  # Now create the
  # new block!
  mined_block = Block(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  blockchain.append(mined_block)
  # Let the client know we mined a block
  return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "\n"



#

@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain
  for block in chain_to_send:
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    block = {             # 数组里面放的是对象,对象直接修改的是地址.
      "index": block_index,
      "timestamp": block_timestamp,
      "data": block_data,
      "hash": block_hash
    }
  # Send our chain to whomever requested it
  chain_to_send = json.dumps(chain_to_send)
  return chain_to_send

def find_new_chains():
  # Get the blockchains of every
  # other node
  other_chains = []
  peer_nodes=['127.0.0.1']
  for node_url in peer_nodes:
    # Get their chains using a GET request
    block = requests.get(node_url + "/blocks").content
    # Convert the JSON object to a Python dictionary
    block = json.loads(block)
    # Add it to our list
    other_chains.append(block)
  return other_chains

def consensus():
  # Get the blocks from other nodes
  other_chains = find_new_chains()
  # If our chain isn't longest,
  # then we store the longest chain
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  # If the longest chain wasn't ours,
  # then we set our chain to the longest
  blockchain = longest_chain

node.run()