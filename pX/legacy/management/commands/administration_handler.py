# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unicodecsv

from pX.administration.models import Department
from pX.administration.degrees.models import Degree
from pX.administration.courses.models import (Course, CoursePrerequisite,
                                              DegreeCourse)
from .utils import verbose_message
from .departments_handler import departments_table_process


def create_departments(config):
    conflicts_file = (config['LOGS_FILES_LOCATION'] +
                      '/' + 'DEPARTMENT_CONFLICTS.txt')
    conflicts = open(conflicts_file, 'w')

    for file in config['FILES']:
        prepared_file = (
            config['PREPARED_FILES_LOCATION'] + '/' + 'departments' +
            '_' + file[:-4] + '.csv'
        )
        departments_table_process(
            prepared_file,
            config['FIELDS'][file].get('process_fields').get('DEPARTMENTS'),
            conflicts, config['VERBOSITY'])

    conflicts.close()


def create_degrees(config):
    degree, msg = Degree.objects.get_or_create(
        level='U',
        name='Bachelor of Aeronautical Engineering',
        department=Department.objects.get(pk=1),
        credits_required=152,
    )
    if config['VERBOSITY'] > 1 and msg:
        print('Created degree {}'.format(degree))


def create_degree_courses(file):
    verbosity = 2
    degree = Degree.objects.all()[0]
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames=['code', 'pre1', 'pre2']
            )
        for row in reader:
            courses = Course.objects.filter(code=row['code'])
            for c in courses:
                if (c.code in ['AE325', 'AE200'] and c.credit == 2):
                    continue
                degree_course = DegreeCourse.objects.filter(
                    degree=degree, course__code=c.code)
                if not degree_course.exists():
                    DegreeCourse.objects.create(
                        degree=degree, course=c)
                    verbose_message(
                        2,
                        {'2': "Got {} and added it to {}"
                              .format(row['code'], degree)}
                        )
                if row['pre1'] != '':
                    # print row['pre1']
                    CoursePrerequisite.objects.get_or_create(
                        course=c,
                        prerequisite=Course.objects.filter(
                            code=row['pre1'])[0])
                    verbose_message(
                        verbosity,
                        {2: "Added {} as a prerequisite for {}"
                            .format(row['pre1'], row['code'])}
                    )
                if row['pre2'] != '':
                    CoursePrerequisite.objects.get_or_create(
                        course=c,
                        prerequisite=Course.objects.filter(
                            code=row['pre2'])[0])
                    verbose_message(
                        2,
                        {'2': "Added {} as a prerequisite for {}"
                              .format(row['pre2'], row['code'])}
                    )
def create_employees(data):

    users = [
        {
            'first_name': 'Abdulhaq',
            'last_name': 'Emhemmed',
            'first_name_ar': 'عبدالحق',
            'last_name_ar': 'السعيد امحمد',
            'email': 'abdulhaq.emhemmed@aero.eng.uot.edu.ly',
            'password': '12345',
            'username': 'abdulhaq.emhemmed'
        },
        {
            'first_name': 'Ahmed',
            'last_name': 'Almakhlofy',
            'first_name_ar': 'أحمد',
            'last_name_ar': 'المخلوفي',
            'email': 'ahmed@aero.eng.uot.edu.ly',
            'password': '12345',
            'username': 'ahmed'
        },
        {
            'first_name': 'Adel',
            'last_name': 'Kurban',
            'first_name_ar': 'عادل',
            'last_name_ar': 'كربان',
            'email': 'kurban@aero.eng.uot.edu.ly',
            'password': '12345',
            'username': 'kurban'
        },
        {
            'first_name': 'Ashraf',
            'last_name': 'Omar',
            'first_name_ar': 'أشرف',
            'last_name_ar': 'عمر',
            'email': 'ashraf@aero.eng.uot.edu.ly',
            'password': '12345',
            'username': 'ashraf'
        }
    ]

    for a in users:
        try:
            employee = Employee.objects.get(
                username=a['username'],
                department=Department.objects.get(name__icontains='aero'))
        except Employee.DoesNotExist:
            employee = Employee.objects.create(
                username=a['username'],
                department=Department.objects.get(name__icontains='aero'),
                first_name=a['first_name'],
                last_name=a['last_name'],
                first_name_ar=a['first_name_ar'],
                last_name_ar=a['last_name_ar'])
            if self.verbosity > 1:
                print ('Created employee {}'
                       .format(employee))
        if a['username'] == 'abdulhaq.emhemmed':
            try:
                user = pXUser.objects.get(
                    email='aaa@aaa.com'
                )
            except pXUser.DoesNotExist:
                user = pXUser.objects.create_superuser(
                    email='aaa@aaa.com',
                    password='123')
                if self.verbosity > 1:
                    print('Created superuser {}'
                          .format(user.email))
            try:
                user_profile = UserProfile.objects.get(
                    user=user, profile_id=employee.pk
                )
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(
                    user=user, profile=employee
                )
        try:
            user = pXUser.objects.get(
                email=a['username']+'@aero.eng.uot.edu.ly'
            )
        except pXUser.DoesNotExist:
            user = pXUser.objects.create(
                email=a['username']+'@aero.eng.uot.edu.ly',
                password='12345')
            if self.verbosity > 2:
                print('Created user {}'
                      .format(user.email))
        try:
            user_profile = UserProfile.objects.get(
                user=user, profile_id=employee.pk
            )
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(
                user=user, profile=employee
            )
