import sys
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    testSuite = loader.discover('tests')
    testRunner = unittest.TextTestRunner(verbosity=2)
    testRunner.run(testSuite)