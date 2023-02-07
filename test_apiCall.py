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

    def test_SuccessUrgent(self):
        result_0 = self.process(None, 'hello')
        self.assertIsNotNone(result_0)
        self.assertEqual(result_0['data']['id'], 100)
        self.assertEqual(len(result_0['data']['transcript']), 1)
        data = result_0['data']

        r1 = "Hi.  I was involved in a car accient last night."
        result_1 = self.process(data, r1)
        self.assertIsNotNone(result_1)
        self.assertEqual(result_1['data']['id'], 200)
        self.assertEqual(len(result_1['data']['transcript']), 4)
        data = result_1['data']

        r2 = "It was three day ago, at 7:00 PM and John, my brother, was driving home from work. He had been looking forward to getting home to see his family and relax after a long day. He was driving on a busy highway, and traffic was heavy. Suddenly, out of nowhere, a car came speeding into his lane and hit him head-on. John's car spun out of control, and he felt a sharp pain in his chest as his seatbelt tightened. The airbags deployed, and he heard the sound of metal crunching. His car finally came to a stop on the side of the road, and he was trapped inside. He was dazed and confused and could feel the blood running down his face from a cut on his forehead. The other driver was also injured, and he stumbled out of his car. The police arrived shortly after, and the paramedics were called to the scene. John was carefully extracted from his car, and he was rushed to the hospital with serious injuries. He is at the hospital recovering in the hospital with broken ribs, a collapsed lung and head injury with couple of stitches."
        result_2 = self.process(data, r2)
        self.assertIsNotNone(result_2)
        self.assertEqual(result_2['data']['id'], 201)
        self.assertEqual(len(result_2['data']['transcript']), 7)
        data = result_2['data']

        r3 = "My name is James Henford."
        result_3 = self.process(data, r3)
        self.assertIsNotNone(result_3)
        self.assertEqual(result_3['data']['id'], 202)
        self.assertEqual(len(result_3['data']['transcript']), 10)
        data = result_3['data']

        r4 = "My number is 213-123-1234"
        result_4 = self.process(data, r4)
        self.assertIsNotNone(result_4)
        self.assertEqual(result_4['data']['id'], 206)
        self.assertEqual(len(result_4['data']['transcript']), 13)
        data = result_4['data']

        r5 = "It was at Winnetka and Reseda."
        result_5 = self.process(data, r5)
        self.assertIsNotNone(result_5)
        self.assertEqual(result_5['data']['id'], 208)
        self.assertEqual(len(result_5['data']['transcript']), 16)
        data = result_5['data']

        r6 = "No witness."
        result_6 = self.process(data, r6)
        self.assertIsNotNone(result_6)
        self.assertEqual(result_6['data']['id'], 209)
        self.assertEqual(len(result_6['data']['transcript']), 19)
        data = result_6['data']

        r7 = "It was the other guy."
        result_7 = self.process(data, r7)
        self.assertIsNotNone(result_7)
        self.assertEqual(result_7['data']['id'], 901)
        self.assertEqual(len(result_7['data']['transcript']), 22)

        print('done')

    def test_FailGreetings(self):
        result = self.process(None, 'hello')
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 100)
        self.assertEqual(len(result['data']['transcript']), 1)

        data = result['data']
        r1 = "Hi.  I am in shock.  I am not sure what to do."
        result = self.process(data, r1)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 102)

        data = result['data']
        r1 = "It is a long and winding road.  It is another Universe."
        result = self.process(data, r1)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 909)

        print('done')

    def test_FailNameNotGiven(self):
        result = self.process(None, 'hello')
        result['data']['id'] = 201

        data = result['data']
        r1 = 'I am not sure what you are asking'
        result = self.process(data, r1)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 201)

        data = result['data']
        r2 = 'Can you speak up?'
        result = self.process(data, r2)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 201)

        data = result['data']
        r3 = 'I do not feel like telling you.'
        result = self.process(data, r2)
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['id'], 909)

        print('done')
