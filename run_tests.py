import sys
import unittest

import xmlrunner


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests")
    runner = xmlrunner.XMLTestRunner(
        output="test-reports",
        verbosity=2,
    )
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)