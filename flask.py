from flask import Flask, request, jsonify
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

@app.route('/score', methods=['POST'])
def score():
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data = {
      "Inputs": {
        "data": [
          {
            "document": "example_value"
          }
        ]
      },
      "GlobalParameters": 1.0
    }

    body = str.encode(json.dumps(data))

    url = 'http://85703749-f0d5-489f-8a7f-724648002ab4.koreacentral.azurecontainer.io/score'
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = ''
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        return jsonify(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return jsonify({'error': 'An error occurred while processing the request'}), 500

if __name__ == '__main__':
    app.run()
