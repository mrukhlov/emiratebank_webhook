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
        res = countryCheck(req)
    elif action == 'transfer.money_service.info':
        res = directRemitYes(req)
    elif action == 'transfer.money_service.info_country':
        res = directRemitCountry(req)
    else:
        log.error("Unexpeted action.")

    return make_response(jsonify(res))

def countryCheck(req):

    speech = req['result']['fulfillment']['speech']
    country = req['result']['parameters']['country']

    country_list_prohibited = ['Iran', 'North Korea']
    country_list_direct = ['India', 'Pakistan', 'Sri Lanka', 'Philippines', 'Egypt']
    if country not in country_list_prohibited + country_list_direct:
        speech = 'You can send money to '+country+' using our international money transfer service. Please refer to the <URL> for more information. Can I help you with something else?'
        contexts = {}
    elif country in country_list_prohibited:
        speech = 'Sorry we are not able to transfer money to '+country+'. Can I help you with something else?'
        contexts = {}
    elif country in country_list_direct:
        speech = 'You can use Direct Remit to transfer money to '+country+'. Would you like to know more?'
        contexts = {
                "name": "service-info",
                "lifespan": 2,
                "parameters": {
                    'country': country
                }
            }

    return {
        "speech": speech,
        "displayText": speech,
        "contextOut": [contexts]
    }

def directRemitYes(req):
    contexts = req['result']['contexts'][0]['parameters']
    speech = 'DirectRemit is free service that allows you to transfer money in 60 seconds. You can ask me more about Direct Remit to ' + contexts['country'] + '.'

    return {
        "speech": speech,
        "displayText": speech
    }

def directRemitCountry(req):
    contexts = req['result']['contexts'][0]['parameters']
    speech = 'You can send a maximum of upto INR 5,000,000 to '+contexts['country']+' for Direct Remit.'

    return {
        "speech": speech,
        "displayText": speech
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    app.run(
        debug=True,
        port=port,
        host='0.0.0.0'
    )
