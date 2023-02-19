import json
from typing import Union
from datetime import datetime
import os

class GlobalState:
    _pkid: int = 0

    def __init__(self, state: Union[dict, str] = None, template = None):
        if state is None:
            template_filename = os.getenv("TEMPLATE_FILENAME") if template is None else template + ".json"
            fn = f"templates/{template_filename}"
            with open(fn, "r") as json_file:
                self.template = json.load(json_file)
                self.state = self._getInitialData(self.template)
                self.state['pkid'] = GlobalState._pkid + 1
                GlobalState._pkid = self.state['pkid']
                self.state['template_file'] = fn
        else:
            self.state = state if isinstance(state, dict) else json.loads(state)
            fn = self.state['template_file']
            with open(fn, "r") as json_file:
                self.template = json.load(json_file)

    def _getInitialData(self, data):
        state = { 
            "pkid": 0,
            "id": self.template['start_id'],
            "sequence": 'q',
            "message": '',
            "type": "", 
            "score": 0, 
            "isComplete": False,
            "audioId": 0,
            "transcript": [],
            "template_file": ''
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
                        "speechtimeout": response["speechtimeout"],
                        "reply": response["reply"],
                        "is_answered":  response["is_answered"],
                        "is_neccessary": response["is_neccessary"],
                        "is_sympathy": response["is_sympathy_reply"],
                        "score": 0,
                        "is_field": True,
                        "answer_count": 0
                    })
                else:
                    gpt3_responses.append({
                        "id": response["id"],
                        "type": processing["type"],
                        "speechtimeout": response["speechtimeout"],
                        "reply": response["reply"],
                        "is_sympathy": response["is_sympathy_reply"],
                        "is_field": False,
                        "answer_count": 0
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
        prompt = block['prompt'] if 'prompt' in block else self.template['prompt']
        if block["scope"] != 0:
            query = f"{prompt} {block['gpt3']} \"{reply}\" "
            return query
        gpt3s = list(filter(lambda x: ('scope' in x) and (x['scope'] == block['id']) and x['is_field'], self.state['gpt3']))
        q_column = [obj['q'] for obj in gpt3s]
        query = f"{prompt} {','.join(q_column)} \"{reply}\" "
        return query

    def UpdateStates(self, replies, func = None, onErrorFunc = None):
        gpt3s = self.state['gpt3']
        for reply in replies:
            gpt3 = next((obj for obj in gpt3s if obj['id'] == reply['id']), None)
            if gpt3 is None:
                continue
            gpt3['a'] = reply['a']
            # answer_count should only increase if the question is not extract (open ended question)
            if len(replies) == 1:
                gpt3['answer_count'] += 1
            if func is None:
                continue
            id = gpt3['id']
            answer = reply['a']
            self._processActions(id, answer, func, onErrorFunc)
        return self.state

    def AddTranscript(self, author, message):
        # get current universal datetime
        current_datetime = datetime.utcnow()
        transcript = {
            "datetime": current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "name": author,
            "text": message
        }
        self.state['transcript'].append(transcript)

    def GetLastMessage(self, index = 0):
        # get last message
        last_message = self.state['transcript'][-1 - index]
        return last_message

    def _lastResponse(self):
        transcripts = self.state['transcript']
        last_ai_index = None
        for i in range(len(transcripts)-1, -1, -1):
            if transcripts[i]["name"] != "AI":
                last_ai_index = i
                break
        ai_messages = [msg["text"] for msg in transcripts[last_ai_index:] if msg["name"] == "AI"]
        joined_message = " ".join(ai_messages)
        return joined_message

    LastResponseMessage = property(_lastResponse)

    def _processActions(self, id, answer, func, onErrorFunc = None):
        block = self.GetStateBlock(id)
        template = self.GetTemplateBlock(id)
        for action in template['actions']:
            processAction = func(self.state, action, answer)
            if processAction:
                block['score'] = action['score']
                block['is_answered'] = action['is_answered']
                block['action'] = action
                return processAction
            elif onErrorFunc: 
                onErrorFunc(self, action, answer, id)
        return None

    def _rateCall(self):
        ratings = self.template['rating']
        score = self.Score
        rating = next((obj for obj in ratings if obj['score'] <= self.Score), None)
        return rating

    def _score(self):
        score = 0
        for gpt3 in self.state['gpt3']:
            score += gpt3['score'] if 'score' in gpt3 else 0
        return score

    def _isNeccessaryAnswered(self):
        for gpt3 in self.state['gpt3']:
            if gpt3['is_neccessary'] and not gpt3['is_answered']:
                return False
        return True
    
    def _isSympathy(self):
        id = self.state['id']
        block = self.GetStateBlock(id)
        return block['is_sympathy']

    def _isRepeatLastQuestion(self):
        id = self.state['id']
        block = self.GetStateBlock(id)
        return block['answer_count'] > 0

    def _isGoodBye(self):
        id = self.state['id']
        stateBlock = self.GetStateBlock(id)
        if stateBlock['answer_count'] >= 3:
            return True
        return stateBlock['type'] == 'goodbye'

    Score = property(_score)
    IsNeccessaryAnswered = property(_isNeccessaryAnswered)
    Rating = property(_rateCall)
    IsSympathyReply = property(_isSympathy)
    IsRepeatLastQuestion = property(_isRepeatLastQuestion)
    IsGoodBye = property(_isGoodBye)

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
                id = templateBlock['scope']
                templateBlock = self.GetTemplateBlock(id)
                self.state['id'] = templateBlock['next']
        elif stateBlock['type'] == 'greetings':
            if stateBlock['is_answered']:
                self.state['id'] = stateBlock['action']['next']

