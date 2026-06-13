import unittest
import os
import tempfile
from workforce import SharedMemory, Employee, load_roles_from_file

class TestSharedMemory(unittest.TestCase):
    def setUp(self):
        self.shared_memory = SharedMemory()

    def test_init(self):
        self.assertEqual(self.shared_memory._memory, [])

    def test_write(self):
        self.shared_memory.write("Alice", "Hello, world!")
        self.assertEqual(self.shared_memory._memory, ["[Alice]: Hello, world!"])

    def test_read_all(self):
        self.shared_memory.write("Bob", "Message 1")
        self.shared_memory.write("Charlie", "Message 2")
        self.assertEqual(self.shared_memory.read_all(), ["[Bob]: Message 1", "[Charlie]: Message 2"])
        # Ensure it returns a copy
        read_list = self.shared_memory.read_all()
        read_list.append("Fake")
        self.assertNotEqual(self.shared_memory._memory, read_list)

    def test_search(self):
        self.shared_memory.write("Dave", "I love apples")
        self.shared_memory.write("Eve", "Oranges are better")
        self.shared_memory.write("Frank", "Apples and bananas")

        self.assertEqual(self.shared_memory.search("apples"), ["[Dave]: I love apples", "[Frank]: Apples and bananas"])
        self.assertEqual(self.shared_memory.search("ORANGES"), ["[Eve]: Oranges are better"])
        self.assertEqual(self.shared_memory.search("grapes"), [])


class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.shared_memory = SharedMemory()
        self.employee = Employee(1, "Data Scientist", "Analyzes data", self.shared_memory)

    def test_init(self):
        self.assertEqual(self.employee.id, 1)
        self.assertEqual(self.employee.title, "Data Scientist")
        self.assertEqual(self.employee.description, "Analyzes data")
        self.assertIs(self.employee.shared_memory, self.shared_memory)

    def test_collaborate(self):
        self.employee.collaborate("Found some trends")
        self.assertEqual(self.shared_memory.read_all(), ["[Employee 1 (Data Scientist)]: Found some trends"])

    def test_read_updates(self):
        self.shared_memory.write("Another Employee", "Some other update")
        self.assertEqual(self.employee.read_updates(), ["[Another Employee]: Some other update"])

    def test_str(self):
        self.assertEqual(str(self.employee), "Employee 1: Data Scientist - Analyzes data")


class TestLoadRolesFromFile(unittest.TestCase):
    def setUp(self):
        self.fd, self.temp_filepath = tempfile.mkstemp(dir=os.getcwd())
        with os.fdopen(self.fd, 'w') as f:
            f.write("Employee 1: Developer - Writes code\n")
            f.write("Employee 2: Tester - Tests code\n")

    def tearDown(self):
        os.remove(self.temp_filepath)

    def test_load_roles_from_file(self):
        roles = load_roles_from_file(self.temp_filepath)
        self.assertEqual(len(roles), 2)

        self.assertEqual(roles[0]['id'], 1)
        self.assertEqual(roles[0]['title'], "Developer")
        self.assertEqual(roles[0]['description'], "Writes code")

        self.assertEqual(roles[1]['id'], 2)
        self.assertEqual(roles[1]['title'], "Tester")
        self.assertEqual(roles[1]['description'], "Tests code")

    def test_load_roles_empty(self):
        fd, temp_empty = tempfile.mkstemp(dir=os.getcwd())
        os.close(fd)
        try:
            roles = load_roles_from_file(temp_empty)
            self.assertEqual(roles, [])
        finally:
            if os.path.exists(temp_empty):
                os.remove(temp_empty)

if __name__ == '__main__':
    unittest.main()
