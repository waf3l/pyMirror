# -*- coding: utf-8 -*-
"""
Tests for path_wrapper module
"""
import os
import unittest
import sys

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

from lib.helpers.job_queue import JobQueue

class TestJobQueueSetup(unittest.TestCase):
    """
    Tests setup for JobQueue
    """
    def setUp(self):
        self.job = JobQueue()

    def tearDown(self):
        pass

    def create_item_event_create(self,isDir=False,path='/'):
    	item = {}
    	item['event_type'] = 'created'
    	item['is_directory'] = isDir
    	item['src_path'] = path
    	return item

class TestJobQueue(TestJobQueueSetup):
	"""Test JobQueue functions"""

	def test_put(self):
		"""Test put item into queue"""
		#create item
		item = self.create_item_event_create()
		#test put item
		self.assertTrue(self.job.put(item))

	def test_get(self):
		"""Test get item from queue"""
		#create item
		item = self.create_item_event_create()
		#put item
		self.job.put(item)
		#try to get item
		status,item = self.job.get()
		#test get status
		self.assertTrue(status)
		#test get item
		self.assertIsNotNone(item)

	def test_isEmpty(self):
		"""Test if is empty or not queue"""
		#test if is empty
		self.assertTrue(self.job.isEmpty())
		
		#create item
		item = self.create_item_event_create()
		#put item
		self.job.put(item)
		#test if is not empty
		self.assertFalse(self.job.isEmpty())

	def test_task_done(self):
		"""Test mark item as done"""
		#create item
		item = self.create_item_event_create()
		#put item
		self.job.put(item)
		#try to get item
		status,item = self.job.get()
		#test get status
		self.assertTrue(status)
		#test get item
		self.assertIsNotNone(item)	
		
		#test task done
		self.assertTrue(self.job.task_done())

		#test raise ValueError and return False	
		self.assertFalse(self.job.task_done())

	def test_task_all_done(self):
		"""Test mark all items as done"""
		#create items
		for i in range(0,9):
			item = self.create_item_event_create()
			#put item
			self.job.put(item)
		
		#test task done
		self.assertTrue(self.job.task_all_done())

	def test_count(self):
		"""Test count item in queue"""
		#count empty job
		status,count = self.job.count()
		#test count
		self.assertTrue(status)
		self.assertEqual(count,0)

		#create item
		item = self.create_item_event_create()
		#put item
		self.job.put(item)
		#count not empty queue
		status,count = self.job.count()
		#test count
		self.assertTrue(status)
		self.assertEqual(count,1)

