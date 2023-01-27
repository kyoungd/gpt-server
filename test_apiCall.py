from unittest import mock, TestCase
from globalState import GlobalState
from processInput import ProcessInput
import json

class TestApiCall(TestCase):

    def process(self, data, response):
        if data is None:
            return ProcessInput.Talk(data, response)
        result = ProcessInput.Talk(data, response)
        if result['continue']:
            return ProcessInput.Talk(data)
        return result

    def test_InitialHello(self):
        result = self.process(None, 'hello')
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 100)
        self.assertEqual(len(result['data']['transcript']), 1)

        data = result['data']
        r1 = "Hi.  I was involved in a car accient last night."
        result = self.process(data, r1)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 200)
        self.assertEqual(len(result['data']['transcript']), 4)

        data = result['data']
        r2 = "It was three day ago, at 7:00 PM and John, my brother, was driving home from work. He had been looking forward to getting home to see his family and relax after a long day. He was driving on a busy highway, and traffic was heavy. Suddenly, out of nowhere, a car came speeding into his lane and hit him head-on. John's car spun out of control, and he felt a sharp pain in his chest as his seatbelt tightened. The airbags deployed, and he heard the sound of metal crunching. His car finally came to a stop on the side of the road, and he was trapped inside. He was dazed and confused and could feel the blood running down his face from a cut on his forehead. The other driver was also injured, and he stumbled out of his car. The police arrived shortly after, and the paramedics were called to the scene. John was carefully extracted from his car, and he was rushed to the hospital with serious injuries. He is at the hospital recovering in the hospital with broken ribs, a collapsed lung and head injury with couple of stitches."
        result = self.process(data, r2)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 201)
        self.assertEqual(len(result['data']['transcript']), 7)

        data = result['data']
        r3 = "My name is James Henford."
        result = self.process(data, r3)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 202)
        self.assertEqual(len(result['data']['transcript']), 10)

        data = result['data']
        r4 = "My number is 213-123-1234"
        result = self.process(data, r4)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 206)
        self.assertEqual(len(result['data']['transcript']), 13)

        data = result['data']
        r5 = "It was at Winnetka and Reseda."
        result = self.process(data, r5)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 208)
        self.assertEqual(len(result['data']['transcript']), 16)

        data = result['data']
        r6 = "No witness."
        result = self.process(data, r6)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 209)
        self.assertEqual(len(result['data']['transcript']), 19)

        data = result['data']
        r7 = "It was the other guy."
        result = self.process(data, r7)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 901)
        self.assertEqual(len(result['data']['transcript']), 22)

        print('done')
