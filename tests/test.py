import ev3api
import unittest
import json
from unittest.mock import Mock

import sys
sys.modules['ev3dev.core'] = Mock()


class Ev3APITestCase(unittest.TestCase):

    def setUp(self):
        ev3api.app.testing = True
        self.app = ev3api.app.test_client()

    def test_get_motors(self):

        response = self.app.get('/motors')
        print(json.loads(response.data))

if __name__ == '__main__':
    unittest.main()
