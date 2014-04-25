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
		self.config_path, self.config_data = self.get_config(os.getcwd())
		if self.config_path is None:
			raise OSError('Can not find config file')
		else:
			self.load_config()


	def load_config(self):
		"""Load config data"""
			
		#System status
		self.system_status = self.config_data['system']['status']
		
		#Logging level
		self.logging_level = self.config_data['logging']['logging_level']

		#Logging to STOUT
		self.logging_stdout = self.config_data['logging']['logging_stdout']

		#Logging to DEBUG to file
		self.logging_debug_to_file = self.config_data['logging']['logging_debug_to_file']

		#Log file name for debug logging level
		self.file_debug_logging_name = 'mirror_debug_'+datetime.now().strftime('%Y%m%d')+'.log'

		#Log file name for info logging level
		self.file_info_logging_name = 'mirror_info_'+datetime.now().strftime('%Y%m%d')+'.log'

		#Log file name for warning logging level
		self.file_warning_logging_name = 'mirror_warning_'+datetime.now().strftime('%Y%m%d')+'.log'

		#Path to the watching directory
		self.watch_dir = self.config_data['watch_dir']['path']

		#Path to the mirror directory
		self.mirror_dir = self.config_data['mirror_dir']['path']

		#Home directory
		self.log_path = self.config_data['logging']['log_path']

		#Path to the logging files
		self.logging_directory = self.config_data['logging']['logging_directory']

	def get_config_old(self,path):
		"""
		Get the path of config file and loads the config file
		
		path: the path for search config file
		"""
		prefix, directory = os.path.split(path)

		if directory == 'mirror_app': 
			return os.path.join(prefix,directory,'config.json'),json.loads(open(os.path.join(prefix,directory,'config.json')).read())
		else:
			while True:
				if (os.path.exists(prefix)) and (prefix is not '/'):
					prefix, directory = os.path.split(prefix)
					if directory == 'mirror_app':
						return os.path.join(prefix,directory,'config.json'),json.loads(open(os.path.join(prefix,directory,'config.json')).read())
				else:
					return None, None

	def get_config(self,path):
		"""
		Get the path of config file and loads the config file
		
		path: the path for search config file
		"""
		prefix, directory = os.path.split(path)

		if directory == 'tests':
			if os.path.exists(os.path.join(prefix,'config.json')): 
				return os.path.join(prefix,'config.json'),json.loads(open(os.path.join(prefix,'config.json')).read())
			else:
				raise OSError('Can not find config.json file')
		else:
			if os.path.exists(os.path.join(prefix,directory,'config.json')):
				return os.path.join(prefix,directory,'config.json'),json.loads(open(os.path.join(prefix,directory,'config.json')).read())
			else:
				raise OSError('Can not find config.json file')
		

	def read(self,group,key):
		"""
		Open config file and read the data
		
		group: data group
		key: key in data group to read the value
		"""
		try:
			config = json.loads(open(self.config_path).read())
			return config[group][key]
		except Exception, e:
			raise e