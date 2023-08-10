import unittest
import os,stat
import shutil

from file import File
from directory import Directory
from filesystem import FileSystem

# The TestIntegrationFileSystem class is a unit test case for testing the integration of the file
# system.
class TestIntegrationFileSystem(unittest.TestCase):
    def setUp(self):
        """
        The setUp function initializes a FileSystem object for testing purposes.
        """
        # Set up a FileSystem for testing
        self.fs = FileSystem()

    def test_integration(self):
        """
        The `test_integration` function tests the integration of various file system operations such as
        creating directories, changing directories, creating files, writing to files, reading files,
        showing file statistics, checking file existence, checking disk usage, removing files, and
        removing directories.
        """
        # Create a new directory
        dir_name = "integration_test_dir"
        self.fs.create_directory(dir_name)
        self.assertTrue(os.path.isdir(dir_name))

        # Change to the new directory
        self.fs.change_directory(dir_name)
        self.assertEqual(os.getcwd(), self.fs.current_directory)

        # Create a new file in the directory
        file_name = "integration_test.txt"
        self.fs.create_file(file_name)
        self.assertTrue(os.path.isfile(file_name))

        # Write to the file
        content = "Test integration."
        file = File(file_name, "user", "group", 0o644)
        file.write(content)

        # Read the file and verify the contents
        self.assertEqual(file.read(), content)


        stats = self.fs.show_stats(file_name)
        self.assertIsNotNone(stats) 


        print("Current directory:", os.getcwd())
        print("File exists:", os.path.isfile(file_name))

        size = self.fs.disk_usage(file_name)
        self.assertEqual(size, len(content))  

        # Delete the file
        self.fs.remove_file(file_name)
        self.assertFalse(os.path.isfile(file_name))


        self.fs.remove_directory(dir_name)
        self.assertFalse(os.path.isdir(dir_name))

    def tearDown(self):
        # Cleans up any files or directories created during testing
        dir_name = "integration_test_dir"
        file_name = os.path.join(dir_name, "integration_test.txt")
        if os.path.isfile(file_name):
            os.remove(file_name)
        if os.path.isdir(dir_name):
            os.rmdir(dir_name)

if __name__ == '__main__':
    unittest.main()