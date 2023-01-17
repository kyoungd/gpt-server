import json
from typing import Union

class GlobalState:
    _pkid: int = 0

    def __init__(self, state: Union[dict, str] = None):
        with open("template_auto_accident.json", "r") as json_file:
            self.template = json.load(json_file)
            if state is None:
                self.state = self.getInitialData(self.template)
                self.state['pkid'] = GlobalState._pkid + 1
                GlobalState._pkid = self.state['pkid']
            else:
                self.state = state if isinstance(state, dict) else json.loads(state)

    def getInitialData(self, data):
        state = { 
            "pkid": 0,
            "id": self.template['start_id'],
            "sequence": 'q',
            "name": "",
            "phone": "",
            "phone2": "",
            "type": "", 
            "score": 0, 
            "responses": [],
            "isComplete": False,
            "transcript": "",
            "audioId": 0
        }
        gpt3_responses = state['responses']
        for processing in data["processing"]:
            if processing["type"] == "extract":
                for response in processing["responses"]:
                    if len(response["actions"]) > 0:
                        gpt3_responses.append({
                            "id": response["id"],
                            "scope": response["scope"],
                            "q": response["gpt3"],
                            "a": "", 
                            "is_answered": False
                        })
        state['gpt3'] = gpt3_responses
        return state

    def to_json(self):
        return json.dumps(self.state)

    # returns the action block based on the current id
    def GetBlock(self, id):
        processes = self.template['processing']
        found_object = None
        for process in processes:
            block = process['responses']
            found_object = next((obj for obj in block if obj['id'] == id), None)
            if found_object is not None:
                break
        return found_object

    def GetQueries(self, reply: str):
        block = self.GetBlock(self.state['id'])
        if block is None:
            return None
        if block["scope"] != 0:
            query = f"{block['prompt']} {block['gpt3']} \"{reply}\" "
            return query
        gpt3s = list(filter(lambda x: x['scope'] == block['id'], self.state['gpt3']))
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
            self.processActions(id, answer, func)
        return self.state

    def processActions(self, id, answer, func):
        block = self.GetBlock(id)
        for action in block['actions']:
            processAction = func(self.state, action, answer)
            if processAction:
                return processAction
        return None
