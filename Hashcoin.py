#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 00:21:25 2018

@author: Dibyo
"""

# To be Installed
# Flask == 0.12.2 : pip install Flask 
# Postman HTTP Client
# requests

# Create a Cryptocurrency Hashcoin


# importing all the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 -  Building a Blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions' : self.transactions
                 }
        self.transactions = []
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if(hash_operation[:4] == '0000' ):
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True
    
    def add_transactions(self, sender, reciever, amount):
        self.transactions.append({'sender': sender,
                                  'reciever': reciever,
                                  'amoiunt': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
        
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        for nodes in network:
            response = requests.get('{}/get_chain')
# Part 2 -  Mining your Blockchain 
            

# Creating the web app 
app = Flask(__name__)

# Creating the Blockchain
blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof =  previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Congrats , you just mined a block ! and you block will be added in the blockchain',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Checking if the blockchain is valid
    
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if(is_valid == True):
        response = {'message' : 'all good the blockchain is valid'}
    else:
        response = {'message' : 'blockchain is not valid tmkb'}
    return jsonify(response), 200


# Getting the Full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response),200    

# Part 3 - Decentralizing our blockchain

# Running the app 
app.run(host = '0.0.0.0', port = 5000)