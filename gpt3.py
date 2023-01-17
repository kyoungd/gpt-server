import openai
import os

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class GPT3:
    def __init__(self, prompt = None):
        self._prompt = prompt

    def get_prompt(self):
        return self._prompt

    def set_prompt(self, prompt):
        self._prompt = prompt

    prompt = property(get_prompt, set_prompt)

    def get_response(self):
        try:
            completions = openai.Completion.create(
                engine="text-davinci-002",
                prompt=self._prompt,
                max_tokens=1024,
                n=1,
                temperature=0.5,
            )
            message = completions.choices[0].text
            return {"status_code": 200, "message": message}
            # Return the response as JSON
        except Exception as e:
            return {"status_code": 500, "message": str(e)}

    @staticmethod
    def run(prompt:str):
        gpt3 = GPT3(prompt)
        return gpt3.get_response()
