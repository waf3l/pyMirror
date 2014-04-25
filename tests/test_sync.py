# -*- coding: utf-8 -*-
"""
Tests for sync module
"""
import os
import unittest
import sys
from shutil import rmtree, copy2

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

watch_dir = os.path.join(app_dir,'tests','watch_dir')
mirror_dir = os.path.join(app_dir,'tests','mirror_dir')

from lib.setup.config import Config
from lib.helpers.hs_generator import get_random_string
from lib.engine.watcher import Watcher
from lib.engine.sync import Sync

class TestSyncSetup(unittest.TestCase):
    """
    Tests setup for Sync
    """
    def setUp(self):
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

		rmtree(watch_dir)
		rmtree(mirror_dir)

class TestSync(TestSyncSetup):
	"""Test for Sync class"""

	def create_random_file(self,path):
		"""Creaate random file"""
		file_name = os.path.join(path,get_random_string())
		with open(file_name,'wb') as myFile:
			myFile.write(os.urandom(1024))
		return file_name
	
	def test_sync_run(self):
		"""Test if sync thread is alive"""
		self.assertTrue(self.sync.isAlive())
