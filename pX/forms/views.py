# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.template.loader import get_template

import os
from django.http import HttpResponse
from django.template import Context
from subprocess import Popen, PIPE
import tempfile
from ..students.models import Student
# from ..students.enrolments.models import StudentEnrolment


def student_enrolment_as_pdf(request, registration_number):

    student = Student.objects.get(registration_number=registration_number)
    # with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
    #     pdf = f.read()
    # r = HttpResponse(content_type='application/pdf')
    # # r['Content-Disposition'] = 'attachment; filename=texput.pdf'
    # r.write(pdf)
    # return r
    return None


def student_academic_progress(request, registration_number):

    student = Student.objects.get(registration_number=registration_number)
    # with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
    #      pdf = f.read()
    # r = HttpResponse(content_type='application/pdf')
    #  r['Content-Disposition'] = 'attachment; filename=texput.pdf'
    # r.write(pdf)
    # return r
    return None


def student_form2_pdf(request, registration_number, period_degree):

    student = Student.objects.get(registration_number=registration_number)
    student_registration = student.student_registrations.get(
        period_degree=period_degree)
    enrolments = StudentEnrolment.objects.filter(
        student_registration=student_registration)
    results = student_registration.studentresult
    nationalities = {
        'LY': 'ليبية',
        'EG': 'مصرية',
        'SD': 'سودانية',
        'IQ': 'عراقية',
        'TN': 'تونسية',
        'PS': 'فلسطينية',
        'SY': 'سورية',
        'MA': 'مغربية',
        'LB': 'لبنانية',
        'YE': 'يمنية',
        'PK': 'باكستانية',
        'IR': 'إيرناية',
        'ER': 'أريتيرية',
        'TR': 'تركية',
        'NE': 'نيجرية',
        'MR': 'موريتانية',
        'DZ': 'جزائرية',
        'DJ': 'جيوبوتية',
        'TD': 'تشادية',
    }
    nationality = nationalities[student.nationality]
    context = {
        'student': student,
        'enrolments': enrolments,
        'student_registration': student_registration,
        'results': results,
        'nationality': nationality
    }
    template = get_template('form2_template.tex', using='jinja2')
    rendered_tpl = template.render(context=context).encode('utf8')

    with open(os.path.join(
            '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/tests/',
            's'+registration_number+'.tex'), 'w') as texfile:
        texfile.write(rendered_tpl)
    # Python3 only. For python2 check out the docs!
    if student.advisor is None:
        student.advisor = "بدون مشرف"
    directory = os.path.join(
        '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/student_form2/' +
        student.advisor
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    #tempdir = tempfile.mkdtemp()
    # Create subprocess, supress output with PIPE and
    # run latex twice to generate the TOC properly.
    # Finally read the generated pdf.
    for i in range(2):
        process = Popen(
            ['xelatex',
             '-jobname', ' '.join([student.full_name_ar, ' - ',
                                   registration_number]),
             '-output-directory', directory],
            stdin=PIPE,
            stdout=PIPE,
        )
        process.communicate(rendered_tpl)
    # with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
    #      pdf = f.read()
    # r = HttpResponse(content_type='application/pdf')
    #  r['Content-Disposition'] = 'attachment; filename=texput.pdf'
    # r.write(pdf)
    # return r
    return None


def advisors_list_as_pdf(request):
    advisors = [
        'د. جمال الشاوش', 'د. عبد الحميد عاشور', 'د. عبد الرسول قاسم',
        'د. علي الرابطي', 'د. أبوبكر الجعيدي', 'د. صالح باشا',
        'د. سعيد القطوس', 'د. صالح قشوط', 'د. مفتاح أبو جلالة',
        'م. منصف بادي', 'د. أيمن المحمودي', 'د. إبراهيم راشد',
        'د. سعد عيسى', 'م. محرم الشعايفي', 'د. عثمان مخلوف',
        'د. الطاهر الحشاني', 'د. عزالدين العربي', 'د. أشرف عمر',
        'د. فاتح العليج', 'م. عادل كربان', 'د. علي السوري']

    for advisor in advisors:

        students = Student.objects.filter(
            advisor=advisor,
            status='E').order_by('first_name_ar')
        context = {
            'students': students,
            'advisor': advisor
        }
        template = get_template('advisor_template.tex', using='jinja2')
        rendered_tpl = template.render(context=context).encode('utf8')
        # with open(os.path.join(
        #         '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/tests/',
        #         advisor), 'w') as texfile:
        #     texfile.write(rendered_tpl)
        # Python3 only. For python2 check out the docs!
        directory = os.path.join(
            '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/advisors_list_as_pdf/'
        )
        if not os.path.exists(directory):
            os.makedirs(directory)
        #tempdir = tempfile.mkdtemp()
        # Create subprocess, supress output with PIPE and
        # run latex twice to generate the TOC properly.
        # Finally read the generated pdf.
        for i in range(2):
            process = Popen(
                ['xelatex',
                 '-jobname', advisor,
                 '-output-directory', directory],
                stdin=PIPE,
                stdout=PIPE,
            )
            process.communicate(rendered_tpl)

    context = {
        'students': (Student.objects.filter(status='E').exclude(advisor=None).
                     order_by('first_name_ar')),
    }

    template = get_template('advisor_list_template.tex', using='jinja2')
    rendered_tpl = template.render(context=context).encode('utf8')
    # with open(os.path.join(
    #         '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/',
    #         's'+registration_number), 'w') as texfile:
    #     texfile.write(rendered_tpl)
    # Python3 only. For python2 check out the docs!
    directory = os.path.join(
        '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/advisors_list_as_pdf/'
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    #tempdir = tempfile.mkdtemp()
    # Create subprocess, supress output with PIPE and
    # run latex twice to generate the TOC properly.
    # Finally read the generated pdf.
    for i in range(2):
        process = Popen(
            ['xelatex',
             '-jobname', 'advisors_list',
             '-output-directory', directory],
            stdin=PIPE,
            stdout=PIPE,
        )
        process.communicate(rendered_tpl)
    # with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
    #     pdf = f.read()
    # r = HttpResponse(content_type='application/pdf')
    # # r['Content-Disposition'] = 'attachment; filename=texput.pdf'
    # r.write(pdf)
    # return r
    return None
