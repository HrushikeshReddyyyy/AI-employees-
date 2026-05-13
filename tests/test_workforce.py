import unittest
from workforce import load_roles_from_file

class TestWorkforce(unittest.TestCase):
    def test_load_roles_from_file_not_found(self):
        """Test that load_roles_from_file raises FileNotFoundError for non-existent file."""
        with self.assertRaises(FileNotFoundError):
            load_roles_from_file("non_existent_file.md")

if __name__ == '__main__':
    unittest.main()
