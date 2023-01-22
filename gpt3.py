import openai
import os

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class GPT3:
    def __init__(self, prompt = None):
        self._prompt = prompt
        self._response = None

    def get_message(self) -> str:
        if self._response is None:
            return None
        msg = self._response['message'].replace("\n", "").replace("\t", " ")
        return msg

    def get_status_code(self) -> int:
        if self._response is None:
            return None
        return self._response['status_code']

    Message = property(get_message)
    StatusCode = property(get_status_code)    

    def Execute(self):
        try:
            completions = openai.Completion.create(
                engine="text-davinci-002",
                prompt=self._prompt,
                max_tokens=1024,
                n=1,
                temperature=0.5,
            )
            message = completions.choices[0].text
            self._response = {"status_code": 200, "message": message}
            # Return the response as JSON
        except Exception as e:
            self._response = {"status_code": 500, "message": str(e)}
        return self._response

    @staticmethod
    def run(prompt:str):
        gpt3 = GPT3(prompt)
        return gpt3.Execute()
