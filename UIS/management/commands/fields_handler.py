def fields():

    exported_read_fields = dict(
        [
            ('DEPARTMENTS', [None, 'name_ar', 'name']),
            ('COURSES', ['code', 'name', 'name_ar', None,
                         'department', 'credit', None,
                         None, None, None, None, None,
                         None, None, None, None, None,
                         None, None]),
            ('STUDENTS', ['registration_number', 'name_ar',
                          'date_of_birth', None, 'nationality', None,
                          'gender', None, None,
                          'name']),
            ('REGISTRATION', ['registration_number',
                              None, None, None,
                              'period', None, 'code',
                              'group', 'grade',
                              'added_or_dropped',
                              'credit',
                              None, None, None,
                              None, None, None,
                              None, None, None,
                              None, None, None,
                              None, 'registration_type',
                              None, 'status', None, None,
                              None, None, None]),
            ('SUMMARY', ['registration_number', 'period',
                         'registration_type']),
        ])
    exported_read_fields_archive = exported_read_fields.copy()
    exported_read_fields_archive['STUDENTS'].extend(
        ("archive_reason", None, None)
    )
    exported_read_fields_main = exported_read_fields.copy()
    exported_read_fields_main['STUDENTS'].extend(
        (None,)
    )


    prepared_write_fields = dict(
        [
            ('DEPARTMENTS', ['name_ar', 'name']),
            ('COURSES', ['code', 'name_ar', 'name', 'department',
                         'credit']),
            ('STUDENTS', ['registration_number', 'first_name_ar',
                          'last_name_ar', 'first_name', 'last_name',
                          'archive_reason', 'gender', 'nationality',
                          'date_of_birth']),
            ('REGISTRATION', ['registration_number',
                              'period',
                              'academic_year',
                              'code',
                              'credit',
                              'group',
                              'grade',
                              'registration_type',
                              'added_or_dropped',
                              'status']),
            ('SUMMARY', ['registration_number',
                         'period', 'academic_year',
                         'registration_type'])
        ])

    process_fields = dict(
        [
            ('DEPARTMENTS', ['name_ar', 'name']),
            ('COURSES', ['code', 'name_ar', 'name',
                         'department', 'credit']),
            ('STUDENTS', ['registration_number',
                          'first_name_ar', 'last_name_ar',
                          'first_name', 'last_name',
                          'archive_reason', 'gender', 'nationality',
                          'date_of_birth']),
            ('SUMMARY', ['registration_number',
                         'period', 'academic_year',
                         'registration_type']),
            ('REGISTRATION', ['registration_number', 'period',
                              'academic_year', 'code', 'credit',
                              'group', 'grade', 'registration_type',
                              'added_or_dropped', 'status'])
        ])

    fields = dict(
        [
            ('Register.mde', dict(
                [
                    ('exported_read_fields', exported_read_fields_main),
                    ('prepared_write_fields', prepared_write_fields),
                    ('process_fields', process_fields),
                ]
             )),
             ('DBArchive.MDE', dict(
                 [
                     ('exported_read_fields', exported_read_fields_archive),
                     ('prepared_write_fields', prepared_write_fields),
                     ('process_fields', process_fields),
                 ]
             ))
        ])

    return fields
