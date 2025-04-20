import os
from unittest import TestCase
from unittest.mock import patch
from pathlib import Path

from src.clemment.utils.path_utils import get_absolute_path, discover_files


class TestPathUtils(TestCase):
    def setUp(self):
        self.patcher = patch(
            'src.clemment.utils.path_utils.PROJECT_ROOT',
            Path('/project/root/')
        )
        self.mock_project_root = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_get_absolute_path_success(self):
        """
        Test get_absolute_path returns the absolute path of a file in clemment.
        """
        filename = "filename"
        subdir1 = "subdir1"
        subdir2 = "subdir2"
        subdirs = [subdir1, subdir2]

        res = get_absolute_path(filename, subdirs)

        self.assertEqual(
            res, str(self.mock_project_root / subdir1 / subdir2 / filename))
    
    def test_discover_files_success(self):
        """
        Test discover_files returns a list of files in a directory and its
        subdirectories.
        """
        path = Path('/project/root/subdir1')
        subdirs = ['subdir2', 'subdir3']
        file1 = 'file1'
        file2 = 'file2'
        file3 = 'file3'

        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [
                (path, subdirs, [file1, file2]),
                (path / subdirs[0] / subdirs[1], [], [file3])
            ]
            result = discover_files(path)
            expected = [
                os.path.join(path, file1),
                os.path.join(path, file2),
                os.path.join(path, subdirs[0], subdirs[1], file3),
            ]
            print(expected)
            self.assertEqual(result, expected)
