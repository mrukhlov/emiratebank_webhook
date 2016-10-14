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
    elif action == 'support.transfer.amount':
        res = directRemitCountryAmount(req)
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
                "lifespan": 3,
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

def directRemitCountryAmount(req):
    quantity = req['result']['parameters']['amount']

    if quantity == 'max':
        speech = 'Your Segment limit applicable for DirectRemit to India is detailed below:\n\n- Personal Banking AED 200,000\n- Private Banking AED 500,000\nThe maximum remittance amount for DirectRemit to Philippines is PHP 500,000 per transaction across segments. The maximum remittance for DirectRemit to Pakistan is PKR 500,000 per transaction across segments. The maximum remittance for DirectRemit to Sri Lanka is LKR 1,000,000 per transaction across segments. The maximum remittance for DirectRemit to Egypt is EGP 100,000 per transaction across segments'
    elif quantity == 'min':
        speech = 'An equivalent of AED 100 in the respective home currency is the minimum amount that can be transferred via DirectRemit.'

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
