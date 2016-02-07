import unicodecsv
from django.db import IntegrityError
from ....administration.models import Faculty, Department


def departments_table_read(file, fieldnames, rows):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        for row in reader:
            row.pop('')
            rows.append(row)


def departments_table_write(file, fieldnames, rows):
    with open(file, 'w') as csvfile:
        writer = unicodecsv.DictWriter(
            csvfile, fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def departments_table_process(file, fieldnames, conflicts, verbosity):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        next(reader, None)
        for row in reader:
            try:
                department, msg = Department.objects.get_or_create(
                    faculty=Faculty.objects.get_or_create(
                        name='Faculty of Engineering')[0],
                    name=row['name'].title(),
                    name_ar=row['name_ar'].title())
            except IntegrityError:
                conflicts.write(
                    "Department ' {}/{}  ''"
                    "has some kind of conflict, probably a name "
                    "conflict\n".format(
                        row['name'],
                        row['name_ar'].encode("UTF-8")))
                continue

            if verbosity > 1:
                if msg:
                    print('Created {}'
                          .format(row['name']))
