from http.server import BaseHTTPRequestHandler
import sys
import os

# Add the parent directory to sys.path so we can import workforce
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workforce import SharedMemory, Employee, load_roles_from_file

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        # Initialize shared memory framework
        shared_memory = SharedMemory()

        output = ["Shared Memory Framework Initialized."]

        # Load employee roles
        roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "roles.md")
        roles_data = load_roles_from_file(roles_path)

        employees = []
        for data in roles_data:
            emp = Employee(data['id'], data['title'], data['description'], shared_memory)
            employees.append(emp)

        output.append(f"Successfully onboarded {len(employees)} employees.")
        output.append("--- Workforce Roster ---")
        for emp in employees:
            output.append(str(emp))

        output.append("\n--- Collaboration Test ---")
        if len(employees) >= 2:
            employees[0].collaborate("We need to prioritize the new predictive analytics model deployment.")
            employees[1].collaborate("Agreed. I will coordinate with the DevOps Engineer to set up the CI/CD pipeline.")

            updates = employees[2].read_updates()
            output.append("Data Scientist reads shared memory:")
            for update in updates:
                output.append("  " + update)

        self.wfile.write("\n".join(output).encode('utf-8'))
        return
