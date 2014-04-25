# -*- coding: utf-8 -*-
"""
Tests for config module
"""
import os
import unittest
import sys

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

from lib.setup.config import Config

class TestConfigSetup(unittest.TestCase):
    """
    Tests setup for Config
    """
    def setUp(self):
        self.config = Config()

    def tearDown(self):
        pass

class TestConfig(TestConfigSetup):
	"""Test the config class"""
	
	def test_get_config(self):
		"""Test discover file config path, and loading data from config file"""
		path, config_data = self.config.get_config(os.getcwd())
		self.assertIsNotNone(path)
		self.assertIsNotNone(config_data)

		path, config_data = self.config.get_config('/test_path')
		self.assertIsNone(path)
		self.assertIsNone(config_data)

	def test_read(self):
		"""Test read key value from config file"""
		self.assertRaises(KeyError,lambda: self.config.read('test','test'))

	def test_system_status(self):
		"""Test system_status value"""
		self.assertIsNotNone(self.config.system_status)
	
	def test_logging_level(self):
		"""Test logging_level value"""
		self.assertIsNotNone(self.config.logging_level)
	
	def test_logging_stdout(self):
		"""Test logging_stdout value"""
		self.assertIsNotNone(self.config.logging_stdout)
	
	def test_logging_debug_to_file(self):
		"""Test logging_debug_to_file value"""
		self.assertIsNotNone(self.config.logging_debug_to_file)
	
	def test_file_debug_logging_name(self):
		"""Test file_debug_logging_name value"""
		self.assertIsNotNone(self.config.file_debug_logging_name)
	
	def test_file_info_logging_name(self):
		"""Test file_info_logging_name value"""
		self.assertIsNotNone(self.config.file_info_logging_name)
	
	def test_file_warning_logging_name(self):
		"""Test file_warning_logging_name value"""
		self.assertIsNotNone(self.config.file_warning_logging_name)
	
	def test_watch_dir(self):
		"""Test watch_dir value"""
		self.assertIsNotNone(self.config.watch_dir)
	
	def test_mirror_dir(self):
		"""test mirror_dir value"""
		self.assertIsNotNone(self.config.mirror_dir)
	
	def test_log_path(self):
		"""Test log_path value"""
		self.assertIsNotNone(self.config.log_path)
	
	def test_logging_directory(self):
		"""Test logging_directory value"""
		self.assertIsNotNone(self.config.logging_directory)