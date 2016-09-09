#!/usr/bin/env python

import json
import os
import random
import logging

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
# log = logging.getLogger(__file__)
# log = app.logger


@app.route('/webhook', methods=['POST'])
def webhook():
    app.logger.info("Hello!!!")

    req = request.get_json(silent=True, force=True)

    action = req.get("result").get('action')

    if action == 'order.pizza_customized':
        res = pizzaToppingCheck(req)
    elif action == 'order.pizza_customized.topping.olives':
        res = pizzaToppingOlives(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def pizzaToppingOlives(req):
    for i in req['result']['contexts']:
        if i['name'] == 'order-end':
            context_end = i
        if i['name'] == 'topping-olive':
            context_topping_olive = i
        if i['name'] == 'add-topping':
            context_add_topping = i

    context_end_index = req['result']['contexts'].index(context_end)
    context_topping_index = req['result']['contexts'].index(context_topping_olive)
    context_add_topping_index = req['result']['contexts'].index(context_add_topping)

    if 'topping-half' in req['result']['contexts'][context_end_index]['parameters']:
        context_end_topping = req['result']['contexts'][context_end_index]['parameters']['topping-half']
    elif 'topping' in req['result']['contexts'][context_end_index]['parameters']:
        context_end_topping = req['result']['contexts'][context_end_index]['parameters']['topping']

    topping_olive = req['result']['parameters']['topping_olive']
    para_topping_ext = [i.replace('olives', topping_olive) for i in context_end_topping]

    speech = req['result']['fulfillment']['speech']
    return {
        "speech": speech,
        "displayText": speech,
        "contextOut": [{"name": "order-end", "lifespan": 1, "parameters": {'topping': para_topping_ext}}],
    }


def pizzaToppingCheck(req):
    result = req.get("result")
    parameters = result.get("parameters")
    print parameters

    if 'topping-half' in parameters:
        topping = parameters['topping-half']
    else:
        topping = parameters.get("topping")

    print topping

    if 'olives' not in topping:
        speech_array = ['Got it, what else today?', 'Okay, got it. What else today?']
        speech = speech_array[random.randint(0, len(speech_array) - 1)]
        return {
            "speech": speech,
            "displayText": speech,
            "contextOut": [{"name": "order-end", "lifespan": 1, "parameters": parameters}],
        }

    speech = 'Green or black olives?'

    return {
        "speech": speech,
        "displayText": speech,
        "contextOut": [{"name": "topping-olive", "lifespan": 1, "parameters": parameters}],
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    app.run(debug=True, port=port, host='0.0.0.0')
