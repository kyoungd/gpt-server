from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput
import json

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

    def test_UpdateStates(self):
        with open("test_UpdateStates_1.json", "r") as json_file:
            replies = json.load(json_file)
            self.state['id'] = 200
            self.globalState.UpdateStates(replies)
            for reply in replies:
                replyBlock = next(obj for obj in self.state['gpt3'] if obj['id'] == reply['id'])
                self.assertEqual(replyBlock['a'], reply['a'])
        # self.assertEqual(result, True)

    def test_Process01(self):
        app1 = ProcessInput()
        data, message = app1.Run()
        print(message)
        r1 = "Hi.  I was involved in a car accient last night."
        app2 = ProcessInput(data)
        data, action = app2.Run(r1)
        # out of the 100 ids, moving to 200 ids.

        app3 = ProcessInput(data)
        data, message = app3.Run()
        print(message)

        r2 = "It was three day ago, at 7:00 PM and John, my brother, was driving home from work. He had been looking forward to getting home to see his family and relax after a long day. He was driving on a busy highway, and traffic was heavy. Suddenly, out of nowhere, a car came speeding into his lane and hit him head-on. John's car spun out of control, and he felt a sharp pain in his chest as his seatbelt tightened. The airbags deployed, and he heard the sound of metal crunching. His car finally came to a stop on the side of the road, and he was trapped inside. He was dazed and confused and could feel the blood running down his face from a cut on his forehead. The other driver was also injured, and he stumbled out of his car. The police arrived shortly after, and the paramedics were called to the scene. John was carefully extracted from his car, and he was rushed to the hospital with serious injuries. He is at the hospital recovering in the hospital with broken ribs, a collapsed lung and head injury with couple of stitches."
        app4 = ProcessInput(data)
        data, action = app4.Run(r2)

        app5 = ProcessInput(data)
        data, message = app4.Run()
        print(message)

        r3 = "My name is James Henford.  That is J A M E S and H E N F O R D."
        app5 = ProcessInput(data)
        data, action = app5.Run(r3)
    
        