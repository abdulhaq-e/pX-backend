# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
import UIS.models.users
import UIS.validators
import exclusivebooleanfield.fields
import django.db.models.deletion
from django.conf import settings
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('course_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('level', models.SmallIntegerField(null=True)),
                ('name', models.CharField(max_length=200, verbose_name='Course name', blank=True)),
                ('name_ar', models.CharField(max_length=200, verbose_name='Course name', blank=True)),
                ('is_compulsary', models.BooleanField(default=True)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('credit', models.SmallIntegerField()),
            ],
            options={
                'ordering': ['level', 'code'],
                'verbose_name': 'Course Catalogue',
                'verbose_name_plural': 'Course Catalogue',
            },
        ),
        migrations.CreateModel(
            name='CoursePrerequisite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('course', models.ForeignKey(to='UIS.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('degree_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('level', models.CharField(max_length=1, choices=[(b'U', 'Undergraduate'), (b'P', 'Postgraduate')])),
                ('name', models.CharField(max_length=60)),
                ('name_ar', models.CharField(max_length=60)),
                ('credits_required', models.SmallIntegerField()),
                ('is_major', models.BooleanField(default=True)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DegreeCourse',
            fields=[
                ('degree_course_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='UIS.Course')),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='UIS.Degree')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('name', models.CharField(unique=True, max_length=60, verbose_name='Name of Faculty')),
                ('name_ar', models.CharField(unique=True, max_length=60, verbose_name='Name of Faculty')),
                ('acronym', models.CharField(max_length=3)),
                ('domain_name', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('name', models.CharField(unique=True, max_length=60, verbose_name='Name of Faculty')),
                ('name_ar', models.CharField(unique=True, max_length=60, verbose_name='Name of Faculty')),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='Identification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('identification_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='NationalID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('national_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PassportID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('passport_number', models.CharField(max_length=255)),
                ('issue_date', models.DateField()),
                ('expiry_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('period_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('academic_year', models.CommaSeparatedIntegerField(help_text='please enter the academic year in this format:         for the year 2012-2013, enter: "2012,2013" (without quotes)', max_length=9, verbose_name='academic year')),
                ('period', models.IntegerField(choices=[(0, 'Academic Year'), (1, 'Autumn'), (2, 'Spring'), (3, 'Summer')])),
                ('set_current_period', exclusivebooleanfield.fields.ExclusiveBooleanField(default=True)),
            ],
            options={
                'ordering': ['academic_year', 'period'],
            },
        ),
        migrations.CreateModel(
            name='PeriodCourse',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('period_course_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('course_description', models.TextField(blank=True)),
                ('course_syllabus', models.TextField(blank=True)),
                ('set_course_details_as_default', models.BooleanField(default=True)),
                ('shared_groups', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='UIS.Course')),
                ('period', models.ForeignKey(to='UIS.Period')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodCourseSectionType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('period_course_section_type_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('is_compulsary', models.BooleanField(default=True)),
                ('period_course', models.ForeignKey(to='UIS.PeriodCourse')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodDegree',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('period_degree_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('is_compulsary', models.BooleanField(default=True)),
                ('degree', models.ForeignKey(to='UIS.Degree', on_delete=django.db.models.deletion.PROTECT)),
                ('period', models.ForeignKey(to='UIS.Period', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('person_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('first_name_ar', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last Name')),
                ('last_name_ar', models.CharField(max_length=50, verbose_name='last Name')),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(max_length=1, null=True, choices=[(b'M', 'Male'), (b'F', 'Female')])),
                ('nationality', django_countries.fields.CountryField(default=b'LY', max_length=2, null=True, choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo (the Democratic Republic of the)'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Cura\xe7ao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('CI', "C\xf4te d'Ivoire"), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands  [Malvinas]'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia (The)'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See  [Vatican City State]'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran (the Islamic Republic of)'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea (the Democratic People's Republic of)"), ('KR', 'Korea (the Republic of)'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'Macedonia (the former Yugoslav Republic of)'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia (the Federated States of)'), ('MD', 'Moldova (the Republic of)'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('RE', 'R\xe9union'), ('BL', 'Saint Barth\xe9lemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan (Province of China)'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Viet Nam'), ('VG', 'Virgin Islands (British)'), ('VI', 'Virgin Islands (U.S.)'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'), ('AX', '\xc5land Islands')])),
                ('address', models.CharField(max_length=45, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('id_number', models.CharField(max_length=255)),
                ('issue_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('place_of_issuing', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PersonID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('object_id', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('identification', models.ForeignKey(to='UIS.Identification')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('role', models.CharField(unique=True, max_length=100)),
                ('role_ar', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('section_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=15, blank=True)),
                ('name_ar', models.CharField(max_length=15, blank=True)),
                ('group', models.CharField(max_length=10, null=True, blank=True)),
                ('section_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='UIS.PeriodCourseSectionType')),
            ],
        ),
        migrations.CreateModel(
            name='SectionType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('section_type_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('name_ar', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnrolment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('enrolment_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('carry_marks', models.FloatField(blank=True, null=True, validators=[UIS.validators.validate_grade])),
                ('final_exam', models.FloatField(blank=True, null=True, validators=[UIS.validators.validate_grade])),
                ('grade', models.FloatField(blank=True, null=True, validators=[UIS.validators.validate_grade])),
                ('published', models.BooleanField(default=False)),
                ('section', models.ForeignKey(related_name='studentenrolment', on_delete=django.db.models.deletion.PROTECT, to='UIS.Section')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnrolmentLog',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('enrolment_log_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('enrolment_status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Added'), (b'D', b'Dropped')])),
                ('section', models.ForeignKey(related_name='studentenrolmentlog', on_delete=django.db.models.deletion.PROTECT, to='UIS.Section')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRegistration',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('student_registration_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('registration_type', models.CharField(default=b'RNC', max_length=3, choices=[('Suspended', ((b'DS', 'Disciplinary Suspension '), (b'ES', 'Exceptional Suspension'), (b'NS', 'Normal Suspension'))), (b'R', 'Registered'), (b'D', 'Dropped Out'), (b'RNC', 'Registration not completed')])),
                ('enrolments', models.ManyToManyField(to='UIS.Section', through='UIS.StudentEnrolment', blank=True)),
                ('period_degree', models.ForeignKey(to='UIS.PeriodDegree')),
            ],
            options={
                'ordering': ('student', 'period_degree__period'),
            },
        ),
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('student_results_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('period_count', models.IntegerField()),
                ('actual_period_count', models.IntegerField()),
                ('registered_credits', models.FloatField()),
                ('passed_credits', models.FloatField()),
                ('repeated_credits', models.FloatField()),
                ('cumulative_registered_credits', models.FloatField()),
                ('cumulative_passed_credits', models.FloatField()),
                ('scored_points', models.FloatField()),
                ('passed_points', models.FloatField()),
                ('repeated_points', models.FloatField()),
                ('cumulative_scored_points', models.FloatField()),
                ('GPA', models.FloatField()),
                ('cumulative_GPA', models.FloatField()),
                ('student_registration', models.OneToOneField(to='UIS.StudentRegistration')),
            ],
            options={
                'ordering': ('student_registration',),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('user_profile_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('profile_id', models.UUIDField()),
                ('profile_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('object_id', models.UUIDField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('role', models.ForeignKey(to='UIS.Role')),
            ],
        ),
        migrations.CreateModel(
            name='UISUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('user_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('roles', models.ManyToManyField(to='UIS.Role', through='UIS.UserRole')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', UIS.models.users.UISUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('details', models.OneToOneField(parent_link=True, to='UIS.Person')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', b'invalid')])),
            ],
            bases=('UIS.person',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('details', models.OneToOneField(parent_link=True, to='UIS.Person')),
                ('registration_number', models.CharField(unique=True, max_length=255, verbose_name='Student UUID')),
                ('status', models.CharField(default=b'E', max_length=1, choices=[(b'E', b'Enrolled'), (b'G', b'Graduated'), (b'L', b'Left'), (b'D', b'Dropped Out'), (b'T', b'Transferred'), (b'K', b'Kicked Out')])),
            ],
            bases=('UIS.person',),
        ),
        migrations.AddField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentenrolmentlog',
            name='student_registration',
            field=models.ForeignKey(related_name='studentenrolmentlog', on_delete=django.db.models.deletion.PROTECT, to='UIS.StudentRegistration'),
        ),
        migrations.AddField(
            model_name='studentenrolment',
            name='student_registration',
            field=models.ForeignKey(related_name='studentenrolment', on_delete=django.db.models.deletion.PROTECT, to='UIS.StudentRegistration'),
        ),
        migrations.AddField(
            model_name='personid',
            name='person',
            field=models.ForeignKey(to='UIS.Person'),
        ),
        migrations.AddField(
            model_name='person',
            name='identifications',
            field=models.ManyToManyField(to='UIS.Identification', through='UIS.PersonID'),
        ),
        migrations.AddField(
            model_name='periodcoursesectiontype',
            name='section_type',
            field=models.ForeignKey(to='UIS.SectionType'),
        ),
        migrations.AddField(
            model_name='periodcourse',
            name='section_types',
            field=models.ManyToManyField(to='UIS.SectionType', through='UIS.PeriodCourseSectionType'),
        ),
        migrations.AddField(
            model_name='period',
            name='courses',
            field=models.ManyToManyField(to='UIS.Course', through='UIS.PeriodCourse', blank=True),
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(to='UIS.Faculty', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='degree',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='UIS.Department'),
        ),
        migrations.AddField(
            model_name='degree',
            name='first_intake',
            field=models.ForeignKey(blank=True, to='UIS.Period', null=True),
        ),
        migrations.AddField(
            model_name='degree',
            name='minors',
            field=models.ManyToManyField(related_name='minors_rel_+', to='UIS.Degree', blank=True),
        ),
        migrations.AddField(
            model_name='degree',
            name='replaced_degrees',
            field=models.ManyToManyField(related_name='replaced_degrees_rel_+', to='UIS.Degree', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='degrees',
            field=models.ManyToManyField(related_name='courses', through='UIS.DegreeCourse', to='UIS.Degree', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='UIS.Department'),
        ),
        migrations.AddField(
            model_name='course',
            name='equalled_courses',
            field=models.ManyToManyField(related_name='equalled_with', to='UIS.Course', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='first_taught',
            field=models.ForeignKey(related_name='first_taught_set', on_delete=django.db.models.deletion.PROTECT, verbose_name='First period given', blank=True, to='UIS.Period', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='last_tught',
            field=models.ForeignKey(related_name='last_taught_set', on_delete=django.db.models.deletion.PROTECT, verbose_name='Last period given', blank=True, to='UIS.Period', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='userrole',
            unique_together=set([('user', 'role', 'object_id')]),
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='student',
            field=models.ForeignKey(related_name='studentregistration', verbose_name='student', to='UIS.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='studentenrolmentlog',
            unique_together=set([('student_registration', 'section', 'enrolment_status')]),
        ),
        migrations.AlterUniqueTogether(
            name='studentenrolment',
            unique_together=set([('student_registration', 'section')]),
        ),
        migrations.AddField(
            model_name='student',
            name='periods',
            field=models.ManyToManyField(related_name='students', through='UIS.StudentRegistration', to='UIS.PeriodDegree'),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('section_type', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='perioddegree',
            unique_together=set([('period', 'degree')]),
        ),
        migrations.AlterUniqueTogether(
            name='periodcourse',
            unique_together=set([('period', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='period',
            unique_together=set([('academic_year', 'period')]),
        ),
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(to='UIS.Department', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterUniqueTogether(
            name='degreecourse',
            unique_together=set([('course', 'degree')]),
        ),
        migrations.AlterUniqueTogether(
            name='degree',
            unique_together=set([('name', 'credits_required', 'department'), ('name_ar', 'credits_required', 'department')]),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('code', 'name', 'department', 'first_taught', 'is_obsolete'), ('code', 'name_ar', 'department', 'first_taught', 'is_obsolete')]),
        ),
        migrations.AlterUniqueTogether(
            name='studentregistration',
            unique_together=set([('student', 'period_degree')]),
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together=set([('username', 'department')]),
        ),
    ]
