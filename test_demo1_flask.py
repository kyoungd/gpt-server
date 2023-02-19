import json
import re
import requests
from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput

class TestDemo1Flask(TestCase):

    def setUp(self):
        self.Url = 'http://localhost:5000'


    # if this causes error, make sure you turn on the flask server
    def test_api_ping(self):
        result = requests.get(self.Url + '/ping')
        self.assertEqual(result.status_code, 200)


    def test_template_accident_demo1(self):
        result_1 = requests.post(self.Url + '/callcenter', json={
            "template": "demo_e46ee1013e65"
        })
        self.assertEqual(result_1.status_code, 200)
        data = result_1.json()
        self.assertIsNotNone(data)
        self.assertRegex(data['message'], r'Talkie')
        self.assertRegex(data['template_file'], r'demo_')
        

    def test_api_template_accident(self):
        result_1 = requests.post(self.Url + '/callcenter')
        self.assertEqual(result_1.status_code, 200)
        data = result_1.json()
        self.assertIsNotNone(data)
        self.assertRegex(data['message'], r'Accident')
        self.assertRegex(data['template_file'], r'accident')
        
