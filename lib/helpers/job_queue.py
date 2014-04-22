# -*- coding: utf-8 -*-
"""
Module for job queue
"""

from Queue import Queue
import logging

class JobQueue():
	"""
	Class for job queue manipulation
	"""
	def __init__(self):
		#logger set for this instance
		self.logger = logging.getLogger('app.jobQueue')

		#main job queue
		self.queue = Queue()

	def put(self,item):
		"""
		Put new item to queue

		item: item that will br puted into queue
		"""
		try:
			self.logger.debug('Im trying to put new item to queue %s'%(item))
			self.queue.put(item)
			self.logger.debug('Successfull put new item to queue')
			return True
		except Exception, e:
			self.logger.error('Error method put, item: %s, error: %s'%(item,e),exc_info=True)
			return False
			

	def get(self):
		"""
		Get item from queue
		"""
		try:
			self.logger.debug('Im trying to get item from queue')
			item = self.queue.get()
			self.logger.debug('Recevie item from queue %s'%(item))
			return True, item
		except Exception, e:
			self.logger.error('Error method get, error: %s'%(e),exc_info=True)
			return False, None

	def isEmpty(self):
		"""
		Check if queue is empty
		"""
		self.logger.debug('Check if queue job is empty')
		isEmpty = self.queue.empty()
		self.logger.debug('Queue job is empty ?: %s'%(isEmpty))
		return isEmpty

	def task_done(self):
		"""
		Mark queue item as done
		"""
		try:
			self.logger.debug('Im trying mark queue job item as done')
			self.queue.task_done()
			self.logger.debug('Queue job item mark as done')
			return True
		except ValueError, e:
			self.logger.error('Error method task_done, error: %s'%(e),exc_info=True)
			return  False
	
	def count(self):
		"""
		Return number of items in queue
		"""	
		try:
			return True, self.queue.qsize()
		except Exception, e:
			self.logger.error('Error method task_done, error: %s'%(e),exc_info=True)
			return  False, None

jobQueue = JobQueue()
