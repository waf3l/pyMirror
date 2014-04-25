# -*- coding: utf-8 -*-
"""
Tests for logger module
"""
import os
import unittest
import sys

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

from lib.setup.logger import Logger
from lib.setup.config import Config

class TestLoggerSetup(unittest.TestCase):
    """
    Tests setup for Logger
    """
    def setUp(self):
    	self.config = Config()
        self.logger = Logger(self.config)

    def tearDown(self):
        pass

class TestLogger(TestLoggerSetup):
	"""Test the logger class"""

	def test_create_logger(self):
		"""Test create logger"""
		self.assertTrue(self.logger.create_logger())