import unittest
import tempfile
import os
from workforce import load_roles_from_file

class TestWorkforce(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.valid_roles_path = os.path.join(self.test_dir.name, "valid_roles.md")
        self.malformed_roles_path = os.path.join(self.test_dir.name, "malformed_roles.md")

        # Valid roles content
        with open(self.valid_roles_path, "w") as f:
            f.write("Employee 1: CEO - Leads the company\n")
            f.write("Employee 2: CTO - Technical leadership\n")

        # Malformed roles content
        with open(self.malformed_roles_path, "w") as f:
            # Valid line
            f.write("Employee 1: CEO - Leads the company\n")
            # Missing ID
            f.write("Employee : CTO - Technical leadership\n")
            # Non-integer ID
            f.write("Employee A: CTO - Technical leadership\n")
            # Missing colon
            f.write("Employee 3 CTO - Technical leadership\n")
            # Missing dash
            f.write("Employee 4: CTO Technical leadership\n")
            # Complete garbage
            f.write("Just some random text\n")
            # Another valid line
            f.write("Employee 5: Dev - Writes code\n")

    def tearDown(self):
        # Cleanup temporary directory
        self.test_dir.cleanup()

    def test_load_roles_happy_path(self):
        """Test that valid roles are correctly loaded."""
        roles = load_roles_from_file(self.valid_roles_path)
        self.assertEqual(len(roles), 2)

        self.assertEqual(roles[0]["id"], 1)
        self.assertEqual(roles[0]["title"], "CEO")
        self.assertEqual(roles[0]["description"], "Leads the company")

        self.assertEqual(roles[1]["id"], 2)
        self.assertEqual(roles[1]["title"], "CTO")
        self.assertEqual(roles[1]["description"], "Technical leadership")

    def test_load_roles_malformed_data(self):
        """Test that malformed lines are safely skipped."""
        roles = load_roles_from_file(self.malformed_roles_path)

        # Only the 2 valid lines should be parsed
        self.assertEqual(len(roles), 2)

        # First valid line
        self.assertEqual(roles[0]["id"], 1)
        self.assertEqual(roles[0]["title"], "CEO")
        self.assertEqual(roles[0]["description"], "Leads the company")

        # Second valid line
        self.assertEqual(roles[1]["id"], 5)
        self.assertEqual(roles[1]["title"], "Dev")
        self.assertEqual(roles[1]["description"], "Writes code")

    def test_load_roles_file_not_found(self):
        """Test that a non-existent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_roles_from_file("non_existent_file.md")

if __name__ == '__main__':
    unittest.main()
