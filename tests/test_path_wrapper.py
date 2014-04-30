# -*- coding: utf-8 -*-
"""
Tests for path_wrapper module
"""
import os
import unittest
import sys
import tempfile
from shutil import rmtree, copy2

app_dir = os.path.dirname(os.getcwd())
sys.path.append(app_dir)

#watch_dir = os.path.join(app_dir,'tests','watch_dir')
#mirror_dir = os.path.join(app_dir,'tests','mirror_dir')

watch_dir = os.path.join(tempfile.gettempdir(),'tests','watch_dir')
mirror_dir = os.path.join(tempfile.gettempdir(),'tests','mirror_dir')

from lib.helpers.path_wrapper import PathWrapper
from lib.helpers.hs_generator import get_random_string



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

    def create_random_file(self,path):
        """Create random file"""
        file_name = os.path.join(path,get_random_string(8))
        with open(file_name,'wb') as myFile:
            myFile.write(os.urandom(1024))
        return file_name

    def create_random_dir(self,path):
        """Create random direcotry"""
        dir_path = os.path.join(path,get_random_string(8))
        os.makedirs(dir_path)
        return dir_path

class TestPathWrapper(TestPathWrapperSetup):
    """Test the PathWrapper functions"""

    def test_check_exist(self):
        """Check if path exist or not"""
        #check path that exists
        self.assertTrue(self.path.check_exist(os.path.expanduser('~')))
        #check path that not exists
        self.assertFalse(self.path.check_exist('/dupa'))

    def test_check_path_protect(self):
        """Check if path is in protected path or not"""
        #test protected path
        self.assertTrue(self.path.check_path_protect(watch_dir))
        #test not protected path
        self.assertFalse(self.path.check_path_protect('xcxcxc'))
        #test none protected path
        path_wrapper_none_protected = PathWrapper()
        self.assertFalse(path_wrapper_none_protected.check_path_protect(watch_dir))

    def test_split_path(self):
        """Check method splits the path and return vaules"""
        #try to split path
        status, path,path_item = self.path.split_path(watch_dir)
        #check status of split path
        self.assertTrue(status)
        self.assertEqual(watch_dir,os.path.join(path,path_item))

    def test_make_dir(self):
        """Check if create directories"""
        #creat edirectory
        self.assertTrue(self.path.make_dir(os.path.join(mirror_dir,'test')))
        #create error catching
        self.assertFalse(self.path.make_dir(os.path.join(mirror_dir,'test')))

    def test_iterate_path(self):
        """I dont know how to test it"""
        pass

    def test_cmp_paths(self):
        """Test compare files"""
        #compare equel files
        self.assertTrue(self.path.cmp_paths(self.fileA,self.fileB))
        #compare diffrent files
        self.assertFalse(self.path.cmp_paths(self.fileA,self.fileC))
        #raise exception
        self.assertFalse(self.path.cmp_paths('/assasas','asasasas'))

    def test_del_path(self):
        """Test delete path"""
        #test delete protected path
        self.assertFalse(self.path.del_path(watch_dir))
        #test delete path that not exists
        self.assertFalse(self.path.del_path('/sdsdsdsd'))

        #test delete directory
        dir_path = self.create_random_dir(mirror_dir)
        self.assertTrue(self.path.del_path(dir_path))
        self.assertFalse(self.path.check_exist(dir_path))

        #test delete file
        file_path = self.create_random_file(mirror_dir)
        self.assertTrue(self.path.del_path(file_path))
        self.assertFalse(self.path.check_exist(file_path))

    def test_copy_path(self):
        """Test copy files"""
        #create file
        file_path = self.create_random_file(watch_dir)
        
        #test copy from a to b
        copy_to_file_path = file_path.replace(file_path,mirror_dir)  
        self.assertTrue(self.path.copy_path(file_path,copy_to_file_path))
        self.assertTrue(self.path.check_exist(copy_to_file_path))
        
        #TODO: Add test with create not existing directory

        #TODO: Add test that return False becouse can not create directory

    def test_move_path(self):
        """Test move file or directory"""
        #create file
        file_path = self.create_random_file(watch_dir)
        #path to move file
        file_move_path = file_path.replace(watch_dir,mirror_dir)
        #move file
        self.assertTrue(self.path.move_path(file_path,file_move_path))
        #check if exists moved file
        self.assertTrue(self.path.check_exist(file_move_path))
        #check if file was moved
        self.assertFalse(self.path.check_exist(file_path))

        #create directory
        dir_path = self.create_random_dir(watch_dir)
        #dir path to move
        dir_move_path = dir_path.replace(watch_dir,mirror_dir)
        #move dir
        self.assertTrue(self.path.move_path(dir_path,dir_move_path))
        #check if exists moved dir
        self.assertTrue(self.path.check_exist(dir_move_path))
        #check if dir moved
        self.assertFalse(self.path.check_exist(dir_path))

        #raise exception
        self.assertFalse(self.path.move_path('asd','ssdsd'))

