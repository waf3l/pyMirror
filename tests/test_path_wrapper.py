# -*- coding: utf-8 -*-
"""
Tests for path_wrapper module
"""
import os
import unittest
import sys
from shutil import rmtree

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

watch_dir = os.path.join(app_dir,'tests','watch_dir')
mirror_dir = os.path.join(app_dir,'tests','mirror_dir')

from lib.helpers.path_wrapper import PathWrapper



class TestPathWrapperSetup(unittest.TestCase):
    """
    Tests setup for PathWrapper
    """
    def setUp(self):
        os.makedirs(watch_dir)
        os.makedirs(mirror_dir)
        self.path = PathWrapper(watch_dir)

    def tearDown(self):
        rmtree(watch_dir)
        rmtree(mirror_dir)

class TestPathWrapper(TestPathWrapperSetup):
    """Test the PathWrapper functions"""

    def test_check_exist(self):
        """Check if path exist or not"""
        self.assertTrue(self.path.check_exist(os.path.expanduser('~')))
        self.assertFalse(self.path.check_exist('/dupa'))

    def test_check_path_protected(self):
        """Check if path is in protected path or not"""
        self.assertTrue(self.path.check_path_protect(watch_dir))
        self.assertFalse(self.path.check_path_protect('xcxcxc'))

    def test_make_dir(self):
        """Check if create directories"""
        self.assertTrue(self.path.make_dir(os.path.join(mirror_dir,'test')))
        self.assertFalse(self.path.make_dir('/sdsd/sdfsdfsf'))
