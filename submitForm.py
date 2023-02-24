import os
import requests
import json
import re
from globalState import GlobalState
from phoneNumber import PhoneNumber

class SMS:
    def __init__(self, phone_number, message, phone_number_from=None):
        self.phone_number = phone_number
        self.message = message

    def Send(self):
        body = {
            'text': self.message,
            'to': self.phone_number
        }
        result = requests.post(os.getenv("SMS_URL"), json=body)
        return result

    @staticmethod
    def SendSMS(phone_number, message):
        sms = SMS(phone_number, message)
        result = sms.Send()
        return result

class SubmitForm:
    def __init__(self, global_state: GlobalState):
        id = global_state.state['id']
        self.template = global_state.GetTemplateBlock(id)
        self.submits = self.template['submit']
        self.gpt3s = global_state.Gpt3s()

    def extractCallContext(self, gpt3s):
        qas = [x for x in gpt3s if x['is_field'] ]
        results = []
        for qa in qas:
            questionBlock = qa['q']
            answer = qa['a']
            match = re.search(r'\"q\"\s*:\s*\"(.*?)\"', questionBlock)
            question = ''
            if match:
                question = match.group(1)
            results.append(f"{question}:{answer}")
        return ", ".join(results)

    def sendSms(self, gpt3s, block):
        result = None
        try:
            id_phone = block['to']
            phone_number = [x for x in gpt3s if x['id'] == id_phone][0]['a']
            phone = PhoneNumber.ExtractNumber(phone_number)
            message = self.extractCallContext(gpt3s)
            result = SMS.SendSMS(phone, message)
            if os.getenv('SMS_PHONE_ADMIN') is not None:
                phoneTo = os.getenv('SMS_PHONE_ADMIN')
                SMS.SendSMS(phoneTo, message)
            return result
        except Exception as e:
            print(e)
            return result

    def SubmitAll(self):
        blocks = self.submits
        for block in blocks:
            if block['type'] == 'sms':
                self.sendSms(self.gpt3s, block)
                return block
        return None

    @staticmethod
    def Run(global_state: GlobalState):
        submit = SubmitForm(global_state)
        return submit.SubmitAll()
