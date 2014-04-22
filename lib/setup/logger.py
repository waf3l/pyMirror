# -*- coding: utf-8 -*-
"""
Module for logger initialization and configuration 
"""
from logging.handlers import RotatingFileHandler
import logging
import os
import sys

class Logger():
	"""
	Main logger for application
	"""
	def __init__(self,config):
		self.config = config

	def create_logger(self):
		"""
		Config and init logger
		"""
		try:
			"""Check if logging directory exist if not directory will be created"""
			if not os.path.isdir(os.path.join(self.config.log_path,self.config.logging_directory)):
				os.makedirs(os.path.join(self.config.log_path,self.config.logging_directory),mode=0770)

			"""Create main logger instance"""
			logger = logging.getLogger('app')
			
			"""Configure colors for level log"""
			logging.addLevelName( logging.DEBUG, "\033[1;32m%s\033[1;m" % logging.getLevelName(logging.DEBUG))
			logging.addLevelName( logging.INFO, "\033[1;33m%s\033[1;m" % logging.getLevelName(logging.INFO))
			logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;m" % logging.getLevelName(logging.WARNING))
			logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;m" % logging.getLevelName(logging.ERROR))
			logging.addLevelName( logging.CRITICAL, "\033[1;41m%s\033[1;m" % logging.getLevelName(logging.CRITICAL))
			"""Set level for logger"""
			logger.setLevel(self.config.logging_level)

			"""formatter for log""" 
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')	
			
			"""check is logging_stdout is True then log to console"""
			if self.config.logging_stdout:
				"""stream nadler for logger"""
				handler_stream = logging.StreamHandler(stream=sys.stdout)
				handler_stream.setLevel(self.config.logging_level)
				handler_stream.setFormatter(formatter)
				logger.addHandler(handler_stream)

			""""check if logging DEBUG to file is true"""
			if self.config.logging_debug_to_file:
				"""file handler for debug"""
				path_file_handler_debug = os.path.join(self.config.log_path,self.config.logging_directory,self.config.file_debug_logging_name)
				handler_debug = RotatingFileHandler(path_file_handler_debug, maxBytes=8192000,backupCount=100)
				handler_debug.setLevel(logging.DEBUG)
				handler_debug.setFormatter(formatter)
				logger.addHandler(handler_debug)

			"""file handler for info"""
			path_file_handler_info = os.path.join(self.config.log_path,self.config.logging_directory,self.config.file_info_logging_name)
			handler_info = RotatingFileHandler(path_file_handler_info, maxBytes=2048000,backupCount=100)
			handler_info.setLevel(logging.INFO)
			handler_info.setFormatter(formatter)
			logger.addHandler(handler_info)

			"""file handler for warning"""
			path_file_handler_warning = os.path.join(self.config.log_path,self.config.logging_directory,self.config.file_warning_logging_name)
			handler_warning = RotatingFileHandler(path_file_handler_warning, maxBytes=512000,backupCount=100)
			handler_warning.setLevel(logging.WARNING)
			handler_warning.setFormatter(formatter)
			logger.addHandler(handler_warning)

			return True
		except Exception, e:
			print e
			return False