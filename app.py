#!/usr/bin/env python

import urllib
import json
import os

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

	if req.get('action') != 'order.pizza_customized.topping.olives':
		res = pizzaToppingCheck(req)
	else:
		res = pizzaToppingOlives(req)

	res = json.dumps(res, indent=4)
	#print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def pizzaToppingOlives(req):
	print req

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
		return {}

	print 'olives' in topping
		
	speech = 'Got it. Green or black olives?'
	print("Response:")
	print(speech)

	return {
		"speech": speech,
		"displayText": speech,
		#"data": {},
		"contextOut": contexts,
	}


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print "Starting app on port %d" % port

	app.run(debug=True, port=port, host='0.0.0.0')
