import requests
import os
import re

class PhoneNumber:
    def __init__(self, number:str):
        self._phoneNumber:str = number
        # extrat only the digits from phone number string
        self._number:str = PhoneNumber.ExtractNumber(number)

    def __str__(self):
        return self._number

    def isValidNumber(self, number:str) -> bool:
        url = os.getenv("NUTRINO_API_URL")
        headers = {
            "User-ID": os.getenv("NUTRINO_USER_ID"),
            "API-KEY": os.getenv("NUTRINO_API_KEY")
        }
        params = {
            "number": number,
            "country-code": 'US'
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['valid']
        else:
            return False

    def IsItValid(self) -> bool:
        if len(self._number) < 9:
            return False
        if len(self._number) > 11:
            return False
        if len(self._number) == 11 and self._number[0] != '1':
            return False
        if len(self._number) == 11:
            self._number = self._number[1:]
        return self.isValidNumber(self._number)
    
    @staticmethod
    def ExtractNumber(number:str) -> str:
        text = number
        # Define a regular expression pattern to match words that represent numbers
        pattern = r'\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b'
        # Use re.findall to extract all matching substrings from the input text
        matches = re.findall(pattern, text)
        # Convert the matches to a string of numbers
        numbers = ''.join([match if match.isnumeric() else str(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'].index(match) + 1) for match in matches])
        return numbers

    @staticmethod
    def IsValidNumber(phoneNumber:str) -> bool:
        pn = PhoneNumber(phoneNumber)
        return pn.IsItValid()
