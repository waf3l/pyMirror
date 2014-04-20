# -*- coding: utf-8 -*-
"""
Module for watching specified path directory and react for IO events 
"""

from threading import Thread
from threading import Event

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from lib.helpers.job_queue import jobQueue

import time
import logging

class WatcherHandler(FileSystemEventHandler):
	"""File system event handler for watcher thread"""

	def __init__(self):
		#init logger for this class
		self.logger = logging.getLogger('app.watcher.handler')

	def on_any_event(self,event):
		"""
		Catch any event ant put into queue

		event: Catched event
		"""
		self.logger.debug(str(event))
		jobQueue.put(event)

class Watcher(Thread):
	"""
	Main class for watching directory
	"""
	def __init__(self,config):
		#init Super
		Thread.__init__(self)
		
		#set thread name
		self.setName('watcher_thread')
		
		#config data
		self.config = config

		#set logger for this module
		self.logger = logging.getLogger('app.watcher')

		#declare end work flag
		self.end_work = Event()

		#flag of hard working :D
		self.do_work = Event()

		#file system event handler
		self.event_handler = WatcherHandler()



	def setup(self):
		"""
		Setup watchdog
		"""
		try:
			#watchdog object
			self.observer = Observer()
			self.observer.schedule(self.event_handler,self.config.watch_dir,recursive=True)
			return True
		except Exception, e:
			self.logger.error('Watcher.setup error: %s'%(str(e)),exc_info=True)
			return False

	def run(self):
		"""Run the thread"""
		try:
			#set True to flag work
			self.do_work.set()

			#clear flad end work
			self.end_work.clear()

			#start watchdog
			self.observer.start()
			self.logger.info('Start watching the directory')
			
			#start infinite loop for watchdog thread
			while not self.end_work.is_set():
				time.sleep(1)
			
			#clear work flad
			self.do_work.clear()
			
			#stop watchdog
			self.observer.stop()
			self.logger.info('Send stop signal for watching directory thread')
			
			#wait for end work of watchdog
			self.logger.info('Waiting to finish watching the directory')
			self.observer.join()
			self.logger.info('Watcher ends his work')
		except Exception, e:
			self.do_work.clear()
			self.logger.error('Watcher.run error: %s'%(str(e)),exc_info=True)

