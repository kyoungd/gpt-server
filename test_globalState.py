from unittest import mock, TestCase
import json
from globalState import GlobalState
from processInput import ProcessInput
from processAction import ProcessAction

class TestGlobalState(TestCase):

    def setUp(self) -> None:
        self.globalState = GlobalState()
        self.state = self.globalState.state
        self.template = self.globalState.template

    def test_initialize(self):
        self.assertEqual(self.state['score'], 0)

    def test_GetTemplateBlock(self):
        self.assertEqual(self.state['id'], 100)
        block = self.globalState.GetTemplateBlock(100)
        self.assertEqual(block['id'], 100)
        self.assertTrue(block['actions'] is not None)

    def test_GetQueries(self):
        self.state['id'] = 100
        query1 = self.globalState.GetQueries("reply")
        self.assertLess(len(query1), 200)
        self.state['id'] = 200
        query2 = self.globalState.GetQueries("replies")
        self.assertGreater(len(query2), 500)

    def test_UpdateStates200(self):
        self.state['id'] = 200
        with open("test_UpdateStates_1.json", "r") as json_file:
            replies = json.load(json_file)
            self.state['id'] = 200
            self.globalState.UpdateStates(replies, ProcessAction.run)
            for reply in replies:
                replyBlock = next(obj for obj in self.state['gpt3'] if obj['id'] == reply['id'])
                self.assertEqual(replyBlock['a'], reply['a'])
            block = self.globalState.GetStateBlock(201)
            self.assertEqual(block['answer_count'], 0)

    def test_UpdateStates201(self):
        self.state['id'] = 201
        reply = [{
            "id": 201,
            "q": "What is your name?",
            "a": "Charlies Schultz"
        }]
        self.globalState.UpdateStates(reply, ProcessAction.run)
        block = self.globalState.GetStateBlock(201)
        self.assertEqual(block['answer_count'], 1)
        self.assertTrue(block['is_answered'])
