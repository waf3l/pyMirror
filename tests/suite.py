import unittest
from test_path_wrapper import TestPathWrapper
from test_job_queue import TestJobQueue
from test_config import TestConfig
from test_logger import TestLogger
from test_hs_generator import TestHSGenerator
from test_watcher import TestWatcher
from test_sync import TestSync
from test_sync_handler import TestSyncHandler

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPathWrapper))
    suite.addTest(unittest.makeSuite(TestJobQueue))
    suite.addTest(unittest.makeSuite(TestConfig))
    suite.addTest(unittest.makeSuite(TestLogger))
    suite.addTest(unittest.makeSuite(TestHSGenerator))
    suite.addTest(unittest.makeSuite(TestWatcher))
    #suite.addTest(unittest.makeSuite(TestSync))
    suite.addTest(unittest.makeSuite(TestSyncHandler))
    return suite