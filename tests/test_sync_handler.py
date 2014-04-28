# -*- coding: utf-8 -*-
"""
Tests for sync handler class
"""
import os
import unittest
import sys
import time
from shutil import rmtree, copy2

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

watch_dir = os.path.join(app_dir,'tests','watch_dir')
mirror_dir = os.path.join(app_dir,'tests','mirror_dir')

from lib.setup.config import Config
from lib.helpers.hs_generator import get_random_string
from lib.engine.watcher import Watcher
from lib.engine.sync import Sync
from lib.helpers.job_queue import jobQueue

class TestSyncHelperSetup(unittest.TestCase):
	"""
	Tests setup for Sync Handler
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


	def tearDown(self):
		self.watcher.end_work.set()
		if self.watcher.isAlive():
			self.watcher.join(timeout=5)

		rmtree(watch_dir)
		rmtree(mirror_dir)
	
	def create_random_file_without_sync(self, path):
		"""Create random file"""
		#set the path and file name
		file_name = os.path.join(path,get_random_string())

		#create file
		with open(file_name,'wb') as myFile:
			myFile.write(os.urandom(1024))

		#wait for watcher that catch the events to job queue
		while jobQueue.isEmpty():
			time.sleep(1)

		#process job queue
		while not jobQueue.isEmpty():
			#get item from job queue
			status, item = jobQueue.get()
			#mark that item as done
			jobQueue.task_done()
			#check if this item is that we looking for
			if status:
				if item.event_type == 'created':
					if item.src_path == file_name:
						jobQueue.task_all_done()
						return file_name, item

		#preventive mark all items as done
		jobQueue.task_all_done()
		raise ValueError('Can not get created item')

	def create_random_file_and_sync(self):
		"""Create a random file and sync the file"""
		#create the file
		file_created, item = self.create_random_file_without_sync(watch_dir)

		#return file name and path with the status of sync
		return file_created, self.sync.sync_handler.process_item(item)

	def mod_file(self,path):
		"""Modified file"""
		#TODO: rewrite like create_random_file
		with open(path,'wb') as myFile:
			myFile.write(os.urandom(2048))
		
		while jobQueue.isEmpty():
			time.sleep(1)

		while not jobQueue.isEmpty():
			status, item = jobQueue.get()
			if item.event_type == 'modified':
				if status:
					jobQueue.task_all_done()
					#TODO: return item not process item
					return self.sync.sync_handler.process_item(item)
				else:
					jobQueue.task_all_done()
					return False
		jobQueue.task_all_done()
		raise ValueError('Can not get modified item')

class TestSyncHandler(TestSyncHelperSetup):
	"""
	Tests for Sync Handler class
	"""
	def test_on_create(self):
		"""Test on_create event"""
		#creat the file and return watcher item and file name and path
		file_name, item = self.create_random_file_without_sync(watch_dir)
		#process the item
		self.assertTrue(self.sync.sync_handler.process_item(item))
		self.assertTrue(os.path.exists(file_name.replace(watch_dir,mirror_dir)))
		#TODO: add compar files watch_die with mirror_dir


	def atest_on_modified_without_compare(self):
		file_created = self.create_random_file(watch_dir)
		file_modified = self.mod_file(file_created)

		time.sleep(2)
		while not jobQueue.isEmpty():
			status, item = jobQueue.get()
			self.assertTrue(status)
			if item.event_type == 'modified':
				self.assertTrue(self.sync.sync_handler.process_item(item))
			jobQueue.task_done()

	def test_on_modified_with_compare(self):
		path_file, status = self.create_random_file_and_sync()
		
		self.assertTrue(status)
		#self.assertTrue(self.mod_file(path_file))
		#TODO: process item
		#TODO: add check exists
		#TODO: compare org with mirror