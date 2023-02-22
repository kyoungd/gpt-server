from flask import Flask, abort, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from tempfile import NamedTemporaryFile
from io import BytesIO
import base64
import openai
from processInput import ProcessInput
import logging
from messageLog import MessageLog
import traceback
import sys

App = Flask(__name__)
CORS(App)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Starting app')

def getTemplate(block):
    try:
        template = block['template']
        return template
    except Exception as e:
        return None

def getData(block):
    try:
        data = block['data'] if len(block['data'].keys()) > 0 else None
        return data
    except Exception as e:
        return None

def getResponse(block):
    try:
        message = block['message']
        return message
    except Exception as e:
        return None

def processQuery(data, response, template=None):
    if data is None:
        return ProcessInput.Talk(data, response, template)
    result = ProcessInput.Talk(data, response)
    if result['continue']:
        return ProcessInput.Talk(data)
    return result

@App.route('/callcenter', methods=['POST'])
def call():
    try:
        # Parse the request body as JSON
        block = None
        try:
            block = request.get_json()
        except Exception as e:
            block = {}
        MessageLog('gpt-server', 'post /callcenter', log_message='Received request', log_json=block)
        data = getData(block)
        template = getTemplate(block)
        response = getResponse(block)
        result = processQuery(data, response, template)
        return jsonify(result['data'])
    except Exception as e:
        trace = traceback.format_exc()
        MessageLog('gpt-server', 'post /callcenter', log_message=trace, log_json={})
        MessageLog('gpt-server', 'post /callcenter', log_message=str(e), log_json={})
        abort(str(e), 501)
             
@App.route("/gpt3", methods=["POST"])
def gpt3():
    try:
        # Parse the request body as JSON
        data = request.get_json()
        # Get the "question" field from the request body
        question = data["question"]
        prompt = (f"{question}\n")
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            temperature=0.5,
        )
        message = completions.choices[0].text
        # Return the response as JSON
        return jsonify({"status_code": 200, "message": message})
    except Exception as e:
        return jsonify({"status_code": 500, "message": str(e)})

@App.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})

@App.route("/tech-code", methods=["GET"])
def tech_code():
    try:
        # Open the JSON file
        with open("tech-code.json", "r") as f:
            # Load the contents of the file as a Python dictionary
            tech_code_dict = json.load(f)
        # Return the dictionary as JSON
        return jsonify(tech_code_dict)
    except Exception as e:
        return jsonify({"status_code": 500, "message": str(e)})


if __name__ == "__main__":
    App.run()
