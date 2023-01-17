from unittest import mock, TestCase
from globalState import GlobalState
import json

class TestGlobalState(TestCase):

    def setUp(self) -> None:
        self.globalState = GlobalState()
        self.state = self.globalState.state
        self.template = self.globalState.template

    def test_initialize(self):
        self.assertEqual(self.state['score'], 0)

    def test_GetBlock(self):
        self.assertEqual(self.state['id'], 100)
        block = self.globalState.GetBlock(100)
        self.assertEqual(block['id'], 100)
        self.assertTrue(block['actions'] is not None)

    def test_GetQueries(self):
        self.state['id'] = 100
        query1 = self.globalState.GetQueries("reply")
        self.assertLess(len(query1), 200)
        self.state['id'] = 200
        query2 = self.globalState.GetQueries("replies")
        self.assertGreater(len(query2), 500)

    def test_UpdateStates(self):
        with open("test_UpdateStates_1.json", "r") as json_file:
            message = json.load(json_file)
        message = '{\t"q": "name of the caller",\t"id": 201,\t"a": "did not say"},{\t"q": "was there injury",\t"id": 203,\t"a": "severe"},{\t"q": "was there death",\t"id": 204,\t"a": "no"},{\t"q": "was there pain",\t"id": 205,\t"a": "severe"},{\t"q": "location of the accident?",\t"id": 206,\t"a": "did not say"},{\t"q": "when was the accident",\t"id": 207,\t"a": "date"},{\t"q": "is there a witness",\t"id": 208,\t"a": "no"},{\t"q": "whos fault is it?",\t"id": 209,\t"a": "did not say"},{\t"q": "phone number",\t"id": 212,\t"a": "did not say"}'
        replies = json.loads(message)

        pass
        # self.assertEqual(result, True)
