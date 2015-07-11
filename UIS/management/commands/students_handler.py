import unicodecsv
from general_handlers import registration_number_handler
from django.db import IntegrityError
from UIS.models.users import UISUser, UserProfile
from UIS.models.students import Student


def students_table_read(file, fieldnames, rows):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        for row in reader:
            row['first_name_ar'], row['last_name_ar'] = (
                row['first_name_ar'].partition(' ')[0],
                row['first_name_ar'].partition(' ')[2]
            )
            row['first_name'], row['last_name'] = (
                row['first_name'].partition(' ')[0],
                row['first_name'].partition(' ')[2]
            )
            row.pop(None, None)
            row.pop('')
            rows.append(row)


def students_table_write(file, fieldnames, rows):
    with open(file, 'w') as csvfile:
        writer = unicodecsv.DictWriter(
            csvfile, fieldnames)
        writer.writeheader()
        for row in rows:
            registration_number_handler(row)
            writer.writerow(row)


def students_table_process(file, fieldnames, conflicts, verbosity):
    with open(file, 'rb') as csvfile:
        reader = unicodecsv.DictReader(
            csvfile, fieldnames)
        next(reader, None)
        for row in reader:
            try:
                student, student_msg = Student.objects.get_or_create(
                    first_name=row['first_name'],
                    first_name_ar=row['first_name_ar'],
                    last_name=row['last_name'],
                    last_name_ar=row['last_name_ar'],
                    registration_number=row['registration_number'],
                )
            except IntegrityError:
                conflicts.write(
                    "Student with registration number {} "
                    "has some kind of conflict, probably a name "
                    "conflict\n".format(row['registration_number'],))
                continue

            if verbosity > 1:
                if student_msg:
                    print("Created student {}".format(
                        row['registration_number']
                    ))
                    user, user_msg = UISUser.objects.get_or_create_user(
                        email=(row['registration_number'] +
                               '@students.uot.edu.ly'),
                        password=row['registration_number'][::-1])
                    if user_msg:
                        UserProfile.objects.create(user=user, profile=student)
                    if verbosity > 1:
                        if user_msg:
                            print("Created user {}".format(
                                row['registration_number']
                            ))
