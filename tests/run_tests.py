import sys
import unittest

def run():
    from suite import suite
    result = unittest.TextTestRunner(verbosity=2).run(suite())
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == '__main__':
    run()