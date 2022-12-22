import openai
import flask
from dotenv import load_dotenv
import os

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

if __name__ == "__main__":
    app.run()
