import json
from blockExtract import BlockExtract
from typing import Union
from globalState import GlobalState

class ProcessInput:
    _pkid: int = 0

    def __init__(self, trackCall: Union[dict, str] = None):
        self._system = GlobalState(trackCall)
        self.State = self._system.state
        self.Template = self._system.template


    def is_goodbye(self):
        return self._system.IsGoodBye()

    IsGoodBye = property(is_goodbye)

    # this returns a main question of the each response block
    def handleTalk(self):
        app = BlockExtract(self._system)
        if self.IsGoodBye:
            rating = self._system.Rating;
            return rating['statement']
        message = app.Message(self.State['id'], self.State['sequence'])
        return message

    # this handles the response from the user
    def handleResponse(self, response):
        app = BlockExtract(self._system)
        app.ProcessResponse(response)

    def Main(self, response = None):
        if self.State['sequence'] == 'q':
            message = self.handleTalk()
            self.State['sequence'] = 'a' if self.State['sequence'] == 'q' else 'q'
            return self.State, message
        if self.State['sequence'] == 'a':
            self.handleResponse(response)
            self.State['sequence'] = 'a' if self.State['sequence'] == 'q' else 'q'
            return self.State, "OK"

    @staticmethod
    def Run(data = None, userResponse = None):
        app = ProcessInput(data)
        return app.Main(userResponse)


if __name__ == "__main__":
    data = None
    while True:
        app = ProcessInput(data)
        data, message = app.Main(data)
        print(message)
        if app.IsGoodBye:
            print(message)
            break
        response = input(message)
        data, message = ProcessInput.Run(data, response)
        print(message)

    # data, message = ProcessInput.Run()
    # print(message)
    # r1 = "Hi.  I was involved in a car accient last night."
    # data, message = ProcessInput.Run(data, r1)
    # # out of the 100 ids, moving to 200 ids.

    # data, message = ProcessInput.Run(data)
    # print(message)
    # r2 = "It was three day ago, at 7:00 PM and John, my brother, was driving home from work. He had been looking forward to getting home to see his family and relax after a long day. He was driving on a busy highway, and traffic was heavy. Suddenly, out of nowhere, a car came speeding into his lane and hit him head-on. John's car spun out of control, and he felt a sharp pain in his chest as his seatbelt tightened. The airbags deployed, and he heard the sound of metal crunching. His car finally came to a stop on the side of the road, and he was trapped inside. He was dazed and confused and could feel the blood running down his face from a cut on his forehead. The other driver was also injured, and he stumbled out of his car. The police arrived shortly after, and the paramedics were called to the scene. John was carefully extracted from his car, and he was rushed to the hospital with serious injuries. He is at the hospital recovering in the hospital with broken ribs, a collapsed lung and head injury with couple of stitches."
    # data, action = ProcessInput.Run(data, r2)

    # data, message = ProcessInput.Run(data)
    # print(message)
    # r3 = "My name is Young Kwon."
    # data, action = ProcessInput.Run(data, r3)

    # data, message = ProcessInput.Run(data)
    # print(message)
    # r4 = "My phone number is 818-679-3565."
    # data, action = ProcessInput.Run(data, r4)

    # data, message = ProcessInput.Run(data)
    # print(message)
    # r5 = "It was at Northridge and Reseda."
    # data, action = ProcessInput.Run(data, r5)

    # print(message)
