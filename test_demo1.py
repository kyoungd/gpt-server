import json
import re
import requests
from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput

class TestDemo1(TestCase):

    def processQuery(self, data, response, template=None):
        if data is None:
            return ProcessInput.Talk(data, response, template)
        result = ProcessInput.Talk(data, response)
        if result['continue']:
            return ProcessInput.Talk(data)
        return result

    def test_demo1(self):
        data = None
        response = ''
        result_1 = self.processQuery(data, response, template="demo_e46ee1013e65")
        self.assertIsNotNone(result_1)
        self.assertEqual(result_1['data']['id'], 200)
        response = 'Hi.  My name is James Crowly.  I am a licensed lawyer in california.  I wanted to talk to you about using your system for my office.  Can you call me?'
        result_2 = self.processQuery(result_1['data'], response)
        self.assertIsNotNone(result_2)
        self.assertEqual(result_2['data']['id'], 202)
        response = 'My number is eight one two, I mean 8 1 8 6 7 9 3 5 6 five.'
        result_3 = self.processQuery(result_2['data'], response)
        self.assertIsNotNone(result_3)
        self.assertEqual(result_3['data']['id'], 901)

    def test_phone_trouble(self):
        data = None
        response = ''
        result_1 = self.processQuery(data, response, template="demo_e46ee1013e65")
        self.assertIsNotNone(result_1)
        self.assertEqual(result_1['data']['id'], 200)
        response = 'Hi.  My name is James Crowly.  I am a licensed lawyer in california.  I wanted to talk to you about using your system for my office.  Can you call me?'
        result_2 = self.processQuery(result_1['data'], response)
        self.assertIsNotNone(result_2)
        self.assertEqual(result_2['data']['id'], 202)
        response = 'My number is eight one two, I mean 8 1 8 6 7 9 3 5.'
        result_3 = self.processQuery(result_2['data'], response)
        self.assertIsNotNone(result_3)
        self.assertEqual(result_3['data']['id'], 202)
        response = 'It is is eight one two, I mean 8 1 8 6 7 9 3 5 six five.'
        result_4 = self.processQuery(result_3['data'], response)
        self.assertIsNotNone(result_3)
        self.assertEqual(result_4['data']['id'], 901)


    def test_demo_step1(self):
        data = None
        with open('./tests/step1.json', 'r') as f:
            # Load the JSON object
            block = json.load(f)
        result = self.processQuery(block['data'], 'Amy, Amy. I am calling you about. Your AI services. And my name is Young faun.')
        self.assertIsNotNone(result)

    def test_demo_step2(self):
        data = None
        with open('./tests/step2.json', 'r') as f:
            # Load the JSON object
            block = json.load(f)
        reply = "Is eight, one, eight. Six, seven, nine. 3565."
        result = self.processQuery(block['data'], reply)
        self.assertIsNotNone(result)

    def test_demo_step3(self):
        block = None
        with open('./tests/step3.json', 'r') as f:
            # Load the JSON object
            block = json.load(f)
        reply = block['message']
        result = self.processQuery(block['data'], reply)
        self.assertIsNotNone(result)

