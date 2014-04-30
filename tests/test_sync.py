# -*- coding: utf-8 -*-
"""
Tests for sync module
"""
import os
import unittest
import sys
import time
import tempfile
from shutil import rmtree, copy2

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

from lib.setup.config import Config
from lib.helpers.hs_generator import get_random_string
from lib.engine.watcher import Watcher
from lib.engine.sync import Sync
from lib.helpers.job_queue import jobQueue

class TestSyncSetup(unittest.TestCase):
    """
    Tests setup for Sync
    """
    def setUp(self):
		temp_folder = tempfile.gettempdir()

		watch_dir_name = 'watch_'+get_random_string()
		mirror_dir_name = 'mirror_'+get_random_string()

		watch_dir = os.path.join(temp_folder,watch_dir_name)
		mirror_dir = os.path.join(temp_folder,mirror_dir_name)
		
		os.makedirs(watch_dir)
		os.makedirs(mirror_dir)

		self.config = Config()
		self.config.watch_dir = watch_dir
		self.config.mirror_dir = mirror_dir

		self.watcher = Watcher(self.config)
		self.watcher.setup()
		self.watcher.start()		
		self.sync = Sync(self.config)	
		self.sync.start()	


    def tearDown(self):
		self.watcher.end_work.set()
		if self.watcher.isAlive():
			self.watcher.join()
		self.sync.end_work.set()
		if self.sync.isAlive():
			self.sync.join()

		rmtree(self.config.watch_dir)
		rmtree(self.config.mirror_dir)

class TestSync(TestSyncSetup):
	"""Test for Sync class"""

	def test_sync_run(self):
		"""Test if sync thread is alive"""
		self.assertTrue(self.sync.isAlive())
