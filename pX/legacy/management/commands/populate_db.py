import random
from django.core.management.base import BaseCommand
from UIS.models.administration import Faculty, Department
from UIS.models.courses import (Course, PeriodCourse,
                                Section)
from UIS.models.time_period import Period
from UIS.models.users import UISUser
from UIS.models.employees import Employee
from UIS.models.students import (Student, SectionEnrolment,
                                 StudentRegistration, StudentDegree)
from UIS.models.degrees import Degree, DegreeCourse


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def add_arguments(self, parser):
        parser.add_argument('--flush',
                            action='store_true',
                            dest='flush',
                            default=False,
                            help='Delete fixtures instead of closing it')

    def _create_faculties(self):
        Faculty.objects.create(name='Faculty of Engineering')

    def _create_departments(self):
        Department.objects.create(
            name='Department of Aeronautical Engineering',
            faculty=Faculty.objects.get(pk=1),
            domain_name='aero.eng.edu.ly'
        )

    def _create_courses(self):
        for j in [101, 201, 301, 401, 501]:
            for i in range(j, j+5):
                Course.objects.create(
                    code='AE'+str(i),
                    level=i/100*100,
                    name='Course '+str(i),
                    department=Department.objects.get(pk=1),
                    credit=3,
                )

    def _create_periods(self):
        for j in range(0, 4):
            for i in [(2010, 2011), (2011, 2012), (2012, 2013),
                      (2013, 2014), (2014, 2015)]:
                Period.objects.create(
                    period=j,
                    academic_year=','.join(str(x) for x in i)
                )

    def _create_period_courses(self):
        for i in Period.objects.exclude(period=0):
            for j in Course.objects.all():
                PeriodCourse.objects.create(period=i, course=j)

    def _create_sections(self):
        for i in PeriodCourse.objects.all():
            Section.objects.create(period_course=i)

    def _create_users(self):
        for i in range(1,6):
            UISUser.objects.create_user(first_name='Student ' + str(i),
                                   last_name='Student ' + str(i),
                                   email=('student' +
                                          str(i)+'@students.uot.edu.ly'),
                                        password='12345'
                                   )
            Student.objects.create(user=UISUser.objects.get(
                email__startswith='student'+str(i)),
                                   registration_number=i)
        for i in range(1,4):
            UISUser.objects.create_user(first_name='Employee ' + str(i),
                                        last_name='Employee ' + str(i),
                                        email=(
                                            'employee'+
                                            str(i)+
                                            '@aero.eng.uot.edu.ly'),
                                        user_type='E',
                                        password='12345')
            Employee.objects.create(
                user=UISUser.objects.get(
                    email__startswith='employee'+str(i)),
                username='employee'+str(i),
                department=Department.objects.all()[0],
            )

    def _create_degrees(self):
        Degree.objects.create(level='U',
                              name='Bachelor of Aeronautical Engineering',
                              department=Department.objects.get(pk=1),
                              credits_required=85,)

    def _create_degree_courses(self):
        for i in Course.objects.all():
            DegreeCourse.objects.create(degree=Degree.objects.all()[0],
                                        course=i)

    def _create_students_registration(self):
        for i in Student.objects.all():
            for j in Period.objects.exclude(period=0):
                StudentRegistration.objects.create(student=i,
                                                   period=j,
                                                   registration_type='R')
        # for i in StudentRegistration.objects.all():
        #     i.degrees.add(Degree.objects.get(pk=1))

    def _create_student_degree(self):
        for j in StudentRegistration.objects.all():
            StudentDegree.objects.create(student_registration=j,
                                         degree=Degree.objects.all()[0]
                                     )

    def _create_student_enrolments(self):
        for i in range(1,6):
            for j in range(1,6):
                period = Period.objects.get(academic_year='2010,2011',
                                            period=1)
                SectionEnrolment.objects.create(
                    student=Student.objects.get(user__first_name='Student '+str(i)),
                    section=Section.objects.get(
                        period_course__course__code='AE10'+str(j),
                        period_course__period=period),
                    grade=random.randint(0,100))
                period = Period.objects.get(academic_year='2010,2011',
                                            period=2)
                SectionEnrolment.objects.create(
                    student=Student.objects.get(user__first_name='Student '+str(i)),
                    section=Section.objects.get(
                        period_course__course__code='AE20'+str(j),
                        period_course__period=period),
                    grade=random.randint(0,100))

    def _delete_faculties(self):
        Faculty.objects.all().delete()

    def _delete_departmenties(self):
        Department.objects.all().delete()

    def _create_all(self):
        self._create_faculties()
        self._create_departments()
        self._create_courses()
        self._create_periods()
        self._create_period_courses()
        self._create_sections()
        self._create_users()
        self._create_degrees()
        self._create_degree_courses()
        self._create_students_registration()
        self._create_student_degree()
        self._create_student_enrolments()
    def _flush_all(self):
        self._delete_faculties()
        self._delete_departments()

    def handle(self, *args, **options):
        if options['flush']:
            self._flush_all()
        else:
            self._create_all()
