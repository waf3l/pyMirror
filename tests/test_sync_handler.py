# -*- coding: utf-8 -*-
"""
Tests for sync handler class
"""
import os
import unittest
import sys
import time
import tempfile
from shutil import rmtree, copy2, move
from filecmp import cmp 

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

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
		temp_folder = tempfile.gettempdir()

		watch_dir_name = 'watch_dir'
		mirror_dir_name = 'mirror_dir'

		watch_dir = os.path.join(temp_folder,watch_dir_name)
		mirror_dir = os.path.join(temp_folder,mirror_dir_name)
		
		if not os.path.exists(watch_dir):
			os.makedirs(watch_dir)
		if not os.path.exists(mirror_dir):
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

		rmtree(self.config.watch_dir)
		rmtree(self.config.mirror_dir)
	
	def create_random_file_without_sync(self, path):
		"""Create random file"""
		#set the path and file name
		file_name = os.path.join(path,get_random_string()+'.bin')

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
		file_created, item = self.create_random_file_without_sync(self.config.watch_dir)

		#return file name and path with the status of sync
		return file_created, self.sync.sync_handler.process_item(item)

	def mod_file(self,path):
		"""Modified file"""
		#open file to be modified
		with open(path,'wb') as myFile:
			#modified the file
			myFile.write(os.urandom(2048))

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
				if item.event_type == 'modified':
					if item.src_path == path:
						jobQueue.task_all_done()
						return path, item

		#preventive mark all items as done
		jobQueue.task_all_done()
		raise ValueError('Can not get modified item')

	def del_file(self,path):
		"""Delete file"""
		#remove file
		os.remove(path)

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
				if item.event_type == 'deleted':
					if item.src_path == path:
						jobQueue.task_all_done()
						return path, item

		#preventive mark all items as done
		jobQueue.task_all_done()
		raise ValueError('Can not get deleted item')		

	def move_file(self,pathA,pathB):
		"""Move file from pathA to pathB"""
		#moved the file
		move(pathA,pathB)

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
				if item.event_type == 'moved':
					if item.src_path == pathA:
						jobQueue.task_all_done()
						return item.dest_path, item

		#preventive mark all items as done
		jobQueue.task_all_done()
		raise ValueError('Can not get moved item')

	def create_dir(self,path):
		"""Create directory"""
		#create path of new directory
		dir_path = os.path.join(path,get_random_string())
		#create directory
		os.makedirs(dir_path)
		#return created directory path
		return dir_path

