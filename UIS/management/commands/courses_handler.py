import unicodecsv
import re
from django.db import IntegrityError
from UIS.models.administration import Department
from UIS.models.courses import Course

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
            else:
                department = Department.objects.get(
                    pk=row['department'])
                row.pop('department')
                try:
                    course = Course.objects.get(
                        code=row['code'],
                        department=department,
                        level = int(
                            re.search(
                                '\d+', row['code']
                            ).group()[0]
                        )*100,
                        credit=row['credit'],
                        name=row['name'].title()
                    )
                except Course.DoesNotExist:
                    course = Course.objects.create(
                        code=row['code'],
                        department=department,
                        level = int(
                            re.search(
                                '\d+', row['code']
                            ).group()[0]
                        )*100,
                        credit=row['credit'],
                        name=row['name'].title()
                    )
                    if verbosity > 1:
                        print("Created {}".format(row['code'],))
