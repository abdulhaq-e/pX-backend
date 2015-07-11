def registration_number_handler(row):
        if row['registration_number'][0] != '0':
            row['registration_number'] = (
                '0' + row['registration_number']
            )


def period_handler(row):
    row['period'] = str(row['period'])
    if row['period'].endswith('Z'):
        row['academic_year'] = (
            row['period'][0:4] + ',' +
            str(int(row['period'][0:4])+1)
        )
        row['period'] = 1
    elif row['period'].endswith('S'):
        row['academic_year'] = (
            str(int(row['period'][0:4])-1) + ',' +
            row['period'][0:4]
        )
        row['period'] = 2
    elif row['period'].endswith('U'):
        row['academic_year'] = (
            str(int(row['period'][0:4])-1) + ',' +
            row['period'][0:4]
        )
        row['period'] = 3
