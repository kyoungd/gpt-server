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

    # this returns a main question of the each response block
    def handleTalk(self):
        app = BlockExtract(self._system)
        message = app.Message(self.State['id'], self.State['sequence'])
        return message

    # this handles the response from the user
    def handleResponse(self, response):
        app = BlockExtract(self._system)
        action = app.ProcessResponse(response)
        self.State['id'] = action['next']
        return action

    def Run(self, response = None):
        if self.State['sequence'] == 'q':
            message = self.handleTalk()
            self.State['sequence'] = 'a' if self.State['sequence'] == 'q' else 'q'
            return self.State, message 
        if self.State['sequence'] == 'a':
            response = self.handleResponse(response)
            self.State['sequence'] = 'a' if self.State['sequence'] == 'q' else 'q'
            return self.State, response

if __name__ == "__main__":
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
