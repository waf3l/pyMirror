# -*- coding: utf-8 -*-
"""
Tests for path_wrapper module
"""
import os
import unittest
import sys
from shutil import rmtree, copy2

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
        self.create_files_cmp()

    def tearDown(self):
        rmtree(watch_dir)
        rmtree(mirror_dir)

    def create_files_cmp(self):
        """create random binary data and create copy of it"""
        self.fileA = os.path.join(watch_dir,'cmp_file_a.bin')
        self.fileB = os.path.join(watch_dir,'cmp_file_b.bin')
        self.fileC = os.path.join(watch_dir,'cmp_file_c.bin')
        with open(self.fileA,'wb') as myFile:
            myFile.write(os.urandom(1024))
        with open(self.fileC,'wb') as myFile:
            myFile.write(os.urandom(2048))
        copy2(self.fileA,self.fileB)

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
        self.assertFalse(self.path.make_dir(os.path.join(mirror_dir,'test')))

    def test_iterate_path(self):
        """Idont know how to test it"""
        pass

    def test_cmd_paths(self):
        """Test compare files"""
        self.assertTrue(self.path.cmp_paths(self.fileA,self.fileB))
        self.assertFalse(self.path.cmp_paths(self.fileA,self.fileC))
    
