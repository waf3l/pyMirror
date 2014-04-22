# -*- coding: utf-8 -*-
"""
Module for handling path manipulation
"""

import os
import logging

from shutil import copy2, rmtree, move
from filecmp import cmp

class PathWrapper(object):
	"""Class for path manipulation purpose"""
	def __init__(self):
		"""Class initialization setup"""

		#logger object
		self.logger = logging.getLogger('app.wrapper.path')

	def check_exist(self,path):
		"""
		Check if path exist on local storage

		path: path to check
		"""
		try:
			self.logger.debug('Try to check if path exists, path: %s'%(path))
			value = os.path.exists(path)
			if value:
				self.logger.debug('Path exist, path: %s'%(path))
				return True
			else:
				self.logger.debug('Path not exist, path: %s'%(path))
				return False
		except Exception, e:
			self.logger.error('PathWrapper.check_exist: %s'%(str(e)),exc_info=True)
			return False

	def make_dir(self,path):
		"""
		Create directories

		path: path of directory that will be created
		"""
		try:
			self.logger.debug('Try to create directory, path: %s'%(path))
			os.makedirs(path,mode=0770)
			self.logger.debug('Directory created, path: %s'%(path))
			return True
		except Exception, e:
			self.logger.error('PathWrapper.make_dir: %s'%(str(e)),exc_info=True)
			return False

	def iterate_path(self,path):
		"""
		Recursively iterate directory tree and return each directory and file path

		path: path to be iterated
		"""
		self.logger.debug('Start iterate directory and file tree, watched path: %s'%(path))
		for subdir,dirs,files in os.walk(path):
			if len(files) > 0:
				for file in files:
					self.logger.debug('Returned path %s'%(os.path.join(subdir,file)))
					yield os.path.join(subdir,file)
			else:
				self.logger.debug('Returned path %s'%(subdir))
				yield subdir

	def cmp_paths(self,pathA,pathB):
		"""
		Check if paths exist and compare them

		pathA: path of file A
		pathB: path of file B
		"""
		try:
			self.logger.debug('Try to compare files, file A: %s, file B: %s'%(pathA,pathB))
			value = cmp(pathA,pathB)
			if value:
				self.logger.debug('Files are equel, file A: %s, file B: %s'%(pathA,pathB))
				return True
			else:
				self.logger.debug('Files are diffrent, file A: %s, file B: %s'%(pathA,pathB))
				return False
		except Exception, e:		
			self.logger.error('PathWrapper.cmp_paths: %s'%(str(e)),exc_info=True)
			return False

	def del_path(self,path):
		"""
		Delete path

		path: the path that will be deleted
		"""
		try:
			self.logger.debug('Try to delete directory or file, path: %s'%(path))
			if os.path.isdir(path):
				self.logger.debug('Path is directory, path: %s'%(path))
				rmtree(path)
				return True
			elif os.path.isfile(path):
				self.logger.debug('Path is file, path: %s'%(path))
				os.remove(path)
				return True
			else:
				#path not recognize 
				self.logger.warning('Path is not recognize, path: %s'%(path))
				return False
		except Exception, e:
			self.logger.error('PathWrapper.del_path: %s'%(str(e)),exc_info=True)
			return False

	def copy_path(self,src_path,dst_path):
		"""
		Copy file from source path to destination path.

		src_path: source path
		dst_path: destination path
		"""
		try:
			self.logger.debug('Try to copy file from : %s to: %s'%(src_path,dst_path))
			if self.check_exist(os.path.split(dst_path)[0]):
				copy2(src_path,dst_path)
				self.logger.debug('File successfull copied from %s to %s'%(src_path,dst_path))
			else:
				if self.make_dir(os.path.split(dst_path)[0]):
					copy2(src_path,dst_path)
					self.logger.debug('File successfull copied from %s to %s'%(src_path,dst_path))
				else:
					#can not create directory tree for file to copy
					return False
			return True
		except Exception, e:
			self.logger.error('PathWrapper.copy_path: %s'%(str(e)),exc_info=True)
			return False

	def move_path(self,src_path,dst_path):
		"""
		Recursively move a file or directory to another location

		src_path: source path
		dst_path: destination path
		"""
		try:
			self.logger.debug('Try to move file or directory from: %s to: %s'%(src_path,dst_path))
			move(src_path,dst_path)
			return True
		except Exception, e:
			self.logger.error('PathWrapper.move_path: %s'%(str(e)),exc_info=True)
			return False