# test_filesystem.py
import unittest
import os
from file import File
from directory import Directory
from filesystem import FileSystem
import shutil,time

# The TestFileSystem class is a unit test case for testing file system operations.
class TestFileSystem(unittest.TestCase):
    def setUp(self):
        # Set up a FileSystem for testing
        self.fs = FileSystem()

    def test_create_file(self):
        """
        The function tests if a file is created successfully.
        """
        self.fs.create_file("test_file.txt")
        self.assertTrue(os.path.isfile("test_file.txt"))

    def test_remove_file(self):
        """
        The function tests the removal of a file and asserts that the file no longer exists.
        """
        self.fs.create_file("test_file.txt")
        self.fs.remove_file("test_file.txt")
        self.assertFalse(os.path.isfile("test_file.txt"))

    def test_create_directory(self):
        """
        The function tests if a directory is created successfully.
        """
        self.fs.create_directory("test_dir")
        self.assertTrue(os.path.isdir("test_dir"))

    def test_remove_directory(self):
        """
        The function tests the removal of a directory and checks if it no longer exists.
        """
        self.fs.create_directory("test_dir")
        self.fs.remove_directory("test_dir")
        self.assertFalse(os.path.isdir("test_dir"))

    def test_change_directory(self):
        """
        The function tests the change_directory method of a file system object by creating a directory,
        changing to that directory, and asserting that the current working directory matches the
        expected value.
        """
        self.fs.create_directory("test_dir")
        self.fs.change_directory("test_dir")
        self.assertEqual(os.getcwd(), self.fs.current_directory)

    def test_file_read_write(self):
        """
        The function tests the file read and write operations by creating a file, writing content to it,
        and then reading the content back.
        """
        file = File("test_file.txt", "user", "group", 0o644)
        file.write("Test content")
        self.assertEqual(file.read(), "Test content")

        
    def test_stat(self):
        """
        The function tests the show_stats method of a file system object by creating a test file and
        checking if the returned stats are not None and have a size of 0.
        """
        self.fs.create_file("test_file.txt")
        stats = self.fs.show_stats("test_file.txt")
        self.assertIsNotNone(stats)  # ensure stats are returned
        self.assertEqual(stats.st_size, 0)  # file should be empty

    def test_du(self):
        """
        The function `test_du` tests the `disk_usage` method of a file system by creating a file,
        writing content to it, and checking if the size of the file matches the length of the content.
        """

        self.fs.create_file("test_file.txt")
        file = File("test_file.txt", "user", "group", 0o644)
        file.write("Test content")
        size = self.fs.disk_usage("test_file.txt")
        self.assertEqual(size, len("Test content"))  
    
    def tearDown(self):
        # Clean up any files or directories created during testing
        if os.path.isfile("test_file.txt"):
            os.remove("test_file.txt")
        if os.path.isdir("test_dir"):
            shutil.rmtree("test_dir")

if __name__ == '__main__':
    unittest.main()