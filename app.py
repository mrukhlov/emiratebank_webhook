#!/usr/bin/env python

import os
import random

from flask import (
    Flask,
    request,
    make_response,
    jsonify
)

app = Flask(__name__)
log = app.logger


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    action = req.get("result").get('action')

    if action == 'transfer.money':
        res = pizzaCountryCheck(req)
    else:
        log.error("Unexpeted action.")

    return pizzaCountryCheck(jsonify(res))

def pizzaCountryCheck(req):

    return {
        "speech": 'aaa',
        "displayText": 'bbb',
        "contextOut": [
            {
                "name": "order-end",
                "lifespan": 1,
                "parameters": {
                    'country': 'test_country'
                }
            }
        ],
    }


'''def pizzaToppingOlives(req):
    contexts = req['result']['contexts']

    order_end_context = None

    for context in contexts:
        if context.get('name') == 'order-end':
            order_end_context = context
            break

    order_end_context_params = order_end_context.get('parameters')

    context_end_topping = None

    if 'topping-half' in order_end_context_params:
        context_end_topping = order_end_context_params['topping-half']
    else:
        context_end_topping = order_end_context_params.get('topping')

    topping_olive = req['result']['parameters']['topping_olive']
    param_topping_ext = [i.replace('olives', topping_olive) for i in context_end_topping]

    speech = req['result']['fulfillment']['speech']

    return {
        "speech": speech,
        "displayText": speech,
        "contextOut": [
            {
                "name": "order-end",
                "lifespan": 1,
                "parameters": {
                    'topping': param_topping_ext
                }
            }
        ],
    }


def pizzaToppingCheck(req):
    result = req.get("result")
    parameters = result.get("parameters")

    if 'topping-half' in parameters:
        topping = parameters['topping-half']
    else:
        topping = parameters.get("topping")

    if 'olives' not in topping:
        speech_array = [
            'Got it, what else today?',
            'Okay, got it. What else today?'
        ]

        speech = random.choice(speech_array)

        return {
            "speech": speech,
            "displayText": speech,
            "contextOut": [
                {
                    "name": "order-end",
                    "lifespan": 1,
                    "parameters": parameters
                }
            ],
        }

    speech = 'Green or black olives?'

    return {
        "speech": speech,
        "displayText": speech,
        "contextOut": [
            {
                "name": "topping-olive",
                "lifespan": 1,
                "parameters": parameters
            }
        ],
    }'''


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    app.run(
        debug=True,
        port=port,
        host='0.0.0.0'
    )
