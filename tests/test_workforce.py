import unittest
from unittest.mock import MagicMock
from workforce import Employee, SharedMemory

class TestEmployee(unittest.TestCase):

    def test_collaborate_with_real_shared_memory(self):
        """Test Employee.collaborate updates a real SharedMemory instance correctly."""
        shared_memory = SharedMemory()
        employee = Employee(1, "Software Engineer", "Writes code", shared_memory)

        test_message = "I have updated the module."
        employee.collaborate(test_message)

        updates = shared_memory.read_all()
        self.assertEqual(len(updates), 1)
        expected_entry = "[Employee 1 (Software Engineer)]: I have updated the module."
        self.assertEqual(updates[0], expected_entry)

    def test_collaborate_with_mocked_shared_memory(self):
        """Test Employee.collaborate calls write on SharedMemory with expected arguments."""
        mock_shared_memory = MagicMock()
        employee = Employee(2, "Product Manager", "Plans features", mock_shared_memory)

        test_message = "The new feature specs are ready."
        employee.collaborate(test_message)

        # Verify that write was called with the correct signature
        mock_shared_memory.write.assert_called_once_with(
            "Employee 2 (Product Manager)", test_message
        )

if __name__ == '__main__':
    unittest.main()
