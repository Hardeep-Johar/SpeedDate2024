from django.shortcuts import render

from speed_date.models import Course, Group, Dollars, Results, Notes
from speed_date.rotation_generator import *

def do_edit_group(request,course_num):
    pass

def do_add_group(request,course_num):
    context = dict()
    the_user=request.user
    if not the_user.username == 'hardeepjohar':
        context['user_name'] = the_user.username
        return render(request,'unauthorized.html',context)
    else:
        course = Course.objects.get(course_number=course_num)
        groups = Group.objects.all()
        group_num = 0
        for group in groups:
            if group_num <= group.group_number:
                group_num = group.group_number + 1
        context['group_number'] = group_num
        context['course'] = course
        return render(request,'add_a_group.html',context)

def do_rotation_generate(request,course_num):
    course = Course.objects.get(course_number=course_num)
    group_list = course.group_set.all()
    group_names = list()
    group_names.append('Prof') #Add prof
    for group in group_list:
        group_names.append(group.group_name)
    date_dict = generate_rotations(group_names)
    #print(date_dict)
    write_rotations_to_file(date_dict,course_num)
    context=dict()
    set_up_dollars(course_num)
    set_up_notes(course_num)
    context['course'] = course
    context['group_list'] = group_list
    return render(request,"course_admin.html",context)

def do_rotation_print(request,course_num):
    pass

def set_up_notes(course_num):
    course = Course.objects.get(course_number=course_num)
    groups = course.group_set.all()
    for group in groups:
        for startup in groups:
            if group == startup:
                continue
            try:
                group.notes_set.get(group_2=startup.group_name).delete()
            except:
                pass
            note = Notes(group=group,group_2=startup,notes='')
            note.save()

def set_up_dollars(course_num):
    course = Course.objects.get(course_number=course_num)
    groups = course.group_set.all()
    for investor in groups:
        for startup in groups:
            if investor==startup:
                continue
            try:
                investor.dollars_set.get(group_2=startup.group_name).delete()
            except:
                pass
            dollar = Dollars(group_1=investor,group_2=startup.group_name)
            dollar.save()

def do_compile_dollars(request,course_num):
    context_dictionary=dict()
    course = Course.objects.get(course_number=course_num)
    groups = course.group_set.all()
    for group in groups:
        try:
            result = course.results_set.get(group=group.group_name)
        except:
            result = Results(course=course,group=group.group_name)
        else:
            result.interesting_dollars = 0.0
            result.completeness_dollars = 0.0
            result.gizmos_dollars = 0.0
        result.save()
    interesting_total = 0.0
    completeness_total = 0.0
    gizmos_total = 0.0
    for group in groups:
        dollars = group.dollars_set.all()
        for dollar in dollars:
            g2 = dollar.group_2
            result = course.results_set.get(group=g2)
            result.interesting_dollars += dollar.interesting_dollars
            result.completeness_dollars += dollar.completeness_dollars
            result.gizmos_dollars += dollar.gizmos_dollars
            interesting_total +=dollar.interesting_dollars
            completeness_total += dollar.completeness_dollars
            gizmos_total += dollar.gizmos_dollars
            result.get_total_dollars()
            result.save()
    results_list = course.results_set.order_by('-total_dollars')
    #results_list.reverse()
    context_dictionary['results'] = results_list
    context_dictionary['course'] = course
    context_dictionary['tinteresting'] = interesting_total
    context_dictionary['tcompleteness'] = completeness_total
    context_dictionary['tgizmos'] = gizmos_total
    context_dictionary['ttotal'] = interesting_total + completeness_total + gizmos_total
    return render(request,'compiled_scores.html',context_dictionary)