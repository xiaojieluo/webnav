
import unittest
from tests.test_user import TestUser

if __name__ == '__main__':
    suite = unittest.TestSuite()

    tests = [
        TestUser("test_register"),
        TestUser("test_login"),
        TestUser('test_delete'),
        # TestUser("test_")
    ]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
