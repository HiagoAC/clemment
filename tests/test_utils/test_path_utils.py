from unittest import TestCase
from unittest.mock import patch
from pathlib import Path

from src.clemment.utils.path_utils import get_absolute_path


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
