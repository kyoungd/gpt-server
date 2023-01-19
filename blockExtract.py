from processAction import ProcessAction
from gpt3 import GPT3
from typing import Union
import json
from globalState import GlobalState
class BlockExtract:
    def __init__(self, globalState:GlobalState):
        self._globalState = globalState
        self._state = globalState.state
        self._template = globalState.template
        self._block = globalState.GetTemplateBlock(self._state['id'])
        self._sequence = self._state['sequence']

    def Message(self, id, sequence):
        if sequence == 'q':
            found_object = None
            if 'responses' in self._block:
                found_object = next((obj for obj in self._block['responses'] if obj['id'] == id), None)
            else:
                found_object = self._block
        return found_object['question']

    def getGpt3Parse(self):
        if self._block["scope"] != 0:
            return self._block["gpt3"]
        gpt3s = list(filter(lambda x: x['is_field'] and x['scope'] == self._block['id'], self._state['gpt3']))
        q_column = [obj['q'] for obj in gpt3s]
        query = ",".join(q_column)
        return f"[{query}]"

    def callGpt3(self, reply):
        gpt3Query = self.getGpt3Parse()
        query = f"{self._block['prompt']} {gpt3Query}  \"{reply}\" "
        response = GPT3.run(query)
        return response

    def updateState(self, replies):
        gpt3s = self._state['gpt3']
        for reply in replies:
            gpt3 = next((obj for obj in gpt3s if obj['id'] == reply['id']), None)
            if gpt3 is None:
                continue
            gpt3['a'] = reply['a']
        return self._state

    def firstUnanswered(self, replies):
        gpt3s = self._state['gpt3']
        for reply in replies:
            gpt3 = next((obj for obj in gpt3s if obj['id'] == reply['id']), None)
            if gpt3 is None:
                continue
            gpt3['a'] = reply['a']
        return self._state

    def ProcessResponse(self, message):
        gpt3Result = self.callGpt3(message)
        msg = gpt3Result['message'].replace("\n", "")
        reply = json.loads(msg)
        replies = reply if isinstance(reply, list) else [reply]
        self._globalState.UpdateStates(replies, ProcessAction.run)
        self._globalState.NextId()
        # self.updateState(reply if isinstance(reply, list) else [reply])
        # for action in self._block['actions']:
        #     processAction = ProcessAction.run(self._state, action, reply)
        #     if processAction:
        #         self._state['id'] = action['next']
        #         return action
        # return None
