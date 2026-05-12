import re

class SharedMemory:
    """
    A shared memory framework to facilitate seamless collaboration and information exchange
    between employees in the distributed AI workforce.
    """
    def __init__(self):
        self._memory = []

    def write(self, employee_name, message):
        """Write a message to the shared memory."""
        entry = f"[{employee_name}]: {message}"
        self._memory.append(entry)
        # In a real distributed system, this would notify other agents.

    def read_all(self):
        """Read all messages from the shared memory."""
        return list(self._memory)

    def search(self, keyword):
        """Search shared memory for a specific keyword."""
        return [entry for entry in self._memory if keyword.lower() in entry.lower()]


class Employee:
    """
    Represents an AI employee within the workforce.
    """
    def __init__(self, id, title, description, shared_memory):
        self.id = id
        self.title = title
        self.description = description
        self.shared_memory = shared_memory

    def collaborate(self, message):
        """Share information or collaborate with the workforce."""
        self.shared_memory.write(f"Employee {self.id} ({self.title})", message)

    def read_updates(self):
        """Read all updates from the shared memory."""
        return self.shared_memory.read_all()

    def __str__(self):
        return f"Employee {self.id}: {self.title} - {self.description}"


def load_roles_from_file(filepath):
    """
    Load employee roles from a markdown file.
    Expects lines in the format:
    Employee <ID>: <Title> - <Description>
    """
    employees_data = []
    with open(filepath, 'r') as f:
        content = f.read()

    # Regex to parse the employee lines
    pattern = re.compile(r"Employee\s+(\d+):\s+(.*?)\s+-\s+(.*)")
    for match in pattern.finditer(content):
        emp_id = int(match.group(1))
        title = match.group(2).strip()
        description = match.group(3).strip()
        employees_data.append({
            "id": emp_id,
            "title": title,
            "description": description
        })
    return employees_data

def main():
    # Initialize shared memory framework
    shared_memory = SharedMemory()
    print("Shared Memory Framework Initialized.")

    # Load employee roles
    roles_data = load_roles_from_file("roles.md")

    employees = []
    for data in roles_data:
        emp = Employee(data['id'], data['title'], data['description'], shared_memory)
        employees.append(emp)

    print(f"Successfully onboarded {len(employees)} employees.")
    print("--- Workforce Roster ---")
    for emp in employees:
        print(emp)

    print("\n--- Collaboration Test ---")
    if len(employees) >= 2:
        employees[0].collaborate("We need to prioritize the new predictive analytics model deployment.")
        employees[1].collaborate("Agreed. I will coordinate with the DevOps Engineer to set up the CI/CD pipeline.")

        updates = employees[2].read_updates()
        print("Data Scientist reads shared memory:")
        for update in updates:
            print("  " + update)

if __name__ == "__main__":
    main()
