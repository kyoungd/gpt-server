import json
import re
import requests
from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput
from processAction import ProcessAction
from gpt3Call import GPT3Call

class TestErrorCorrection(TestCase):

    def processQuery(self, data, response, template=None):
        if data is None:
            return ProcessInput.Talk(data, response, template)
        result = ProcessInput.Talk(data, response)
        if result['continue']:
            return ProcessInput.Talk(data)
        return result

    def test_name_or_did_not_say_error(self):
        block = None
        with open('./tests/error-name-or-did-not-say.json', 'r') as f:
            # Load the JSON object
            block = json.load(f)
        reply = block['message']
        result = self.processQuery(block['data'], reply)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 201)

    def test_UpdateStaets(self):
        with open('./tests/error-name-or-did-not-say.json', 'r') as f:
            # Load the JSON object
            block = json.load(f)
        repliesString = '[{"q": "name of the caller", "id": 201, "a": "name or did not say"}, {"q": "phone number", "id": 202, "a": "phone number or did not say"}, {"q": "what is this call about", "id": 203, "a": "detail description of the call or did not say"}]'
        repliesRaw = json.loads(repliesString)
        state = GlobalState(block['data'])
        model = GPT3Call(state)
        replies = model.checkGpt3Hickup(repliesRaw)
        self.assertEqual(replies[0]['a'], 'did not say')

