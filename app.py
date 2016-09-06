#!/usr/bin/env python

import urllib
import json
import os
import random

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print("Request:")
	#print(json.dumps(req, indent=4))

	action  = req.get("result").get('action')

	if action == 'order.pizza_customized':
		print 'aaa'
		res = pizzaToppingCheck(req)
	elif action == 'order.pizza_customized.topping.olives':
		print 'bbb'
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

	context_end_topping = req['result']['contexts'][context_end_index]['parameters']['topping.original']
	topping_olive = req['result']['parameters']['topping']
	para_topping_ext = [i.replace('olives', topping_olive) for i in context_end_topping]
	req['result']['parameters']['topping'] = para_topping_ext
	req['result']['contexts'][context_topping_index]['parameters']['topping'] = para_topping_ext
	req['result']['contexts'][context_add_topping_index]['parameters']['topping'] = para_topping_ext
	#return req
	speech = req['result']['fulfillment']['speech']
	return {
		"speech": speech,
		"displayText": speech,
		#"data": {},
		#"contextOut": [{"name":"asd", "lifespan":1, "parameters":{'topping':para_topping_ext}}],
	}

def pizzaToppingCheck(req):
	result = req.get("result")
	parameters = result.get("parameters")
	contexts = result.get("contexts").append([{"name":"topping-olive", "lifespan":2, "parameters":parameters}])

	if 'topping-half' in parameters:
		topping = parameters['topping-half']
	else:
		topping = parameters.get("topping")

	print topping

	if 'olives' not in topping:
		#return {}
		speech_array = ['Got it, what else today?', 'Okay, got it.']
		speech = speech_array[random.randint(0, 1)]
		return {
			"speech": speech,
			"displayText": speech,
			#"data": {},
		}

	print 'olives' in topping
		
	speech = 'Got it. Green or black olives?'
	print("Response:")
	print(speech)

	return {
		"speech": speech,
		"displayText": speech,
		#"data": {},
		"contextOut": [{"name":"topping-olive", "lifespan":1, "parameters":parameters}],
	}


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print "Starting app on port %d" % port

	app.run(debug=True, port=port, host='0.0.0.0')
