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

	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	#print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def makeWebhookResult(req):
	result = req.get("result")
	parameters = result.get("parameters")

	if 'topping-half' in parameters:
		topping = parameters['topping-half']
	else:
		topping = parameters.get("topping")

	print topping

	if 'olives' not in topping:
		return {}

	print 'olives' in topping

	'''if req.get("result").get("action") != "order.pizza_customized_black":
		speech = 'black'
	elif req.get("result").get("action") != "order.pizza_customized_green":
		speech = 'green'''
		
	speech = 'Got it. Green or black?'
	print("Response:")
	print(speech)

	return {
		"speech": speech,
		"displayText": speech,
		#"data": {},
		"contextOut": [{"name":"topping-olive", "lifespan":2, "parameters":parameters}],
	}


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print "Starting app on port %d" % port

	app.run(debug=True, port=port, host='0.0.0.0')
