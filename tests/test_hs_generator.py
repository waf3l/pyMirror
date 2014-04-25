# -*- coding: utf-8 -*-
"""
Tests for hs_generator module
"""
import os
import unittest
import sys

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

from lib.helpers.hs_generator import  get_random_string, get_random_hash

class TestHSGeneratorSetup(unittest.TestCase):
	"""Setup for hs_generator"""

	def setUp(self):
		pass

	def tearDown(self):
		pass

class TestHSGenerator(TestHSGeneratorSetup):
	"""Test hs_generator"""
	
	def test_get_random_string(self):
		"""Test generate random string"""
		self.assertIsNotNone(get_random_string())

	def test_get_random_hash(self):
		"""Test generate random hash"""
		self.assertIsNotNone(get_random_hash())