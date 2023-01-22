from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput
from gpt3 import GPT3
import json

class Test_Greetings(TestCase):

    def test_FirstGreetings(self):
        app = ProcessInput()
        data, message = app.Run()
        id = app.GlobalState.state['id']
        block = app.GlobalState.GetTemplateBlock(id)
        self.assertEqual(block['question'], message)

    def test_SecondGreetings(self):
        app = ProcessInput()
        app.Run()
        response = 'I am feeling better but I am still in shock.'
        data, message = app.Run(response)
        prompt1 = app.Gpt3.ResponseMessage
        block = app.GlobalState.GetStateBlock(100)
        self.assertEqual(block['a'], 'did not say')
        self.assertNotEqual(prompt1, "Okay")
        self.assertEqual(app.GlobalState.state['id'], 102)
        prompt2 = f"{prompt1} \"{message} {response}\" "
        gpt3 = GPT3(prompt2)
        gpt3.Execute()
        print(gpt3.Message)

    def test_GreetingsFail(self):
        app = ProcessInput()
        app.Run()
        response = 'I am feeling better but I am still in shock.'
        data, message = app.Run(response)
        prompt1 = app.Gpt3.ResponseMessage
        block = app.GlobalState.GetStateBlock(100)
        self.assertEqual(block['a'], 'did not say')
        self.assertNotEqual(prompt1, "Okay")
        self.assertEqual(app.GlobalState.state['id'], 102)
        data, message = app.Run()
        response = 'Is this the pizzareia'
        data, message = app.Run(response)
        data, message = app.Run()
        self.assertEqual(app.GlobalState.state['id'], 909)

    def test_GreetingsSuccessFirst(self):
        app = ProcessInput()
        app.Run()
        response = 'I got into a bad pile up.'
        data, message = app.Run(response)
        block = app.GlobalState.GetStateBlock(100)
        self.assertEqual(block['a'], 'yes')

    def test_GreetingsSuccessSecond(self):
        app = ProcessInput()
        app.Run()
        response = 'I am still unsure about it.'
        data, message = app.Run(response)
        app.Run()
        response = 'I got into a bad pile up.'
        data, message = app.Run(response)
        block = app.GlobalState.GetStateBlock(102)
        self.assertEqual(block['a'], 'yes')
