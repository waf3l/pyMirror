# -*- coding: utf-8 -*-
"""
Module for syncing monitored directory with mirror directory
"""

from threading import Thread, Event

from lib.helpers.job_queue import jobQueue

import logging
import time


class SyncHandler(object):
	"""Handler for job queue"""

	def __init__(self):
		"""Class initialization setup"""
		self.logger = logging.getLogger('app.sync_handler')

	def process_item(self,item):
		"""
		Work on item form job queue

		item: item from job queue
		"""
		pass

	def on_delete(self,item):
		""""""
		pass

	def on_create(self,item):
		""""""
		pass

	def on_modify(self,item):
		""""""
		pass

	def on_move(self,item):
		""""""
		pass

class Sync(Thread):
	"""Synhronization class"""
	
	def __init__(self,config):
		"""Class initialization setup"""
		#init super
		Thread.__init__(self)

		#set name of thread
		self.setName('sync_thread')

		#logger for this class
		self.logger = logging.getLogger('app.sync')

		#flag of working status
		self.do_work = Event()

		#flag end work
		self.end_work = Event()

		#config data
		self.config = config

		#initialize sync handler
		self.sync_handler = SyncHandler()

	def run(self):
		"""Run thread"""
		try:
			#set True to flag work
			self.do_work.set()

			#clear flad end work
			self.end_work.clear()

			self.logger.info('Sync thread is now working')
			#start infinite loop for sync thread
			while not self.end_work.is_set():
				time.sleep(1)
				while not jobQueue.isEmpty():
					status, item = jobQueue.get()
					if status:
						self.sync_handler.process_item(item)
					else:
						raise Exception('Can not get item from job queue')
			
			#clear work flad
			self.do_work.clear()
		except Exception, e:
			self.do_work.clear()
			self.logger.error('Sync.run error: %s'%(str(e)),exc_info=True)

