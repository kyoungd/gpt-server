from processAction import ProcessAction
from gpt3 import GPT3
from typing import Union
import json
import os
from globalState import GlobalState

class GPT3Call:
    def __init__(self, globalState:GlobalState):
        self._globalState = globalState
        self._state = globalState.state
        self._template = globalState.template
        self._block = globalState.GetTemplateBlock(self._state['id'])
        self._sequence = self._state['sequence']

    def _responseMessage(self):
        prompt = os.getenv("GPT3_RESPONSE_PROMPT")
        # prompt = "If the following statement is simple factual statement without emotion, reply with 'okay'.  Otherwise write a single and simple sympathetic statement as a call center operator to the following statement: "
        if self._globalState.IsRepeatLastQuestion:
            return prompt
        if self._block['is_sympathy_reply']:
            return prompt
        return "Okay"

    ResponseMessage = property(_responseMessage)

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
        prompt = self._block['prompt'] if 'prompt' in self._block else self._template['prompt']
        query = f"{prompt} {gpt3Query}  \"{reply}\" "
        response = GPT3.run(query)
        return response

    def ProcessResponse(self, message):
        gpt3Result = self.callGpt3(message)
        msg = gpt3Result['message'].replace("\n", "")
        reply = json.loads(msg)
        replies = reply if isinstance(reply, list) else [reply]
        self._globalState.UpdateStates(replies, ProcessAction.run, ProcessAction.onError)
        self._globalState.NextId()

    def IsFinishedTalking(self, message):
        pass
