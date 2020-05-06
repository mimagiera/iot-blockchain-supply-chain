import datetime
import json
import time

import requests
from flask import render_template, redirect, request

from app import app
from app.model import *

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
                           title='Smart manufacturing PoC',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    c_factory_id = request.form["current_factory_id"]
    d_factory_id = request.form["destination_factory_id"]
    product = request.form["product"]
    number_of_parts_to_produce = request.form["number_of_parts_to_produce"]
    product_schema = request.form["product_schema"]

    if product not in ProductType.__members__:
        return redirect("/")

    product_description = ProductDescription(json.dumps(ProductType[product].value), product_schema,
                                             number_of_parts_to_produce)

    my_data = OrderDescription([json.dumps(product_description.__dict__)], time.time(),
                               str(c_factory_id), str(d_factory_id))

    post_object = {
        'product': product,
        'my_data': json.dumps(my_data.__dict__)
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
