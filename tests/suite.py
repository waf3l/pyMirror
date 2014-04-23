import unittest
from test_path_wrapper import TestPathWrapper
from test_job_queue import TestJobQueue

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPathWrapper))
    suite.addTest(unittest.makeSuite(TestJobQueue))
    # suite.addTest(unittest.makeSuite(TestApplication))
    # suite.addTest(unittest.makeSuite(TestUsers))
    # suite.addTest(unittest.makeSuite(TestGroups))
    # suite.addTest(unittest.makeSuite(TestGpo))
    # suite.addTest(unittest.makeSuite(TestSniffer))
    # suite.addTest(unittest.makeSuite(TestIndex))
    return suite