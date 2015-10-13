# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from subprocess import Popen, PIPE
import tempfile
from .models.students import Student


def student_enrolment_as_pdf(request, registration_number):

    student = Student.objects.get(registration_number=registration_number)
    context = {
        'student': student,
        'allowed_courses': student.get_allowed_enrolments()
    }
    template = get_template('my_template.tex', using='jinja2')
    rendered_tpl = template.render(context=context).encode('utf8')
    # with open(os.path.join(
    #         '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/',
    #         's'+registration_number), 'w') as texfile:
    #     texfile.write(rendered_tpl)
    # Python3 only. For python2 check out the docs!
    if student.advisor == None:
        student.advisor = "بدون مشرف"
    directory = os.path.join(
        '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/student_enrolment/' +
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
             '-jobname', ' '.join([student.get_full_name_ar(), ' - ',
                                   registration_number]),
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


def student_grade_as_pdf(request, registration_number):

    student = Student.objects.get(registration_number=registration_number)
    context = {
        'student': student,
        'enrolments': student.get_enroled_courses(),
        'registrations': student.student_registrations.all(),
        'results': student.student_registrations.last().studentresult,
    }
    template = get_template('student_grade_template.tex', using='jinja2')
    rendered_tpl = template.render(context=context).encode('utf8')
    # with open(os.path.join(
    #         '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/tests/',
    #         's'+registration_number+'.tex'), 'w') as texfile:
    #     texfile.write(rendered_tpl)
    # Python3 only. For python2 check out the docs!
    if student.advisor == None:
        student.advisor = "بدون مشرف"
    directory = os.path.join(
        '/home/abdulhaq/workspace/pX/pX-tools/legacyDB/student_grade/' +
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
             '-jobname', ' '.join([student.get_full_name_ar(), ' - ',
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
