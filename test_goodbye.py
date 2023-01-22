from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput
import json

class TestGoodBye(TestCase):

    def setUp(self) -> None:
        self.globalState = GlobalState()
        self.state = self.globalState.state
        self.template = self.globalState.template

    def setupScore(self, id, point):
        block = self.globalState.GetStateBlock(id)
        block['score'] = point

    def outcome(self):
        gpt3s = self.state['gpt3']
        for obj in gpt3s:
            if 'is_answered' in obj:
                obj['is_answered'] = True
        self.setupScore(201, 500)
        self.setupScore(202, 500)
        self.state['id'] = 900

    def test_goodbye1(self):
        self.outcome()
        self.setupScore(203, 200)
        self.setupScore(204, 100)
        data = self.globalState.to_json()
        app = ProcessInput(data)
        data, message = app.Run()
        message901 = next(obj for obj in self.template['rating'] if obj['id'] == 901)['statement']
        self.assertEqual(message, message901)

    def test_goodbye2(self):
        self.outcome()
        self.setupScore(203, 0)
        self.setupScore(204, 100)
        self.setupScore(205, 1)
        data = self.globalState.to_json()
        app = ProcessInput(data)
        data, message = app.Run()
        message902 = next(obj for obj in self.template['rating'] if obj['id'] == 902)['statement']
        self.assertEqual(message, message902)

    def test_goodbye3(self):
        self.outcome()
        self.setupScore(205, 1)
        data = self.globalState.to_json()
        app = ProcessInput(data)
        data, message = app.Run()
        message903 = next(obj for obj in self.template['rating'] if obj['id'] == 903)['statement']
        self.assertEqual(message, message903)
