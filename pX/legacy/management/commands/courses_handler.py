import unicodecsv
import re
# from django.db import IntegrityError
from ....administration.models import Department
from ....administration.courses.models import Course

codes = []


def courses_table_read(file, fieldnames, rows):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        for row in reader:
            if row['code'] in codes:
                continue
            else:
                row.pop('')
                rows.append(row)
                codes.append(row['code'])


def courses_table_write(file, fieldnames, rows):
    with open(file, 'w') as csvfile:
        writer = unicodecsv.DictWriter(
            csvfile, fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def courses_table_process(file, fieldnames, conflicts, verbosity):

    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        next(reader, None)
        for row in reader:
            if row['name'] == 'NON_EQUIVALENT COURSE':
                continue

            department = Department.objects.get(
                pk=row['department'])
            row.pop('department')
            try:
                Course.objects.get(
                    code=row['code'],
                    department=department,
                    level=int(
                        re.search(
                            '\d+', row['code']
                        ).group()[0]
                    )*100,
                    credit=row['credit'],
                    name=row['name'].title()
                )
            except Course.DoesNotExist:
                Course.objects.create(
                    code=row['code'],
                    department=department,
                    level=int(
                        re.search(
                            '\d+', row['code']
                        ).group()[0]
                    )*100,
                    credit=row['credit'],
                    name=row['name'].title()
                )
                if verbosity > 1:
                    print("Created {}".format(row['code'],))


def create_courses(config):
    conflicts_file = (config['LOGS_FILES_LOCATION'] +
                      '/' + 'COURSE_CONFLICTS.txt')
    conflicts = open(conflicts_file, 'w')

    for file in config['FILES']:
        prepared_file = (
            config['PREPARED_FILES_LOCATION'] + '/' + 'courses' +
            '_' + file[:-4] + '.csv'
        )
        courses_table_process(
            prepared_file,
            config['FIELDS'][file].get('process_fields').get('COURSES'),
            conflicts,
            config['VERBOSITY'])

    conflicts.close()
