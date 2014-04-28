# -*- coding: utf-8 -*-
"""
Tests for watcher module
"""
import os
import unittest
import sys
import time

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

from lib.engine.watcher import Watcher,jobQueue
from lib.setup.config import Config

class TestWatcherSetup(unittest.TestCase):
    """
    Tests setup for Watcher
    """
    def setUp(self):
        self.config = Config()
        self.watcher = Watcher(self.config)


    def tearDown(self):
        time.sleep(2)
        self.watcher.end_work.set()
        if self.watcher.isAlive():
        	self.watcher.join(timeout=5)

class TestWatcher(TestWatcherSetup):
	"""Test the watcher class"""

	def test_setup(self):
		"""Test setup watcher"""
		self.assertTrue(self.watcher.setup())

	def test_run(self):
		"""Test watcher thread work"""
		self.watcher.setup()
		self.watcher.start()
		self.assertTrue(self.watcher.isAlive())

	def test_watcher_event(self):
		"""test event process"""
		item = {}
		item['event_type'] = 'created'
		item['is_directory'] = True
		item['src_path'] = '/test_path'

		self.watcher.event_handler.on_any_event(item)
		self.assertEquals(jobQueue.count(),(True,1))
		#try to get item
		status,item = jobQueue.get()
		#test get status
		self.assertTrue(status)
		#test get item
		self.assertIsNotNone(item)