import json
from typing import Union

class GlobalState:
    _pkid: int = 0

    def __init__(self, state: Union[dict, str] = None):
        with open("template_auto_accident.json", "r") as json_file:
            self.template = json.load(json_file)
            if state is None:
                self.state = self._getInitialData(self.template)
                self.state['pkid'] = GlobalState._pkid + 1
                GlobalState._pkid = self.state['pkid']
            else:
                self.state = state if isinstance(state, dict) else json.loads(state)

    def _getInitialData(self, data):
        state = { 
            "pkid": 0,
            "id": self.template['start_id'],
            "sequence": 'q',
            "name": "",
            "phone": "",
            "phone2": "",
            "type": "", 
            "score": 0, 
            "isComplete": False,
            "transcript": "",
            "audioId": 0
        }
        gpt3_responses = []
        for processing in data["processing"]:
            for response in processing["responses"]:
                if len(response["actions"]) > 0:
                    gpt3_responses.append({
                        "id": response["id"],
                        "type": processing["type"],
                        "scope": response["scope"],
                        "q": response["gpt3"],
                        "a": "", 
                        "is_answered":  response["is_neccessary"],
                        "is_neccessary": response["is_neccessary"],
                        "is_field": True
                    })
                else:
                    gpt3_responses.append({
                        "id": response["id"],
                        "type": processing["type"],
                        "is_field": False
                    })
        state['gpt3'] = gpt3_responses
        return state

    def to_json(self):
        return json.dumps(self.state)

    def GetStateBlock(self, id):
        found_object = next((obj for obj in self.state['gpt3'] if obj['id'] == id), None)
        return found_object

    # returns the action block based on the current id
    def GetTemplateBlock(self, id):
        processes = self.template['processing']
        found_object = None
        for process in processes:
            block = process['responses']
            found_object = next((obj for obj in block if obj['id'] == id), None)
            if found_object is not None:
                break
        return found_object

    def GetQueries(self, reply: str):
        block = self.GetTemplateBlock(self.state['id'])
        if block is None:
            return None
        if block["scope"] != 0:
            query = f"{block['prompt']} {block['gpt3']} \"{reply}\" "
            return query
        gpt3s = list(filter(lambda x: x['scope'] == block['id'] and x['is_field'], self.state['gpt3']))
        q_column = [obj['q'] for obj in gpt3s]
        query = f"{block['prompt']} {','.join(q_column)} \"{reply}\" "
        return query

    def UpdateStates(self, replies, func = None):
        gpt3s = self.state['gpt3']
        for reply in replies:
            gpt3 = next((obj for obj in gpt3s if obj['id'] == reply['id']), None)
            if gpt3 is None:
                continue
            gpt3['a'] = reply['a']
            if func is None:
                continue
            id = gpt3['id']
            answer = reply['a']
            self._processActions(id, answer, func)
        return self.state

    def _processActions(self, id, answer, func):
        block = self.GetStateBlock(id)
        template = self.GetTemplateBlock(id)
        for action in template['actions']:
            processAction = func(self.state, action, answer)
            if processAction:
                block['score'] = action['score']
                block['is_answered'] = action['is_answered']
                block['action'] = action
                return processAction
        return None

    def _rateCall(self):
        ratings = self.template['score']
        score = self.Score
        for rating in ratings:
            if score >= rating['score']:
                return rating['rating']
        return None

    def _score(self):
        score = 0
        for gpt3 in self.state['gpt3']:
            score += gpt3['score']
        return score

    def _isNeccessaryAnswered(self):
        for gpt3 in self.state['gpt3']:
            if gpt3['is_neccessary'] and not gpt3['is_answered']:
                return False
        return True
    
    Score = property(_score)
    IsNeccessaryAnswered = property(_isNeccessaryAnswered)
    Rating = property(_rateCall)

    def NextId(self):
        id = self.state['id']
        stateBlock = self.GetStateBlock(id)
        templateBlock = self.GetTemplateBlock(id)
        if stateBlock['type'] == 'extract':
            inqueries = list(filter(lambda x: x['is_field'] and x['id'] >= id and not x['is_answered'], self.state['gpt3']))
            if inqueries and len(inqueries) > 0:
                gpt3s = sorted(inqueries, key=lambda x: x['id'])
                self.state['id'] = gpt3s[0]['id']
            else:
                self.state['id'] = templateBlock['next']
        elif stateBlock['type'] == 'greetings':
            if stateBlock['is_answered']:
                self.state['id'] = stateBlock['action']['next']

    def IsGoodBye(self):
        id = self.state['id']
        stateBlock = self.GetStateBlock(id)
        return stateBlock['type'] == 'goodbye'
