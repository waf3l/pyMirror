# -*- coding: utf-8 -*-
"""
Module for read config file
"""
from datetime import datetime
import os
import json

class Config():
	"""Main config for app"""

	def __init__(self):
		"""Init config"""	
		#System status
		self.system_status = self.read('system','status')

		#Logging level
		self.logging_level = self.read('logging','logging_level')

		#Logging to STOUT
		self.logging_stdout = self.read('logging','logging_stdout')

		#Logging to DEBUG to file
		self.logging_debug_to_file = self.read('logging','logging_debug_to_file')

		#Log file name for debug logging level
		self.file_debug_logging_name = 'mirror_debug_'+datetime.now().strftime('%Y%m%d')+'.log'

		#Log file name for info logging level
		self.file_info_logging_name = 'mirror_info_'+datetime.now().strftime('%Y%m%d')+'.log'

		#Log file name for warning logging level
		self.file_warning_logging_name = 'mirror_warning_'+datetime.now().strftime('%Y%m%d')+'.log'

		#Path to the watching directory
		self.watch_dir = self.read('watch_dir','path')

		#Path to the mirror directory
		self.mirror_dir = self.read('mirror_dir','path')

		#Home directory
		self.home_dir = os.path.expanduser("~")

		#Path to the logging files
		self.logging_directory = self.read('logging','logging_directory')

	def read(self,group,key):  	
		config = json.loads(open('config.json').read())
		return config[group][key]