# -*- coding: utf-8 -*-
"""
Module for syncing monitored directory with mirror directory
"""

from threading import Thread, Event

from lib.helpers.job_queue import jobQueue
from lib.helpers.path_wrapper import PathWrapper

import logging
import time
import os.path

class SyncHandler(object):
	"""Handler for job queue"""

	def __init__(self,config):
		"""Class initialization setup"""
		
		#logger for this class
		self.logger = logging.getLogger('app.sync_handler')

		#config
		self.config = config

		#path manipulation
		self.path = PathWrapper(self.config.watch_dir)

	def process_item(self,item):
		"""
		Work on item form job queue

		item: item from job queue
		"""
		if item.event_type == 'deleted':
			if self.on_delete(item):
				return True
			else:
				#error
				return False
		elif item.event_type == 'created':
			if self.on_create(item):
				return True
			else:
				#error
				return False
		elif item.event_type == 'modified':
			if self.on_modify(item):
				return True
			else:
				#error
				return False
		elif item.event_type == 'moved':
			if self.on_move(item):
				return True
			else:
				#error
				return False
		else:
			#not recognize event fuck this 
			return True

	def on_delete(self,item):
		"""Item event on delete"""
		try:
			self.logger.debug('on_delete, item: %s'%(item))
			if self.path.check_exist(item.src_path.replace(self.config.watch_dir, self.config.mirror_dir)):
				if self.path.del_path(item.src_path.replace(self.config.watch_dir, self.config.mirror_dir)):
					return True
				else:
					#can not delete path
					return False
			else:
				#path not exist, skipping
				return True
		except Exception, e:
			self.logger.error('SyncHandler.on_delete, error: %s'%(str(e)),exc_info=True)
			return False

	def on_create(self,item):
		"""New item event on create"""
		try:
			self.logger.debug('on_create, item: %s'%(item))
			#check if source path exist
			if self.path.check_exist(item.src_path):
				#check if mirror path exist
				if self.path.check_exist(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					#mirror path exists
					if item.is_directory:
						#path is directory skipping
						return True
					else:
						#compare the two files
						if self.path.cmp_paths(item.src_path,item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							#files are equel skiping
							return True
						else:
							#file are diffrent delete old and copy new one
							if self.path.del_path(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
								if self.path.copy_path(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
									#success
									return True
								else:
									#error
									return False
							else:
								#error
								return False	
				else:
					#mirror path not exists
					if item.is_directory:
						#directory not exist create it
						if self.path.make_dir(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							#success
							return True
						else:
							#error, can not create directory
							return False
					else:
						#file not exist copy it
						if self.path.copy_path(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							#success
							return True
						else:
							#error, can not copy this file
							return False
			else:
				#sourc path not exist, skipping
				return True
		except Exception, e:
			self.logger.error('SyncHandler.on_create, error: %s'%(str(e)),exc_info=True)
			return False

	def on_modify(self,item):
		"""Item event on modify"""
		try:
			self.logger.debug('on_modify, item: %s'%(item))
			
			if self.path.check_exist(item.src_path):
				#source path exist
				#check if mirror path exist
				if self.path.check_exist(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):				
					#mirror path exist
					if item.is_directory:
						#path is dir return
						return True
					else:
						#path is file
						#compare the original with mirror
						if self.path.cmp_paths(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							#are equel skiping
							return True
						else:
							#files are diffrent
							#delete the old one
							if self.path.del_path(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
								#copy the new one
								if self.path.copy_path(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
									return True
								else:
									#error, can not copy the new one
									return False
							else:
								#error, can not delete the old one
								return False
				else:
					#mirror path not exists
					if item.is_directory:
						#path is directory
						if self.path.make_dir(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							return True
						else:
							#error, can not create directory
							return False
					else:
						#path is file
						if self.path.copy_path(item.src_path, item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							return True
						else:
							#error, can not copy new file
							return False
			else:
				#source path not exists skipping
				return True
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

			#check if the new destination exist
			if self.path.check_exist(item.dest_path):
				#new dest exist
				#check if old mirror path exist
				if self.path.check_exist(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir)):
					#old mirror path exist
					if item.is_directory:
						#path is directory
						#check if new dest pth exist in mirror
						if self.path.check_exist(item.dest_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							#path already exist on mirror, skiping
							return True
						else:
							#path not exist
							#moving to the new location
							if self.path.move_path(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir),item.dest_path.replace(self.config.watch_dir,self.config.mirror_dir)):
								return True
							else:
								#error, can not move old path to new one
								return False
					else:
						#path is file
						if self.path.move_path(item.src_path.replace(self.config.watch_dir,self.config.mirror_dir),item.dest_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							return True
						else:
							#error, can not move old path to new one
							return False
				else:
					#old mirror dest not exist, replace move by copy
					if item.is_directory:
						#path is directory
						if self.path.make_dir(item.dest_path.replace(self.config.watch_dir,self.config.mirror_dir)):
							return True
						else:
							#error, can not create new directory
							return False
					else:
						#path is file
							if self.path.copy_path(item.dest_path, item.dest_path.replace(self.config.watch_dir,self.config.mirror_dir)):
								return True
							else:
								#error, can not copy the new one
								return False
			else:
				#new dest not exist skipping
				return True
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
						if self.sync_handler.process_item(item):
							#mark item as done
							jobQueue.task_done()
						else:
							#handle error, but for the time being now mark as done
							jobQueue.task_done()
					else:
						raise Exception('Can not get item from job queue')
			
			#clear work flad
			self.do_work.clear()
		except Exception, e:
			self.do_work.clear()
			self.logger.error('Sync.run error: %s'%(str(e)),exc_info=True)

