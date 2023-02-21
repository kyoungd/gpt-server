from unittest import mock, TestCase
from messageLog import MessageLog

class TestLogs(TestCase):

    def test_logs_success(self):
        result = MessageLog('gpt-server', 'test_logs', log_message='unit test', log_json={})
        self.assertEqual(result.status_code, 200)

