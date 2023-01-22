# The caller can only repeat 3 times before the machine hangs up.
from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput
import json

class Test_FullCycleQA(TestCase):

    def test_FullCycle1(self):
        app = ProcessInput()

        app.Run()
        r1 = "Hi.  I was involved in a car accient last night."
        app.Run(r1)
        self.assertEqual(app.GlobalState.state['id'], 200)
        self.assertNotEqual(app.Gpt3.ResponseMessage, "Okay")

        app.Run()
        r2 = "It was three day ago, at 7:00 PM and John, my brother, was driving home from work. He had been looking forward to getting home to see his family and relax after a long day. He was driving on a busy highway, and traffic was heavy. Suddenly, out of nowhere, a car came speeding into his lane and hit him head-on. John's car spun out of control, and he felt a sharp pain in his chest as his seatbelt tightened. The airbags deployed, and he heard the sound of metal crunching. His car finally came to a stop on the side of the road, and he was trapped inside. He was dazed and confused and could feel the blood running down his face from a cut on his forehead. The other driver was also injured, and he stumbled out of his car. The police arrived shortly after, and the paramedics were called to the scene. John was carefully extracted from his car, and he was rushed to the hospital with serious injuries. He is at the hospital recovering in the hospital with broken ribs, a collapsed lung and head injury with couple of stitches."
        app.Run(r2)
        self.assertNotEqual(app.Gpt3.ResponseMessage, "Okay")
        self.assertEqual(app.GlobalState.state['id'], 201)
    
        app.Run()
        r3 = "My name is James Henford."
        app.Run(r3)
        self.assertEqual(app.Gpt3.ResponseMessage, "Okay")
        self.assertEqual(app.GlobalState.state['id'], 202)
    
        app.Run()
        r4 = "My number is 213-123-1234"
        app.Run(r4)
        self.assertEqual(app.Gpt3.ResponseMessage, "Okay")
        self.assertEqual(app.GlobalState.state['id'], 206)
    
        app.Run()
        r5 = "It was at Winnetka and Reseda."
        app.Run(r5)
        self.assertEqual(app.Gpt3.ResponseMessage, "Okay")
        self.assertEqual(app.GlobalState.state['id'], 208)
    
        app.Run()
        r6 = "No witness."
        app.Run(r6)
        self.assertEqual(app.Gpt3.ResponseMessage, "Okay")
        self.assertEqual(app.GlobalState.state['id'], 209)
    
        app.Run()
        r7 = "It was the other guy."
        app.Run(r7)
        self.assertEqual(app.Gpt3.ResponseMessage, "Okay")
        self.assertEqual(app.GlobalState.state['id'], 900)

        app.Run()
        self.assertTrue(app.GlobalState.IsGoodBye)
        self.assertEqual(app.GlobalState.state['id'], 901)
