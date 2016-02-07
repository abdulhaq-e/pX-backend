from django.core.management.base import BaseCommand
import unicodecsv

from UIS.models.students import Student


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    FILES_LOCATION = 'reports/'

    def _export(self):
        report_file = self.FILES_LOCATION + 'Summary.csv'

        with open(report_file, 'w') as csvfile:
            writer = unicodecsv.DictWriter(
                csvfile, fieldnames=[
                    'registration_number',
                    'first_name_ar',
                    'last_name_ar',
                    'first_name_en',
                    'last_name_en',
                    'period_count',
                    'actual_period_count',
                    'first_period',
                    'last_period',
                    'registered_credits',
                    'passed_credits',
                    'GPA',
                    'status'
                ])
            writer.writeheader()

            for i in Student.objects.all():
                if self.verbosity > 1:
                    print('Processing student {}'.format(i.registration_number))

                results = i.get_prettier_results()

                if results[0]['Periods']:
                    first_period = results[0]['Periods'][0]
                    last_period = results[0]['Periods'][-1]
                    last_results = results[0]['Results'][last_period]['Statistics']
                    writer.writerow(
                    {'registration_number': i.registration_number,
                     'first_name_ar': i.first_name_ar,
                     'last_name_ar': i.last_name_ar,
                     'first_name_en': i.first_name_en,
                     'last_name_en': i.last_name_en,
                     'period_count': last_results.get('period_count'),
                     'actual_period_count': last_results.get(
                         'actual_period_count'),
                     'first_period': first_period,
                     'last_period': last_period,
                     'passed_credits': last_results.get(
                         'cumulative_passed_credits'),
                     'registered_credits': last_results.get(
                         'cumulative_registered_credits'),
                     'GPA': last_results.get('cumulative_GPA'),
                     'status': i.get_status_display()
                     }
                    )
                else:
                    writer.writerow(
                    {'registration_number': i.registration_number,
                     'first_name_ar': i.first_name_ar,
                     'last_name_ar': i.last_name_ar,
                     'first_name_en': i.first_name_en,
                     'last_name_en': i.last_name_en,
                     'period_count': 0,
                     'actual_period_count': 0,
                     'first_period': '',
                     'last_period': '',
                     'passed_credits': '',
                     'registered_credits': '',
                     'GPA': '',
                     'status': ''
                     }
                    )

                if self.verbosity > 1:
                    print('Added student {}'.format(i.registration_number))

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')
        self._export()
