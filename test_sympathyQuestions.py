# test questions where there should be a sympathatic response.
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

    # the question is "what i your name".  It tests for not answering the question.
    # it should answer with a sympathetic answer.
    def test_WrongAnswerSympthyOn(self):
        self.outcome(201)
        self.state['sequence'] = 'a'
        data = self.globalState.to_json()
        app = ProcessInput(data)
        response = 'I am feeling better but I am still in shock.'
        data, message = app.Run(response)
        prompt = app.Gpt3.ResponseMessage
        self.assertNotEqual(prompt, "Okay")
        print(prompt)

    def test_RightAnswerSympathyOff(self):
        self.outcome(201)
        self.state['sequence'] = 'a'
        data = self.globalState.to_json()
        app = ProcessInput(data)
        response = 'My name is Charlies Bond.'
        data, message = app.Run(response)
        prompt = app.Gpt3.ResponseMessage
        self.assertEqual(prompt, "Okay")
        print(prompt)

    def test_AnyAnswerSympathyOnForExtract(self):
        self.outcome(200)
        self.state['sequence'] = 'a'
        data = self.globalState.to_json()
        app = ProcessInput(data)
        response = 'I am feeling better but I am still in shock.'
        data, message = app.Run(response)
        prompt = app.Gpt3.ResponseMessage
        self.assertNotEqual(prompt, "Okay")
        print(prompt)

    def test_RightAnswerSympathyOn(self):
        self.outcome(203)
        self.state['sequence'] = 'a'
        data = self.globalState.to_json()
        app = ProcessInput(data)
        response = 'I cracked my back and my arm is broken.  I need to be hospitalized for 2 weeks.'
        data, message = app.Run(response)
        prompt = app.Gpt3.ResponseMessage
        self.assertNotEqual(prompt, "Okay")
        print(prompt)
