import openai
import flask
from dotenv import load_dotenv
import os
import json

app = flask.Flask(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/gpt3", methods=["POST"])
def gpt3():

    # Parse the request body as JSON
    data = flask.request.get_json()

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
    return flask.jsonify({"message": message})

@app.route("/ping", methods=["GET"])
def ping():
    return flask.jsonify({"message": "pong"})

@app.route("/tech-code", methods=["GET"])
def tech_code():
    # Open the JSON file
    with open("tech-code.json", "r") as f:
        # Load the contents of the file as a Python dictionary
        tech_code_dict = json.load(f)

    # Return the dictionary as JSON
    return flask.jsonify(tech_code_dict)

if __name__ == "__main__":
    app.run()
