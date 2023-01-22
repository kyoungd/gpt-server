import json
from gpt3Call import GPT3Call
from typing import Union
from globalState import GlobalState
from gpt3 import GPT3

class ProcessInput:
    _pkid: int = 0

    def __init__(self, trackCall: Union[dict, str] = None):
        self._system = GlobalState(trackCall)
        self._gpt3 = None

    def get_globalState(self):
        return self._system

    def get_gpt3(self):
        return self._gpt3

    GlobalState = property(get_globalState)
    Gpt3 = property(get_gpt3)

    # this returns a main question of the each response block
    def handleTalk(self):
        if self._system.IsGoodBye:
            rating = self._system.Rating
            self.GlobalState.state['id'] = rating['id']
            return rating['statement']
        self._gpt3 = GPT3Call(self._system)
        message = self._gpt3.Message(self._system.state['id'], self._system.state['sequence'])
        return message

    # this handles the response from the user
    def handleResponse(self, response):
        self._gpt3 = GPT3Call(self._system)
        self._gpt3.ProcessResponse(response)

    def Run(self, response = None):
        if self._system.state['sequence'] == 'q':
            message = self.handleTalk()
            self._system.state['sequence'] = 'a' if self._system.state['sequence'] == 'q' else 'q'
            return self._system.state, message
        if self._system.state['sequence'] == 'a':
            self.handleResponse(response)
            self._system.state['sequence'] = 'a' if self._system.state['sequence'] == 'q' else 'q'
            return self._system.state, "OK"


if __name__ == "__main__":
    data = None
    while True:
        app1 = ProcessInput(data)
        data, message1 = app1.Run()
        if app1.GlobalState.IsGoodBye:
            print(message1)
            break
        print('-----------------')
        response = input(message1 + "  ")
        app2 = ProcessInput(data)
        data, message2 = app2.Run(response)
        prompt1 = app2.Gpt3.ResponseMessage
        if prompt1 == "Okay":
            print(message2)
            continue
        prompt2 = f"{prompt1} \"{message1} {response}\" "
        gpt3 = GPT3(prompt2)
        gpt3.Execute()
        print(gpt3.Message.split(',')[0])
