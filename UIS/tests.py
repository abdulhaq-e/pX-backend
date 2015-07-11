from django.test import TestCase
from UIS.models import Employee, Student

class EmployeeMethodTest(TestCase):

    def test_employee_name_displayed_correctly(self):
        employee = Employee(first_name_ar='John', last_name_ar='Smith')

        self.assertEqual(str(employee), 'John Smith')
# Create your tests here.