class TestSyncHandler(TestSyncHelperSetup):
	"""
	Tests for Sync Handler class
	"""
	def test_on_create_file(self):
		"""Test on_create event"""
		#creat the file and return watcher item and file name and path
		file_name, item = self.create_random_file_without_sync(self.config.watch_dir)
		
		#process the item
		self.assertTrue(self.sync.sync_handler.process_item(item))
		
		#check if exist in mirror dir
		self.assertTrue(os.path.exists(file_name.replace(self.config.watch_dir,self.config.mirror_dir)))
		
		#compare synced file with original
		self.assertTrue(cmp(file_name,file_name.replace(self.config.watch_dir,self.config.mirror_dir)))

	def test_on_modified_with_sync_files(self):
		"""Test on_modified event with already synced files"""
		#create file
		file_name, status = self.create_random_file_and_sync()
	
		#check status of created file
		self.assertTrue(status)

		#modified the file
		mod_file, item = self.mod_file(file_name)
		
		#process the item
		self.assertTrue(self.sync.sync_handler.process_item(item))

		#check if exist in mirror dir
		self.assertTrue(os.path.exists(file_name.replace(self.config.watch_dir,self.config.mirror_dir)))
		
		#compare synced file with original
		self.assertTrue(cmp(file_name,file_name.replace(self.config.watch_dir,self.config.mirror_dir)))

	def test_on_modified_without_sync_files(self):
		"""Test on_modified event without synced files"""
		#create file
		file_name, item = self.create_random_file_without_sync(self.config.watch_dir)
	
		#check file path exist
		self.assertTrue(os.path.exists(file_name))

		#check if returned item is not none
		self.assertIsNotNone(item)

		#modified the file
		mod_file, item = self.mod_file(file_name)

		#process the item
		self.assertTrue(self.sync.sync_handler.process_item(item))

		#check if exist in mirror dir
		self.assertTrue(os.path.exists(file_name.replace(self.config.watch_dir,self.config.mirror_dir)))
		
		#compare synced file with original
		self.assertTrue(cmp(file_name,file_name.replace(self.config.watch_dir,self.config.mirror_dir)))

	def test_on_delete_with_sync_files(self):
		"""Test on_delete event with already synced files"""
		#create file
		file_name, status = self.create_random_file_and_sync()
	
		#check status of created file
		self.assertTrue(status)

		#modified the file
		deleted_file, item = self.del_file(file_name)
		
		#process the item
		self.assertTrue(self.sync.sync_handler.process_item(item))

		#check if exist in watch dir
		self.assertFalse(os.path.exists(file_name))

		#check if exist in mirror dir
		self.assertFalse(os.path.exists(file_name.replace(self.config.watch_dir,self.config.mirror_dir)))

	def test_on_delete_without_sync_files(self):
		"""Test on_delete event without synced files"""
		#create file
		file_name, item = self.create_random_file_without_sync(self.config.watch_dir)
	
		#check file path exist
		self.assertTrue(os.path.exists(file_name))

		#check if returned item is not none
		self.assertIsNotNone(item)

		#modified the file
		deleted_file, item = self.del_file(file_name)
		
		#process the item
		self.assertTrue(self.sync.sync_handler.process_item(item))

		#check if exist in watch dir
		self.assertFalse(os.path.exists(file_name))

		#check if exist in mirror dir
		self.assertFalse(os.path.exists(file_name.replace(self.config.watch_dir,self.config.mirror_dir)))

	def test_on_move_with_sync_files(self):
		"""Test on_moved event with already synced files"""
		#create file
		file_name, status = self.create_random_file_and_sync()
	
		#check status of created file
		self.assertTrue(status)

		#create directory
		dir_path = self.create_dir(self.config.watch_dir)

		#move the file
		dir_dest_path, item = self.move_file(file_name,dir_path)

		#check if exists dest_path
		self.assertTrue(os.path.exists(dir_dest_path))
		
		#process the item
		self.assertTrue(self.sync.sync_handler.process_item(item))

		#check if exist mirror dir dest path
		self.assertTrue(os.path.exists(dir_dest_path.replace(self.config.watch_dir,self.config.mirror_dir)))

		#check if exist watch dir dest path
		self.assertTrue(os.path.exists(dir_dest_path))

		#check if not exist source in watched dir
		self.assertFalse(os.path.exists(file_name))

		#check if not exist source in mirror dir
		self.assertFalse(os.path.exists(file_name.replace(self.config.watch_dir,self.config.mirror_dir)))

	def test_on_move_without_sync_files(self):
		"""Test on_moved event without synced files"""
		#create file
		file_name, item = self.create_random_file_without_sync(self.config.watch_dir)

		#check file path exist
		self.assertTrue(os.path.exists(file_name))

		#check if returned item is not none
		self.assertIsNotNone(item)

		#create directory
		dir_path = self.create_dir(self.config.watch_dir)

		#move the file
		dir_dest_path, item = self.move_file(file_name,dir_path)

		#check if exists dest_path
		self.assertTrue(os.path.exists(dir_dest_path))

		#process the item
		self.assertTrue(self.sync.sync_handler.process_item(item))

		#check if exist mirror dir dest path
		self.assertTrue(os.path.exists(dir_dest_path.replace(self.config.watch_dir,self.config.mirror_dir)))

		#check if exist watch dir dest path
		self.assertTrue(os.path.exists(dir_dest_path))

		#check if not exist source in watched dir
		self.assertFalse(os.path.exists(file_name))

		#check if not exist source in mirror dir
		self.assertFalse(os.path.exists(file_name.replace(self.config.watch_dir,self.config.mirror_dir)))