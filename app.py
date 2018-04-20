# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import ssl

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "dblpsearch":
        return {}
    baseurl = "http://ec2-18-217-98-95.us-east-2.compute.amazonaws.com:8080/CloudComputing/article"
    context = ssl._create_unverified_context()
    #result = req.get("result")
    #yql_query = makeYqlQuery(req)
    #if yql_query is None:
    #    return {}
    #yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    #yql_url = requests.post(baseurl, json = req.get("result"))
    #####yql_url = requests.post(baseurl, json = {'id': '76314cf2-1a90-4388-a7f8-f7f786a10827', 'timestamp': '2018-04-17T09:29:01.184Z', 'lang': 'en', 'result': {'source': 'agent', 'resolvedQuery': 'Cloud Computing', 'action': 'DBLPSearch', 'actionIncomplete': False, 'parameters': {'author': ['CS John'], 'title': ['Cloud Computing'], 'year': ['2011'], 'id': ''}, 'contexts': [], 'metadata': {'intentId': '7f288f89-818a-495e-ae25-1ac40e63d564', 'webhookUsed': 'true', 'webhookForSlotFillingUsed': 'false', 'webhookResponseTime': 5035, 'intentName': 'look_for_article'}, 'fulfillment': {'speech': 'We would like to suggest you to read "Cocoa: Dynamic Container-Based Group Buying Strategies for Cloud Computing" from this John C. S. Lui and it is published in 2011.', 'messages': [{'type': 0, 'speech': 'We would like to suggest you to read "Cocoa: Dynamic Container-Based Group Buying Strategies for Cloud Computing" from this  John C. S. Lui and it is published in 2011.'}]}, 'score': 1}, 'status': {'code': 206, 'errorType': 'partial_content', 'errorDetails': 'Webhook call failed. Error: Webhook response was empty.', 'webhookTimedOut': False}, 'sessionId': '67a43021-aac2-4352-a878-ecbf4f612045'})
    #yql_url = requests.post(baseurl,data = {'key':'value'})
    data2 = b'{"id": "d33afbce-baec-4194-b677-55e3a62ffd88", "timestamp": "2018-03-31T12:03:52.095Z", "lang": "en", "result": {"source": "agent", "resolvedQuery": "Cloud Computing", "action": "", "actionIncomplete": False, "parameters": {"authors": ["Anna M. Bianchi"], "title": ["Role of signal"], "year": ["2007"], "id": ""}, "contexts": [], "metadata": {"intentId": "7f288f89-818a-495e-ae25-1ac40e63d564", "webhookUsed": "true", "webhookForSlotFillingUsed": "false", "intentName": "look_for_article"}, "fulfillment": {"speech": "", "messages": [{"type": 0, "speech": ""}]}, "score": 1}, "status": {"code": 200, "errorType": "success", "webhookTimedOut": False}, "sessionId": "4e513bc9-4744-4f63-87d8-68f08f2f33c8"}'
    #data2 = json.dumps(result).encode()
    yql_url = Request(baseurl, data2, headers={'User-agent': 'Mozilla 5.10', 'Content-type': 'application/json', 'Accept': 'application/json'})
    try:
        handler = urlopen(yql_url)
    except HTTPError as e:
        print(e)
    datax = json.loads(handler.read().decode().replace("\\",'')[1:-1])
    #data = "test"
    res = makeWebhookResult(req)
    #return res
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    title = parameters.get("title")
    author = parameters.get("author")
    year = parameters.get("year")

    return {'title' : title, 'author' : author, 'year' : year}


def makeWebhookResult(data):
    #query = data.get('query')
    #if query is None:
    #    return {}

    #result = query.get('results')
    #if result is None:
    #    return {}

    #channel = result.get('channel')
    #if channel is None:
    #    return {}

    #item = channel.get('item')
    #location = channel.get('location')
    #units = channel.get('units')
    #if (location is None) or (item is None) or (units is None):
    #    return {}

    #condition = item.get('condition')
    #if condition is None:
    #    return {}

    # print(json.dumps(item, indent=4))

    #speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
    #         ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    #print("Response:")
    #print(speech)

    return {
        #"speech": speech,
        #"displayText": speech,
        "speech": "",
        #"speech": data['displayText'],
        #"displayText": data['displayText'],
        "displayText" : "",
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
