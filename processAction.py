from phoneNumber import PhoneNumber


class ProcessAction:
    def __init__(self, state, action, answer):
        self._state = state
        self._action = action
        self._answer = answer

    def doMatch(self, answer):
        answers = self._action['answer']
        if answer.strip().lower() in [s.lower() for s in answers]:
            return True
        return False

    def similar (self, answer, one, similarity):
        return True

    def doSimilarity(self, answer, similarity):
        answers = self._actions['answer']
        for one in answers:
            if self.similar(answer, one, similarity):
                return True
        return False

    def doExist(self, answer):
        if answer.strip() == '':
            return False
        return True
    
    def doValidatePhoneNumber(self, answer):
        return PhoneNumber.IsValidNumber(answer)

    def DoOperation(self):
        if self._action['operation'] == 'match':
            return self.doMatch(self._answer)
        if self._action['operation'] == 'similar':
            return self.doSimilarity(self._answer, self._action['similarity'])
        if self._action['operation'] == 'exist':
            return self.doExist(self._answer)
        if self._action['operation'] == 'phone_number':
            return self.doValidatePhoneNumber(self._answer)
        if self._action['operation'] == 'goto':
            return True

    @staticmethod
    def run (state, action, answer):
        processAction = ProcessAction(state, action, answer)
        return processAction.DoOperation()

    @staticmethod
    def onError (globalState, action, answer, id):
        if action['operation'] == 'phone_number':
            if len(PhoneNumber.ExtractNumber(answer)) > 4:
                globalState.AddTranscript("AI", "The phone number seems incorrect.  Once again, and slowly.")
