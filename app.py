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

    if action == 'order.pizza_customized':
        res = pizzaToppingCheck(req)
    elif action == 'order.pizza_customized.topping.olives':
        res = pizzaToppingOlives(req)
    else:
        log.error("Unexpeted action.")

    return make_response(jsonify(res))


def pizzaToppingOlives(req):
    for i in req['result']['contexts']:
        if i['name'] == 'order-end':
            context_end = i

    context_end_index = req['result']['contexts'].index(context_end)

    if 'topping-half' in req['result']['contexts'][context_end_index]['parameters']:
        context_end_topping = req['result']['contexts'][context_end_index]['parameters']['topping-half']
    elif 'topping' in req['result']['contexts'][context_end_index]['parameters']:
        context_end_topping = req['result']['contexts'][context_end_index]['parameters']['topping']

    topping_olive = req['result']['parameters']['topping']
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
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    app.run(
        debug=True,
        port=port,
        host='0.0.0.0'
    )
