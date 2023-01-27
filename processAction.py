import spacy

nlp = spacy.load("en_core_web_md")

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

    def DoOperation(self):
        if self._action['operation'] == 'match':
            return self.doMatch(self._answer)
        if self._action['operation'] == 'similar':
            return self.doSimilarity(self._answer, self._action['similarity'])
        if self._action['operation'] == 'exist':
            return self.doExist(self._answer)
        if self._action['operation'] == 'goto':
            return True

    @staticmethod
    def run (state, action, answer):
        processAction = ProcessAction(state, action, answer)
        return processAction.DoOperation()
