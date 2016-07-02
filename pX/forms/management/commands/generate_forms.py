# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.core.management.base import BaseCommand

from pX.students.models import Student


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'Generate form 2 for students'

    def add_arguments(self, parser):
        parser.add_argument('--form-type',
                            dest='form_type',
                            required=True,
                            choices=['Enrolment Form',
                                     'Academic Progress'])
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-a', '--all',
                           action='store_true',
                           dest='all',
                           default=False,
                           help='Generate for all students')
        group.add_argument('--students', nargs='*')

    def _generate_form(self, student, form_type):

        if self.verbosity > 1:
            print("Generating {} for student {}"
                  .format(form_type, student))

        return student.generate_form(form_type)
        # print(student.get_allowed_enrolments())

    def _generate_for_all(self, form_type):

        exclusion = [
                    #AE325
                    '021101269',
                    '022120950',
                    '021714315',
                    '022122045',
                    '021090784',
                    '022131953',
                    '022120324',
                    '022123411',
                    '021100854',
                    '021090776',
                    '021090774',
                    '021090765',
                    '021101001',
                    '021100608',
                    '021900998',
                    '021104277',
                    '022132023',
                    '021101259',
                    #EPM
                    '021101118',
                    '021129103',
                    '02205096',
                    '021028243',
                    '021101003',
                    '021100287',
                    '022855007',
                    '021123012',]
                    # below student is not registered at all
                    # '02214159'
                # ]
        for i, student in enumerate(Student.objects.filter(status='E', registration_number__in=exclusion), 1):
            if self.verbosity > 1:
                print("{}- "
                .format(i), end="")

            self._generate_form(student, form_type)


    def handle(self, *args, **options):

        self.verbosity = options.get('verbosity')
        form_type = options['form_type']

        if options['all']:
            self._generate_for_all(form_type)
        else:
            for student_registration_number in options['students']:
                student = Student.objects.get(
                    registration_number=student_registration_number)
                self._generate_form(student, form_type)
