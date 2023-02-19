from unittest import mock, TestCase
from phoneNumber import PhoneNumber

class TestApiCall(TestCase):

    def test_PhoneCheckSuccess_me(self):
        result_0 = PhoneNumber.IsValidNumber('8186793565')
        self.assertTrue(result_0)

    def test_PhoneCheckSuccess_wallgreen(self):
        result_0 = PhoneNumber.IsValidNumber('18183414339')
        self.assertTrue(result_0)

    def test_PhoneCheckFail_wrong_number(self):
        result_0 = PhoneNumber.IsValidNumber('1231231234')
        self.assertFalse(result_0)

    def test_PhoneCheckFail_starts_1(self):
        result_0 = PhoneNumber.IsValidNumber('28186793565')
        self.assertFalse(result_0)

    def test_PhoneCheckFail_eight_digits(self):
        result_0 = PhoneNumber.IsValidNumber('186793565')
        self.assertFalse(result_0)

    def test_PhoneCheckSuccess_string_number(self):
        result_0 = PhoneNumber.IsValidNumber('eight one eight. 679.  three five 69.')
        self.assertTrue(result_0)
