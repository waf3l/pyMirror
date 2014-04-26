# -*- coding: utf-8 -*-
"""
Directory mirror app based on watchdog library
"""

from lib.setup.logger import Logger
from lib.setup.config import Config
from lib.engine.watcher import Watcher
from lib.engine.index import Index
from lib.engine.sync import Sync

import sys
import logging
import time

class Main(object):
	"""Main app class"""
	
	def __init__(self):
		"""Initialize main app class"""
		#get config 
		try:
			self.config = Config()
		except Exception, e:
			raise e
			sys.exit(1)
		
		#set logger for main class
		self.logger = Logger(self.config)	
		
		#initialize watcher thread
		self.watcher = Watcher(self.config)	
		
		#initialize index thread
		self.index = Index(self.config)

		#initialize sync thread
		self.sync = Sync(self.config)

	def setup(self):
		"""Setup the app"""
		if self.logger.create_logger():
			self.log = logging.getLogger('app.main')
			self.log.info('Init main logger')
			return True
		else:
			print 'Error main setup'
			return False

	def startWatcher(self):
		"""Start watcher thread"""
		try:
			if self.watcher.setup():
				self.log.info('Starting watcher thread')
				self.watcher.start()
				self.log.info('Watcher thread working')
				return True
			else:
				main.log.error('Error start watcher, see log for detail')
				return False
		except Exception, e:
			self.log.error('Main.startWatcher error: %s'%(str(e)),exc_info=True)
			return False

	def startIndex(self):
		"""Start index thread"""
		try:
			self.index.start()
			self.log.info('Waiting for indexing ends work')
			self.index.join()
			self.log.info('Indexing end work')
			if self.index.finish_success.is_set():
				return True
			else:
				self.log.error('Can not continue work, index finised work with error status, check log for detail')
				return False
		except Exception, e:
			self.log.error('Main.startIndex error: %s'%(str(e)),exc_info=True)
			return False

	def startSync(self):
		"""Start sync thread"""
		try:
			self.log.info('Starting sync thread')
			self.sync.start()
			self.log.info('Sync thread working')
			return True
		except Exception, e:
			self.log.error('Main.startSync error: %s'%(str(e)),exc_info=True)
			return False

	def mainLoop(self):
		"""Main infinite loop"""
		try:
			while True:
				time.sleep(1)
				if not self.do_check_engine():
					self.log.error('Check engine return error, shutdown the app')
					raise KeyboardInterrupt
		except KeyboardInterrupt, e:
			self.log.warning('KeyboardInterrupt')
			self.do_exit(0)

	def do_check_engine(self):
		"""Check if all threads all working"""
		if not self.watcher.do_work.is_set():
			self.log.error('Watcher thread suddenly ends his work')
			return False
		if not self.sync.do_work.is_set():
			self.log.error('Sync thread suddenly ends his work')
			return False

		return True

	def do_exit(self,exit_code):
		"""
		Finish all threads and exit app
		
		exit_code: exit status
		"""
		self.log.info('Send end work signal to watcher thread')
		self.watcher.end_work.set()
		
		self.log.info('Waiting for watcher thread ends his work')
		self.watcher.join()

		self.log.info('Send end work signal to sync thread')
		self.sync.end_work.set()

		self.log.info('Waiting for sync thread ends his work')
		self.sync.join

		#exit with status code
		sys.exit(exit_code)

if __name__ == "__main__":
	main = Main()
	if main.setup():
		if main.startWatcher():
			if main.startIndex():
				if main.startSync():	
					main.mainLoop()
				else:
					sys.exit(1)
			else:
				sys.exit(1)
		else:
			sys.exit(1)

	else:
		sys.exit(1)
