# -*- coding: utf-8 -*-
"""
Module for syncing monitored directory with mirror directory
"""

from threading import Thread, Event

from lib.helpers.job_queue import jobQueue
from lib.helpers.path_wrapper import PathWrapper

import logging
import time


class SyncHandler(object):
	"""Handler for job queue"""

	def __init__(self,config):
		"""Class initialization setup"""
		
		#logger for this class
		self.logger = logging.getLogger('app.sync_handler')

		#config
		self.config = config

		#path manipulation
		self.path = PathWrapper()

	def process_item(self,item):
		"""
		Work on item form job queue

		item: item from job queue
		"""
		if item.event_type == 'deleted':
			self.on_delete(item)
		elif item.event_type == 'created':
			self.on_create(item)
		elif item.event_type == 'modified':
			self.on_modify(item)
		elif item.event_type == 'moved':
			self.on_move(item)
		else:
			#not recognize event fuck this, mark as done
			pass
		#mark item as done
		jobQueue.task_done()

	def on_delete(self,item):
		"""Item event on delete"""
		try:
			self.logger.debug('on_delete, item: %s'%(item))
			if self.path.del_path(item.src_path.replace(self.config.watch_dir, self.config.mirror_dir)):
				return True
			else:
				return False
		except Exception, e:
			self.logger.error('SyncHandler.on_delete, error: %s'%(str(e)),exc_info=True)
			return False

	def on_create(self,item):
		"""Item event on create"""
		def create():
			"""Create dir or copy file"""
			if item.is_directory:
				#object is directory
				if self.path.make_dir(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					#success
					return True
				else:
					#error
					return False
			else:
				#object is file
				if self.path.copy_path(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					#success
					return True
				else:
					#error
					return False
		try:
			self.logger.debug('on_create, item: %s'%(item))
			#check if created source object exist in mirror 
			if self.path.check_exist(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
				#object exist
				#delete old one on mirror
				if self.path.del_path(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					create()
				else:
					#error
					return False
			else:
				#object not exists
				create()

		except Exception, e:
			self.logger.error('SyncHandler.on_create, error: %s'%(str(e)),exc_info=True)
			return False

	def on_modify(self,item):
		"""Item event on modify"""
		try:
			self.logger.debug('on_modify, item: %s'%(item))
			"""
			First check if src exist on dest,
			If exist compar them. If the are equel skip this job.
			Else delete the dst and replce him with src one
			"""
			if self.path.check_exist(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
				#item exist on dst
				if self.path.cmp_paths(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					#are equel skiping
					return True
				else:
					#are diffrent
					#delete the old one
					if self.path.del_path(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
						#create the new one
						if self.path.copy_path(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							return True
						else:
							#error
							return False
					else:
						#error
						return False
			else:
				#item not exist in dst
				#create the item on dst
				if self.path.copy_path(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					return True
				else:
					#error
					return False
		except Exception, e:
			self.logger.error('SyncHandler.on_modify, error: %s'%(str(e)),exc_info=True)
			return False

	def on_move(self,item):
		"""Item eventon move"""
		try:
			self.logger.debug('on_move, item: %s'%(item))
			"""
			Copied from shutil.move

			If the destination is a directory or a symlink to a directory, the source
		    is moved inside the directory. The destination path must not already
		    exist.

		    If the destination already exists but is not a directory, it may be
		    overwritten depending on os.rename() semantics.
			"""
			if item.is_directory:
				#is dir
				if self.path.check_exist(item.dest_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					#path already exist skiping
					return True
				else:
					if self.path.move_path(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir),item.dest_path.replace(self.config.watch_dir,self.config.mirror_dir)):
						return True
					else:
						return False					
			else:
				#is file
				if self.path.move_path(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir),item.dest_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					return True
				else:
					return False
		except Exception, e:
			self.logger.error('SyncHandler.on_move, error: %s'%(str(e)),exc_info=True)
			return False

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
		self.sync_handler = SyncHandler(config)

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

