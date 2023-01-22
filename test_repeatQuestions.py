# The caller can only repeat 3 times before the machine hangs up.
from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput
import json

class Test_SympathyAnswer(TestCase):

    def setUp(self) -> None:
        self.globalState = GlobalState()
        self.state = self.globalState.state
        self.template = self.globalState.template

    def setupScore(self, id: int, point: int):
        block = self.globalState.GetStateBlock(id)
        block['score'] = point

    def outcome(self, id: int):
        gpt3s = self.state['gpt3']
        for obj in gpt3s:
            if ('is_answered' in obj) and (obj['id'] < id):
                obj['is_answered'] = True
        obj['answer_count'] = 0
        self.state['id'] = id

    def test_WrongAnswerRepeat(self):
        self.outcome(201)
        self.state['sequence'] = 'a'
        data = self.globalState.to_json()
        app = ProcessInput(data)
        response = 'I am feeling better but I am still in shock.'
        data, _ = app.Run(response)
        prompt = app.Gpt3.ResponseMessage
        self.assertEqual(app.GlobalState.state['id'], 201)
        self.assertNotEqual(prompt, "Okay")
        print(prompt)

    def test_WrongAnswerRepeatEndCall(self):
        self.outcome(201)
        self.state['sequence'] = 'a'
        data = self.globalState.to_json()
        app = ProcessInput(data)
        response = 'I am feeling better but I am still in shock.'
        data, _ = app.Run(response)
        prompt = app.Gpt3.ResponseMessage
        self.assertNotEqual(prompt, "Okay")
        print(prompt)

        data, _ = app.Run()
        response = 'It feels so surreal but I am still not OK.'
        data, _ = app.Run(response)
        prompt = app.Gpt3.ResponseMessage
        self.assertNotEqual(prompt, "Okay")

        data, _ = app.Run()
        response = 'My emotions are all over the place.'
        data, _ = app.Run(response)
        prompt = app.Gpt3.ResponseMessage
        self.assertNotEqual(prompt, "Okay")

        app = ProcessInput(data)
        data, _ = app.Run()
        self.assertTrue(app.GlobalState.IsGoodBye)
