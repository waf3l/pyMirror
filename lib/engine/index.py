# -*- coding: utf-8 -*-
"""
Module for indexing watched directory and mirror directory.

When indexing find difference between the two directories it will
try to sync them.
"""
from threading import Thread, Event
from lib.helpers.path_wrapper import PathWrapper

import logging
import os.path

class Index(Thread):
	"""
	Class for indexing the watched and mirror directory, when indexing find
	difference between this two directories then will by trying to sync them.
	"""
	def __init__(self,config):
		"""Class initial setup"""

		Thread.__init__(self)

		#config data
		self.config = config

		#set thread name
		self.setName('index_thread')

		#set logger for this module
		self.logger = logging.getLogger('app.index')

		#declare end work flag
		#self.end_work = Event()

		#flag of hard working :D
		#self.do_work = Event()	

		#flag for verify if thread work end with success status or failure
		self.finish_success = Event()

		#path manipulation
		self.path = PathWrapper()

		#list of mirror paths that passed validation with original directory
		self.mirror_validation_paths=[]

	def run(self):
		"""Run thread"""
		if self.validate():
			self.finish_success.set()
		else:
			self.finish_success.clear()	

	def validate(self):
		"""Validate mirror directory and original direcotry"""
		self.logger.info('Start indexing watched directory and mirror directory')
		if self.path.check_exist(self.config.mirror_dir):
			#mirror exists
			if self.check_mirror():
				#mirror checked
				if self.check_original():
					#TODO: check if mirror_validation_paths is empty
					self.logger.info('Index finish work with status: success')
					return True
				else:
					self.logger.error('Index finish work with status: error')
					return False
			else:
				self.logger.error('Index finish work with status: error')
				return False
		else:
			if self.path.make_dir(self.config.mirror_dir):
				#mirror path created 
				if self.check_original():
					#TODO: check if mirror_validation_paths is empty
					self.logger.info('Index finish work with status: success')
					return True
				else:
					self.logger.error('Index finish work with status: error')
					return False
			else:
				#mirror path not created 
				self.logger.error('Index finish work with status: error')
				return False 

	def check_mirror(self):
		"""Compare mirror path list with original direcotry"""
		try:
			self.logger.info('Indexing mirror directory')
			self.mirror_validation_paths.append(self.config.mirror_dir)
			for path in self.path.iterate_path(self.config.mirror_dir):				
				self.logger.debug('Index path: %s'%(path))
				#check if path is file
				if os.path.isfile(path):
					self.logger.debug('Path is FILE, path: %s'%(path))
					#check if file exist in watched directory
					if self.path.check_exist(path.replace(self.config.mirror_dir,self.config.watch_dir)):					
						if not self.path.cmp_paths(path,path.replace(self.config.mirror_dir,self.config.watch_dir)):
							#are diffrent
							if not self.path.del_path(path):
								self.logger.error('Index mirror directory error')
								return False
						else:
							#files are the same skip to next path
							self.logger.debug('Mirror path: %s are equel with original path: %s, add mirror path to list validation'%(path,path.replace(self.config.mirror_dir,self.config.watch_dir)))
							self.mirror_validation_paths.append(path)
					else:
						#file not exist in watched directory
						#delete the file
						if not self.path.del_path(path):
							self.logger.error('Index mirror directory error')
							return False
				#check if path is dir
				elif os.path.isdir(path):
					self.logger.debug('Path is DIRECTORY, path: %s'%(path))
					if not self.path.check_exist(path.replace(self.config.mirror_dir,self.config.watch_dir)):
						if not self.path.del_path(path):
							self.logger.error('Index mirror directory error')
							return False
					else:
						#directory exist skip to next path
						self.mirror_validation_paths.append(path)
				else:
					#not recognize path
					self.logger.warning('Not recognize path: %s'%(path))
					self.logger.error('Index mirror directory error') 
					return False
			self.logger.info('Index mirror directory ok')
			return True
		except Exception, e:
			self.logger.error('Index.check_mirror, error: %s'%(str(e)),exc_info=True)
			return False

	def check_original(self):
		"""Compare original path list with mirror"""
		try:
			self.logger.info('Indexing watched directory')
			for path in self.path.iterate_path(self.config.watch_dir):
				self.logger.debug('Index path: %s'%(path))
				#check if path exist in validation list
				if not path.replace(self.config.watch_dir,self.config.mirror_dir) in self.mirror_validation_paths:
					self.logger.debug('Path not exist in mirror list validation, path: %s'%(path))
					if os.path.isfile(path):
						self.logger.debug('Path is FILE, path: %s'%(path))
						if not self.path.copy_path(path,path.replace(self.config.watch_dir,self.config.mirror_dir)):
							#failed copy file
							self.logger.error('Index watched directory error')
							return False						
					elif os.path.isdir(path):
						self.logger.debug('Path is DIRECTORY, path: %s'%(path))

						if not self.path.make_dir(path.replace(self.config.watch_dir,self.config.mirror_dir)):
							self.logger.error('Index watched directory error')
							return False
					else:
						#not recognize path
						self.logger.warning('Not recognize path: %s'%(path))
						self.logger.error('Index watched directory error')
						return False
				else:
					#path exist in list validation skip and remove from list
					self.logger.debug('Path exist in mirror list validation, skiping and removing path from list, path: %s'%(path))
					self.mirror_validation_paths.remove(path.replace(self.config.watch_dir,self.config.mirror_dir))
			self.logger.info('Index watched directory ok')
			return True
		except Exception, e:
			self.logger.error('Index.check_original, error: %s'%(str(e)),exc_info=True)
			return False